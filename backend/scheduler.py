"""
Background Weekly Automation Scheduler for Competitor Ad Tracker.
Runs the weekly pipeline: Collect Ads -> AI Summarize -> Post to Slack & Email.
"""

import time
import threading
from datetime import datetime, timedelta
from backend import database, ad_collector, summarizer, notifier
from backend.config import SCHEDULE_DAY, SCHEDULE_HOUR, SCHEDULE_MINUTE, SCHEDULE_ENABLED

class PipelineScheduler:
    def __init__(self):
        self.running = False
        self.thread = None
        self.last_run = database.get_setting("last_pipeline_run", None)
        self.is_executing = False

    def start(self):
        """Starts the scheduler thread."""
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print("[Scheduler] Weekly Competitor Ad Tracker background engine started.")

    def stop(self):
        self.running = False

    def _run_loop(self):
        while self.running:
            try:
                enabled = database.get_setting("schedule_enabled", str(SCHEDULE_ENABLED)).lower() == "true"
                if enabled and not self.is_executing:
                    target_day = database.get_setting("schedule_day", SCHEDULE_DAY).lower()
                    target_hour = int(database.get_setting("schedule_hour", SCHEDULE_HOUR))
                    target_minute = int(database.get_setting("schedule_minute", SCHEDULE_MINUTE))

                    now = datetime.now()
                    current_day = now.strftime("%A").lower()

                    if current_day == target_day and now.hour == target_hour and now.minute == target_minute:
                        # Ensure we haven't already run in the last 60 minutes
                        last_run_str = database.get_setting("last_pipeline_run")
                        should_run = True
                        if last_run_str:
                            try:
                                last_dt = datetime.strptime(last_run_str, "%Y-%m-%d %H:%M:%S")
                                if (now - last_dt).total_seconds() < 3600:
                                    should_run = False
                            except Exception:
                                pass

                        if should_run:
                            print(f"[Scheduler] Triggering scheduled weekly pipeline: {now.strftime('%Y-%m-%d %H:%M:%S')}")
                            self.run_pipeline(trigger_source="scheduled")
            except Exception as e:
                print(f"[Scheduler] Error in loop: {e}")

            time.sleep(30) # Check every 30 seconds

    def run_pipeline(self, trigger_source="manual"):
        """
        Executes the full automated workflow:
        1. Collects fresh ads from the 3 competitor brands
        2. Generates the AI weekly intelligence digest
        3. Dispatches notifications to Slack and/or Email
        """
        if self.is_executing:
            return {"status": "busy", "message": "Pipeline is already actively executing."}

        self.is_executing = True
        start_time = datetime.now()
        report = {
            "trigger_source": trigger_source,
            "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "steps": {}
        }

        try:
            # 1. Ingest ads
            print(f"[Pipeline] Step 1: Collecting ads from 3 competitor brands...")
            collect_res = ad_collector.collect_ads_for_all_competitors(ads_per_competitor=3)
            report["steps"]["collection"] = collect_res

            # 2. AI Summarization
            print(f"[Pipeline] Step 2: Generating weekly AI summary & narrative analysis...")
            digest = summarizer.generate_weekly_digest(custom_days=7)
            report["steps"]["digest_id"] = digest.get("id") if digest else None

            # 3. Post to Slack
            print(f"[Pipeline] Step 3: Posting summary to Slack...")
            slack_res = notifier.send_slack_notification(digest)
            report["steps"]["slack"] = slack_res

            # 4. Post to Email
            print(f"[Pipeline] Step 4: Posting summary to Email...")
            email_res = notifier.send_email_notification(digest)
            report["steps"]["email"] = email_res

            # Record success
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.last_run = now_str
            database.set_setting("last_pipeline_run", now_str)
            report["status"] = "success"
            report["completed_at"] = now_str
            print(f"[Pipeline] End-to-end pipeline finished successfully at {now_str}.")

        except Exception as e:
            report["status"] = "error"
            report["error"] = str(e)
            print(f"[Pipeline] Execution error: {e}")
        finally:
            self.is_executing = False

        return report

    def get_status(self):
        """Returns scheduler state and time of next run."""
        enabled = database.get_setting("schedule_enabled", str(SCHEDULE_ENABLED)).lower() == "true"
        target_day = database.get_setting("schedule_day", SCHEDULE_DAY).capitalize()
        target_hour = int(database.get_setting("schedule_hour", SCHEDULE_HOUR))
        target_minute = int(database.get_setting("schedule_minute", SCHEDULE_MINUTE))

        # Calculate next execution date
        now = datetime.now()
        days_ahead = {
            "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
            "Friday": 4, "Saturday": 5, "Sunday": 6
        }
        target_day_idx = days_ahead.get(target_day, 0)
        current_day_idx = now.weekday()

        day_diff = (target_day_idx - current_day_idx) % 7
        target_time = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
        if day_diff == 0 and now >= target_time:
            day_diff = 7

        next_run = (now + timedelta(days=day_diff)).replace(hour=target_hour, minute=target_minute, second=0)

        return {
            "enabled": enabled,
            "target_day": target_day,
            "target_time": f"{target_hour:02d}:{target_minute:02d}",
            "last_run": database.get_setting("last_pipeline_run", self.last_run or "Never"),
            "next_run": next_run.strftime("%A, %b %d at %I:%M %p") if enabled else "Disabled",
            "is_executing": self.is_executing
        }

scheduler_instance = PipelineScheduler()
