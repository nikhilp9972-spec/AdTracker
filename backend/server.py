"""
Competitor Ad Tracker - Python HTTP REST API Server.
Zero-dependency, multi-threaded REST API server with frontend static file serving.
"""

import os
import sys
import json
import socket
import mimetypes
from urllib.parse import urlparse, parse_qs
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from backend import database, ad_collector, summarizer, notifier, seed_data
from backend.scheduler import scheduler_instance
from backend.config import HOST, PORT, FRONTEND_DIR

class AdTrackerRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS for modern web clients
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def send_json(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def send_error_json(self, message, status_code=400):
        self.send_json({"status": "error", "message": message}, status_code=status_code)

    def parse_body(self):
        """Helper to read and parse JSON request body."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length > 0:
                raw_body = self.rfile.read(content_length).decode("utf-8")
                return json.loads(raw_body)
        except Exception as e:
            print(f"[Server] Failed to parse request body: {e}")
        return {}

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # API Endpoints
        if path.startswith("/api/"):
            try:
                # Competitors
                if path == "/api/competitors":
                    active_only = query.get("active_only", ["true"])[0].lower() == "true"
                    return self.send_json(database.get_competitors(active_only=active_only))

                # Ads Listing with EdTech and Cross-Platform Filtering
                elif path == "/api/ads":
                    comp_id = query.get("competitor_id", [None])[0]
                    platform = query.get("platform", [None])[0]
                    category = query.get("category", [None])[0]
                    offer_type = query.get("offer_type", [None])[0]
                    cta = query.get("cta", [None])[0]
                    is_demo_param = query.get("is_demo", [None])[0]
                    is_demo = int(is_demo_param) if is_demo_param in ["0", "1"] else None
                    search = query.get("search", [None])[0]
                    limit = int(query.get("limit", [100])[0])
                    offset = int(query.get("offset", [0])[0])
                    
                    ads = database.get_ads(
                        competitor_id=comp_id,
                        platform=platform,
                        category=category,
                        offer_type=offer_type,
                        cta=cta,
                        is_demo=is_demo,
                        search=search,
                        limit=limit,
                        offset=offset
                    )
                    return self.send_json(ads)

                # Digests
                elif path == "/api/digests/latest":
                    digest = database.get_latest_digest()
                    return self.send_json(digest or {})

                elif path == "/api/digests":
                    limit = int(query.get("limit", [20])[0])
                    return self.send_json(database.get_all_digests(limit=limit))

                elif path.startswith("/api/digests/"):
                    d_id = path.replace("/api/digests/", "")
                    digest = database.get_digest_by_id(d_id)
                    if digest:
                        return self.send_json(digest)
                    return self.send_error_json("Digest not found", 404)

                # Scheduler & Pipeline Status
                elif path == "/api/scheduler/status":
                    return self.send_json(scheduler_instance.get_status())

                # Audience Reach & Share of Voice Analytics
                elif path == "/api/analytics/reach":
                    industry = query.get("industry", [None])[0]
                    return self.send_json(database.get_reach_analytics(industry_filter=industry))

                # Cross-Platform Analytics (Meta vs Google Ads & Discover)
                elif path == "/api/analytics/cross-platform":
                    return self.send_json(database.get_cross_platform_analytics())

                # Transparent Collection Logs
                elif path == "/api/collection-logs":
                    limit = int(query.get("limit", [30])[0])
                    return self.send_json(database.get_collection_logs(limit=limit))

                # Dashboard Summary Stats
                elif path == "/api/stats":
                    return self.send_json(database.get_dashboard_stats())

                # Notification Audit Logs
                elif path == "/api/notifications/logs":
                    limit = int(query.get("limit", [25])[0])
                    return self.send_json(database.get_notification_logs(limit=limit))

                # Slack Block Kit Preview
                elif path == "/api/notifications/preview-slack":
                    digest = database.get_latest_digest()
                    if not digest:
                        return self.send_error_json("No digest found to preview", 404)
                    return self.send_json(notifier.build_slack_block_kit(digest))

                # Email HTML Preview
                elif path == "/api/notifications/preview-email":
                    digest = database.get_latest_digest()
                    if not digest:
                        return self.send_error_json("No digest found to preview", 404)
                    html = notifier.build_email_html(digest)
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.end_headers()
                    return self.wfile.write(html.encode("utf-8"))

                # Settings
                elif path == "/api/settings":
                    return self.send_json(database.get_all_settings())

                else:
                    return self.send_error_json("Unknown API endpoint", 404)

            except Exception as e:
                return self.send_error_json(str(e), 500)

        # Static File Serving for Frontend
        return self.serve_static(path)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        body = self.parse_body()

        if not path.startswith("/api/"):
            return self.send_error_json("Not found", 404)

        try:
            # 1. Trigger Full Ad Collection (All Competitors)
            if path == "/api/ads/collect":
                count = int(body.get("ads_per_competitor", 4))
                res = ad_collector.collect_ads_for_all_competitors(ads_per_competitor=count)
                return self.send_json(res)

            # 1b. Trigger Single Competitor Ad Collection
            elif path == "/api/ads/collect-single":
                comp_id = body.get("competitor_id")
                if not comp_id:
                    return self.send_error_json("competitor_id is required", 400)
                count = int(body.get("count", 4))
                res = ad_collector.collect_ads_for_single_competitor(comp_id, count=count)
                return self.send_json(res)

            # 1c. Manual Verified Ad Import (Strict transparency: allow marketing team to paste verified ad link)
            elif path == "/api/ads/import-manual":
                comp_id = body.get("competitor_id")
                headline = body.get("headline")
                body_text = body.get("body_text", "")
                platform = body.get("platform", "meta").lower()
                ad_url = body.get("ad_library_url") or body.get("landing_page_url", "")
                
                if not comp_id or not headline:
                    return self.send_error_json("competitor_id and headline are required", 400)

                categories = body.get("course_categories") or ad_collector.classify_edtech_ad(body_text, headline)
                hook = body.get("marketing_hook") or ad_collector.extract_marketing_hook(body_text, headline)
                vp = body.get("value_proposition") or ad_collector.extract_value_proposition(f"{headline} {body_text}")
                offer = body.get("offer_details") or ad_collector.extract_offer_details(f"{headline} {body_text}")
                aud = body.get("audience_hypothesis") or ad_collector.infer_target_audience(body_text, categories)
                strat = body.get("creative_strategy") or ad_collector.infer_creative_strategy(body_text, platform=platform)
                google_plc = body.get("google_placement", "Search" if platform == "google" else "Standard Feed")
                is_verified = int(body.get("is_placement_verified", 1 if platform == "google" else 0))

                saved = database.save_ad({
                    "competitor_id": comp_id,
                    "external_ad_id": body.get("external_ad_id", f"manual_{os.urandom(4).hex()}"),
                    "platform": platform,
                    "headline": headline,
                    "body_text": body_text,
                    "cta_text": body.get("cta_text", "Learn More"),
                    "creative_url": body.get("creative_url", ""),
                    "media_type": body.get("media_type", "image"),
                    "landing_page_url": body.get("landing_page_url", ad_url),
                    "first_seen": body.get("first_seen"),
                    "last_seen": body.get("last_seen"),
                    "status": "active",
                    "impressions_range": body.get("impressions_range", "Manual Verified"),
                    "spend_tier": body.get("spend_tier", "Verified"),
                    "course_categories": categories,
                    "marketing_hook": hook,
                    "value_proposition": vp,
                    "offer_details": offer,
                    "audience_hypothesis": aud,
                    "creative_strategy": strat,
                    "google_placement": google_plc,
                    "is_placement_verified": is_verified,
                    "ad_library_url": ad_url,
                    "is_demo": 0,
                    "source": "manual_import"
                })
                return self.send_json({"status": "success", "ad": saved})

            # 2. Trigger AI Digest Generation
            elif path == "/api/digests/generate":
                days = int(body.get("days", 7))
                digest = summarizer.generate_weekly_digest(custom_days=days)
                return self.send_json(digest)

            # 3. Post to Slack
            elif path == "/api/notifications/slack":
                digest_id = body.get("digest_id")
                digest = database.get_digest_by_id(digest_id) if digest_id else database.get_latest_digest()
                if not digest:
                    return self.send_error_json("No digest available to send", 400)
                webhook_url = body.get("webhook_url")
                res = notifier.send_slack_notification(digest, webhook_url=webhook_url)
                return self.send_json(res)

            # 4. Post to Email
            elif path == "/api/notifications/email":
                digest_id = body.get("digest_id")
                digest = database.get_digest_by_id(digest_id) if digest_id else database.get_latest_digest()
                if not digest:
                    return self.send_error_json("No digest available to send", 400)
                recipients = body.get("recipients")
                res = notifier.send_email_notification(digest, recipient_list=recipients)
                return self.send_json(res)

            # 5. Test Slack Webhook
            elif path == "/api/notifications/test-slack":
                url = body.get("webhook_url") or database.get_setting("slack_webhook_url")
                res = notifier.test_slack_webhook(url)
                return self.send_json(res)

            # 6. Test Email SMTP
            elif path == "/api/notifications/test-email":
                host = body.get("host") or database.get_setting("smtp_host")
                port = body.get("port") or database.get_setting("smtp_port", 587)
                user = body.get("user") or database.get_setting("smtp_user")
                passwd = body.get("pass") or database.get_setting("smtp_pass")
                sender = body.get("from") or database.get_setting("smtp_from")
                test_recip = body.get("recipient")
                res = notifier.test_email_smtp(host, port, user, passwd, sender, test_recip)
                return self.send_json(res)

            # 7. Add or Update Competitor
            elif path == "/api/competitors":
                name = body.get("name")
                if not name:
                    return self.send_error_json("Competitor brand name is required", 400)
                comp = database.upsert_competitor(
                    name=name,
                    domain=body.get("domain"),
                    industry=body.get("industry", "EdTech"),
                    logo_url=body.get("logo_url"),
                    platforms=body.get("platforms"),
                    active=body.get("active", 1),
                    comp_id=body.get("id")
                )
                return self.send_json(comp)

            # 8. Delete Competitor
            elif path.startswith("/api/competitors/delete"):
                comp_id = body.get("id")
                if comp_id:
                    database.delete_competitor(comp_id)
                    return self.send_json({"status": "success", "message": f"Competitor {comp_id} removed"})
                return self.send_error_json("Missing competitor id", 400)

            # 9. Update Scheduler Settings
            elif path == "/api/scheduler/update":
                if "enabled" in body:
                    database.set_setting("schedule_enabled", str(body["enabled"]).lower())
                if "day" in body:
                    database.set_setting("schedule_day", str(body["day"]).lower())
                if "hour" in body:
                    database.set_setting("schedule_hour", str(body["hour"]))
                if "minute" in body:
                    database.set_setting("schedule_minute", str(body["minute"]))
                return self.send_json(scheduler_instance.get_status())

            # 10. Update General Settings
            elif path == "/api/settings":
                for k, v in body.items():
                    database.set_setting(k, v)
                return self.send_json({"status": "success", "settings": database.get_all_settings()})

            # 11. Run Full Pipeline Now (End-to-End: Collect -> Summarize -> Post)
            elif path == "/api/pipeline/run-now":
                report = scheduler_instance.run_pipeline(trigger_source="manual_web_ui")
                return self.send_json(report)

            else:
                return self.send_error_json("Unknown POST endpoint", 404)

        except Exception as e:
            return self.send_error_json(str(e), 500)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path.startswith("/api/competitors/"):
            comp_id = path.replace("/api/competitors/", "").strip("/")
            database.delete_competitor(comp_id)
            return self.send_json({"status": "success", "message": f"Deleted competitor {comp_id}"})
        return self.send_error_json("Not found", 404)

    def serve_static(self, path):
        """Serves files from the frontend directory."""
        if path == "/" or path == "":
            file_path = FRONTEND_DIR / "index.html"
        else:
            rel_path = path.lstrip("/")
            file_path = FRONTEND_DIR / rel_path

        if not file_path.exists() or file_path.is_dir():
            file_path = FRONTEND_DIR / "index.html"

        if not file_path.exists():
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")
            return

        # Determine MIME type
        content_type, _ = mimetypes.guess_type(str(file_path))
        if not content_type:
            content_type = "application/octet-stream"
            if str(file_path).endswith(".css"):
                content_type = "text/css"
            elif str(file_path).endswith(".js"):
                content_type = "application/javascript"

        try:
            with open(file_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", f"{content_type}; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"500 Internal Error: {e}".encode("utf-8"))

def start_server():
    """Initializes database, seeds default data, starts scheduler, and boots HTTP server."""
    print("=" * 60)
    print("  🚀 Starting AdPulse Intelligence - EdTech Ad Tracker")
    print("=" * 60)

    # 1. Initialize SQLite Database
    database.init_db()

    # 2. Seed initial EdTech competitors (PW, Unacademy, Scaler), authentic ads, and digest
    seed_data.seed_database_if_empty()

    # 3. Start Background Scheduler
    scheduler_instance.start()

    # 4. Start HTTP Server (Dual-stack IPv4 & IPv6 support so localhost and 127.0.0.1 both work seamlessly)
    httpd = None
    try:
        class DualStackThreadingServer(ThreadingHTTPServer):
            address_family = socket.AF_INET6

            def server_bind(self):
                try:
                    self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
                except Exception:
                    pass
                super().server_bind()

        httpd = DualStackThreadingServer(("::", PORT), AdTrackerRequestHandler)
    except Exception:
        server_address = (HOST, PORT)
        httpd = ThreadingHTTPServer(server_address, AdTrackerRequestHandler)

    print(f"[Server] Serving Web UI & REST API at http://localhost:{PORT} and http://127.0.0.1:{PORT}")
    print(f"[Server] Ready for marketing team requests. Press Ctrl+C to terminate.")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[Server] Shutting down gracefully...")
        scheduler_instance.stop()
        httpd.server_close()
        sys.exit(0)

if __name__ == "__main__":
    start_server()
