"""
Notification Engine for EdTech Competitor Ad Intelligence.
Formats and dispatches weekly intelligence briefs to:
1. Slack (via Incoming Webhook with Block Kit formatting)
2. Email (via SMTP with responsive modern HTML newsletter template)
"""

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from backend import database
from backend.config import (
    SLACK_WEBHOOK_URL,
    SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SMTP_FROM, EMAIL_RECIPIENTS
)

def clean_error_message(text, max_len=180):
    """Sanitizes error text to prevent dumping large HTML or JSON blobs into UI alerts."""
    if not text:
        return "Unknown error"
    import re
    # Remove any HTML tags or script blocks
    clean = re.sub(r'<[^>]+>', ' ', text)
    clean = ' '.join(clean.split()).strip()
    if len(clean) > max_len:
        clean = clean[:max_len] + "..."
    return clean

def build_slack_block_kit(digest):
    """Constructs a professional, highly readable Slack Block Kit payload for EdTech intelligence."""
    title = digest.get("title", "EdTech Competitor Ad Intelligence Brief")
    exec_summary = digest.get("executive_summary", "")
    brand_breakdowns = digest.get("brand_breakdowns", [])
    macro_themes = digest.get("macro_themes", [])
    counter_strategies = digest.get("counter_strategies", [])
    cross_platform = digest.get("cross_platform_intelligence", {})

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"🎓 {title}",
                "emoji": True
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"*Period:* {digest.get('period_start')} to {digest.get('period_end')} | *Sector:* EdTech & Upskilling | *Status:* Automated Monitored Run"
                }
            ]
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*📋 Executive Summary:*\n{exec_summary}"
            }
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*🥊 Competitor Brand Analysis (Physics Wallah, Unacademy, Scaler & Peers):*"
            }
        }
    ]

    for brand in brand_breakdowns:
        name = brand.get("competitor_name", "Brand")
        narrative = brand.get("primary_narrative", "")
        cats = ", ".join(brand.get("promoted_categories", ["Online Courses"])[:3])
        offers = ", ".join(brand.get("active_offers", ["Standard Pricing"])[:2])
        hooks = ", ".join(brand.get("dominant_hooks", ["Skill Development"])[:2])
        ads_count = brand.get("ads_tracked", 0)
        recent_ads = brand.get("recent_ads", [])
        aud_hyp = brand.get("audience_hypothesis", "AI Hypothesis: Prospective learners")

        recent_ads_lines = []
        for ra in recent_ads[:2]:
            plat = ra.get("platform", "ad").upper()
            plc = ra.get("google_placement", "Feed")
            headline = ra.get("headline", "New Course Launch")
            cta = ra.get("cta_text", "Enroll Now")
            url = ra.get("ad_library_url") or "#"
            body = ra.get("body_text", "")
            if len(body) > 90:
                body = body[:90] + "..."
            
            tag = f"[{plat} • {plc}]" if plat == "GOOGLE" else f"[{plat}]"
            link_part = f"<{url}|View Ad ↗>" if url and url != "#" else ""
            recent_ads_lines.append(f"> • *{tag}* \"{headline}\"\n>   _{body}_ `[CTA: {cta}]` {link_part}")

        recent_ads_block = ("\n\n*📰 Sample Creatives Monitored:*\n" + "\n".join(recent_ads_lines)) if recent_ads_lines else ""

        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    f"*• {name}* ({ads_count} ads monitored)\n"
                    f"_{narrative}_\n"
                    f"📚 *Top Courses:* `{cats}`\n"
                    f"⚡ *Hooks:* `{hooks}` | 🏷️ *Offers:* `{offers}`\n"
                    f"🎯 *Targeting:* _{aud_hyp}_"
                    f"{recent_ads_block}"
                )
            }
        })

    # Cross-Platform Intelligence
    if cross_platform and isinstance(cross_platform, dict):
        meta_count = cross_platform.get("meta_total_ads", 0)
        google_count = cross_platform.get("google_total_ads", 0)
        discover_count = cross_platform.get("verified_google_discover_ads", 0)
        summary = cross_platform.get("platform_comparison_summary", "Meta leads visual awareness; Google leads enrollment.")

        blocks.append({"type": "divider"})
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    f"*🌐 Cross-Platform Intelligence (Meta vs Google):*\n"
                    f"• *Meta Ad Library:* `{meta_count} ads` (Visual Reels, Testimonials, UGC)\n"
                    f"• *Google Transparency:* `{google_count} ads` (Search intent, Demand Gen, `{discover_count}` Verified Discover)\n"
                    f"_{summary}_"
                )
            }
        })

    # Recommended Actionable Counter-Strategies
    if counter_strategies:
        blocks.append({"type": "divider"})
        strat_lines = []
        for s in counter_strategies[:3]:
            strat_lines.append(f"• *{s.get('tactic')}:* {s.get('action')}")
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*💡 Strategic Opportunities For Our Marketing Team (AI Generated):*\n" + "\n".join(strat_lines)
            }
        })

    blocks.extend([
        {"type": "divider"},
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Open EdTech Ad Vault & Analytics 🚀",
                        "emoji": True
                    },
                    "url": "http://localhost:8000",
                    "style": "primary"
                }
            ]
        }
    ])

    return {"blocks": blocks}

def send_slack_notification(digest, webhook_url=None):
    """Posts the EdTech digest to Slack. Returns dict with status and message."""
    url = (webhook_url or database.get_setting("slack_webhook_url") or SLACK_WEBHOOK_URL or "").strip()
    if not url:
        return {"status": "skipped", "message": "No Slack Webhook URL configured"}

    if not url.startswith("https://hooks.slack.com/"):
        err = "Invalid Slack Webhook URL. It must start with 'https://hooks.slack.com/services/...'. You entered a workspace link (e.g. slack.com) instead of an Incoming Webhook."
        database.log_notification(
            channel="slack",
            recipient=url[:35] + "...",
            status="FAILED",
            digest_id=digest.get("id"),
            error_message=err
        )
        return {"status": "error", "message": err}

    payload = build_slack_block_kit(digest)
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp_text = resp.text.strip().lower()
        if resp.status_code == 200 and resp_text == "ok":
            database.log_notification(
                channel="slack",
                recipient=url[:35] + "...",
                status="SUCCESS",
                digest_id=digest.get("id")
            )
            return {"status": "success", "message": "Successfully posted weekly EdTech intelligence to Slack"}
        else:
            raw_err = clean_error_message(resp.text)
            err = f"Slack rejected webhook (HTTP {resp.status_code}): {raw_err}"
            database.log_notification(
                channel="slack",
                recipient=url[:35] + "...",
                status="FAILED",
                digest_id=digest.get("id"),
                error_message=err
            )
            return {"status": "error", "message": err}
    except Exception as e:
        err = clean_error_message(str(e))
        database.log_notification(
            channel="slack",
            recipient=url[:35] + "...",
            status="FAILED",
            digest_id=digest.get("id"),
            error_message=err
        )
        return {"status": "error", "message": err}

def build_email_html(digest):
    """Generates an ultra-clean, modern, luxury HTML email newsletter template for EdTech intelligence."""
    title = digest.get("title", "EdTech Competitor Ad Intelligence Brief")
    exec_summary = digest.get("executive_summary", "")
    brand_breakdowns = digest.get("brand_breakdowns", [])
    counter_strategies = digest.get("counter_strategies", [])
    cross_platform = digest.get("cross_platform_intelligence", {})

    brands_html = ""
    for brand in brand_breakdowns:
        name = brand.get("competitor_name", "Brand")
        narrative = brand.get("primary_narrative", "")
        cats = ", ".join(brand.get("promoted_categories", ["Online Courses"])[:3])
        offers = ", ".join(brand.get("active_offers", ["Standard Pricing"])[:2])
        hooks = ", ".join(brand.get("dominant_hooks", ["Skill Development"])[:2])
        ads_count = brand.get("ads_tracked", 0)
        recent_ads = brand.get("recent_ads", [])
        aud_hyp = brand.get("audience_hypothesis", "AI Hypothesis: Prospective learners")

        recent_ads_html = ""
        if recent_ads:
            recent_ads_html = '<div style="margin-top: 14px; padding-top: 12px; border-top: 1px solid #e2e8f0;"><div style="color: #64748b; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">Sample Monitored Creatives:</div>'
            for ra in recent_ads[:2]:
                plat = ra.get("platform", "ad").upper()
                plat_color = "#0081FB" if plat == "META" else "#EA4335"
                plc = ra.get("google_placement", "")
                tag = f"{plat} • {plc}" if plc and plat == "GOOGLE" else plat
                url = ra.get("ad_library_url") or "#"
                link_btn = f'<a href="{url}" style="color: #4f46e5; text-decoration: none; font-size: 11px; font-weight: 600;">View Ad ↗</a>' if url and url != "#" else ""

                recent_ads_html += f"""
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px 12px; margin-bottom: 8px;">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
                        <span style="background: {plat_color}; color: #ffffff; font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 4px;">{tag}</span>
                        {link_btn}
                    </div>
                    <strong style="color: #0f172a; font-size: 13px; display: block; margin-bottom: 2px;">{ra.get('headline', 'Course Campaign')}</strong>
                    <p style="color: #64748b; font-size: 12px; margin: 0 0 4px 0; line-height: 1.4;">{ra.get('body_text', '')}</p>
                    <span style="display: inline-block; background: #e0e7ff; color: #4338ca; font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 4px;">
                        CTA: {ra.get('cta_text', 'Learn More')}
                    </span>
                </div>
                """
            recent_ads_html += '</div>'

        brands_html += f"""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; margin-bottom: 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <h3 style="margin: 0; color: #0f172a; font-size: 18px; font-weight: 700;">{name}</h3>
                <span style="background: #4f46e5; color: #ffffff; font-size: 12px; font-weight: 600; padding: 4px 10px; border-radius: 20px;">
                    {ads_count} Active Creatives
                </span>
            </div>
            <p style="color: #334155; font-size: 13px; line-height: 1.6; margin: 0 0 12px 0;">{narrative}</p>
            <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 8px;">
                <span style="background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; font-size: 11px; padding: 3px 8px; border-radius: 6px;">
                    📚 Courses: {cats}
                </span>
                <span style="background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; font-size: 11px; padding: 3px 8px; border-radius: 6px;">
                    🏷️ Offers: {offers}
                </span>
                <span style="background: #f5f3ff; color: #6d28d9; border: 1px solid #ddd6fe; font-size: 11px; padding: 3px 8px; border-radius: 6px;">
                    ⚡ Hook: {hooks}
                </span>
            </div>
            <div style="font-size: 11px; color: #64748b; font-style: italic; margin-bottom: 8px;">
                🎯 {aud_hyp}
            </div>
            {recent_ads_html}
        </div>
        """

    strats_html = ""
    for s in counter_strategies[:3]:
        strats_html += f"""
        <li style="margin-bottom: 12px; color: #334155; font-size: 13px; line-height: 1.6;">
            <strong style="color: #4f46e5;">{s.get('tactic')}:</strong> {s.get('action')}
        </li>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
    </head>
    <body style="margin: 0; padding: 0; background-color: #f1f5f9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #0f172a;">
        <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 680px; margin: 30px auto; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.05);">
            <!-- Header -->
            <tr>
                <td style="padding: 36px 32px 24px 32px; background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%); color: #ffffff;">
                    <div style="display: inline-block; background: rgba(99, 102, 241, 0.25); border: 1px solid rgba(129, 140, 248, 0.4); border-radius: 20px; padding: 4px 12px; font-size: 11px; font-weight: 700; color: #a5b4fc; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;">
                        EdTech Competitor Ad Intelligence Brief
                    </div>
                    <h1 style="margin: 0 0 10px 0; color: #ffffff; font-size: 24px; font-weight: 800; letter-spacing: -0.5px;">{title}</h1>
                    <p style="margin: 0; color: #94a3b8; font-size: 13px;">Monitored Period: {digest.get('period_start')} to {digest.get('period_end')}</p>
                </td>
            </tr>

            <!-- Executive Summary -->
            <tr>
                <td style="padding: 28px 32px;">
                    <div style="background: #f8fafc; border-left: 4px solid #4f46e5; border-radius: 0 10px 10px 0; padding: 18px 20px; margin-bottom: 24px;">
                        <h4 style="margin: 0 0 8px 0; color: #4f46e5; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 700;">Executive Summary</h4>
                        <p style="margin: 0; color: #334155; font-size: 14px; line-height: 1.6;">{exec_summary}</p>
                    </div>

                    <h2 style="color: #0f172a; font-size: 18px; font-weight: 700; margin: 30px 0 16px 0;">Competitor Advertising Breakdown</h2>
                    {brands_html}

                    <h2 style="color: #0f172a; font-size: 18px; font-weight: 700; margin: 32px 0 16px 0;">Strategic Opportunities For Our Marketing Team</h2>
                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 22px;">
                        <ul style="margin: 0; padding-left: 20px;">
                            {strats_html}
                        </ul>
                    </div>

                    <!-- CTA Button -->
                    <div style="text-align: center; margin-top: 36px; margin-bottom: 16px;">
                        <a href="http://localhost:8000" style="display: inline-block; background: #4f46e5; color: #ffffff; font-size: 14px; font-weight: 700; text-decoration: none; padding: 14px 32px; border-radius: 8px; box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3);">
                            Open Dashboard & Ad Vault →
                        </a>
                    </div>
                </td>
            </tr>

            <!-- Footer -->
            <tr>
                <td style="padding: 20px 32px; background: #f8fafc; border-top: 1px solid #e2e8f0; text-align: center; color: #64748b; font-size: 12px;">
                    Automated by AdPulse EdTech Ad Intelligence Engine • Delivered weekly to growth and marketing leadership.
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

def send_email_notification(digest, recipient_list=None, smtp_settings=None):
    """Sends the HTML digest email via SMTP."""
    recipients = recipient_list or database.get_setting("email_recipients")
    if isinstance(recipients, str):
        recipients = [r.strip() for r in recipients.split(",") if r.strip()]
    if not recipients:
        recipients = EMAIL_RECIPIENTS

    if not recipients:
        return {"status": "skipped", "message": "No email recipients configured"}

    host = (smtp_settings and smtp_settings.get("host")) or database.get_setting("smtp_host") or SMTP_HOST
    port = int((smtp_settings and smtp_settings.get("port")) or database.get_setting("smtp_port") or SMTP_PORT)
    user = (smtp_settings and smtp_settings.get("user")) or database.get_setting("smtp_user") or SMTP_USER
    passwd = (smtp_settings and smtp_settings.get("pass")) or database.get_setting("smtp_pass") or SMTP_PASS
    sender = (smtp_settings and smtp_settings.get("from")) or database.get_setting("smtp_from") or SMTP_FROM

    if not user or not passwd:
        msg = f"[Simulated Mode] SMTP credentials not set. Simulated email delivery to {', '.join(recipients)}"
        database.log_notification(
            channel="email",
            recipient=", ".join(recipients),
            status="SUCCESS",
            digest_id=digest.get("id"),
            error_message="Simulated: SMTP credentials not set (Configure in Settings)"
        )
        return {"status": "simulated", "message": msg}

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🎓 {digest.get('title', 'Weekly EdTech Competitor Ad Brief')}"
        msg["From"] = sender
        msg["To"] = ", ".join(recipients)

        html_content = build_email_html(digest)
        part = MIMEText(html_content, "html")
        msg.attach(part)

        context = ssl.create_default_context()
        if port == 465:
            with smtplib.SMTP_SSL(host, port, context=context) as server:
                server.login(user, passwd)
                server.sendmail(sender, recipients, msg.as_string())
        else:
            with smtplib.SMTP(host, port) as server:
                server.starttls(context=context)
                server.login(user, passwd)
                server.sendmail(sender, recipients, msg.as_string())

        database.log_notification(
            channel="email",
            recipient=", ".join(recipients),
            status="SUCCESS",
            digest_id=digest.get("id")
        )
        return {"status": "success", "message": f"Email successfully sent to {', '.join(recipients)}"}

    except Exception as e:
        err = f"SMTP Error: {str(e)}"
        database.log_notification(
            channel="email",
            recipient=", ".join(recipients),
            status="FAILED",
            digest_id=digest.get("id"),
            error_message=err
        )
        return {"status": "error", "message": err}

def test_slack_webhook(url):
    """Sends an immediate test ping to the given Slack webhook."""
    url = (url or "").strip()
    if not url:
        return {"status": "error", "message": "Webhook URL is empty. Please enter your Slack Incoming Webhook URL in Settings."}

    if not url.startswith("https://hooks.slack.com/"):
        return {
            "status": "error",
            "message": "Invalid Slack URL. You entered a workspace or login link (e.g. scalerinternal.slack.com). Slack Webhooks must begin with: https://hooks.slack.com/services/..."
        }

    payload = {
        "text": "🟢 *AdPulse Intelligence Test Ping*\nYour Slack webhook is successfully configured and ready to receive weekly EdTech competitor briefs!"
    }
    try:
        res = requests.post(url, json=payload, timeout=8)
        resp_text = res.text.strip().lower()
        if res.status_code == 200 and resp_text == "ok":
            return {"status": "success", "message": "Slack webhook test passed! Verification message delivered to your channel."}
        
        raw_msg = clean_error_message(res.text)
        return {"status": "error", "message": f"Slack rejected webhook (HTTP {res.status_code}): {raw_msg}"}
    except Exception as e:
        return {"status": "error", "message": clean_error_message(str(e))}

def test_email_smtp(host, port, user, passwd, sender, test_recipient):
    """Sends an immediate test email to verify SMTP credentials."""
    if not user or not passwd or not test_recipient:
        return {"status": "error", "message": "Missing SMTP user, password, or recipient"}
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "🟢 AdPulse EdTech Ad Intelligence - Test Verification"
        msg["From"] = sender or user
        msg["To"] = test_recipient
        msg.attach(MIMEText("<h2>Test Email</h2><p>Your SMTP email configuration is active and working properly.</p>", "html"))

        context = ssl.create_default_context()
        if int(port) == 465:
            with smtplib.SMTP_SSL(host, int(port), context=context) as server:
                server.login(user, passwd)
                server.sendmail(sender or user, [test_recipient], msg.as_string())
        else:
            with smtplib.SMTP(host, int(port)) as server:
                server.starttls(context=context)
                server.login(user, passwd)
                server.sendmail(sender or user, [test_recipient], msg.as_string())
        return {"status": "success", "message": f"Test email sent successfully to {test_recipient}!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
