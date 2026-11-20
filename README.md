# 🎓 AdPulse Intelligence • Real-World Automated EdTech Competitor Ad Intelligence System

> **Automated Weekly Competitive Advertising Intelligence for EdTech:** Automatically monitors real advertisements from **Physics Wallah (PW)**, **Unacademy**, and **Scaler** (and custom EdTech brands), categorizes courses across 22 EdTech disciplines, analyzes marketing hooks and value propositions using AI, and delivers weekly strategic intelligence briefs directly to **Slack** and **Email**.

---

## 🌟 Executive Overview

In the fast-moving EdTech sector, growth and performance marketing teams spend hours manually taking screenshots across ad libraries without synthesizing the underlying messaging hooks, course categories, or promotional incentives.

**AdPulse Intelligence** automates this entire competitive intelligence cycle:

1. **Genuine Public Advertisement Collection:** Integrates directly with the **Meta Ad Library API** (`graph.facebook.com/v19.0/ads_archive`) and tracks **Google Ads Transparency Center** creatives across search and visual feeds.
2. **Strict Data Transparency:** Never fabricates fake ad data or synthetic URLs. If an API request fails, it records the exact failure in transparent collection audit logs, retains previously verified data, and clearly flags benchmark data with a `DEMO` badge.
3. **22 EdTech Course Categories:** Multi-label AI classification covering Online Courses, Coding, Software Development, Data Science, AI, JEE Prep, NEET Prep, UPSC, Banking, Government Exams, MBA/CAT, Study Abroad, Bootcamps, Certifications, and Placement Programs.
4. **EdTech Marketing Analysis:** Extracts attention-grabbing marketing hooks, core value propositions (placement support, AIR rank faculty, 1-on-1 mentorship), genuine promotional offers (free masterclasses, scholarship diagnostic tests, EMI options), and audience hypotheses.
5. **Cross-Platform Intelligence (Meta vs Google):** Dedicated cross-channel benchmarking comparing visual social feed creatives (Meta Reels & UGC) against Google Discover (strictly verified placements), Demand Gen, and high-intent Search keywords.
6. **7-Section Weekly AI Intelligence Report:** Generates an executive brief with competitor breakdowns, market messaging trends, creative intelligence, actionable counter-strategies for your marketing team, and direct links to real ads.
7. **Automated Weekly Delivery:** Formatted and dispatched automatically every Monday at 9:00 AM directly into **Slack** (via native Slack Block Kit cards) and **Email** (via responsive HTML newsletters).

---

## 🚀 Monitored EdTech Competitor Brands

By default, the platform monitors 3 core EdTech market leaders:

1. **Physics Wallah (PW)** (`comp-pw`): Affordable competitive exam prep (JEE, NEET, UPSC, SSC), foundational batches, live doubt-clearing, and offline Vidyapeeth centers.
2. **Unacademy** (`comp-unacademy`): Top-tier educators, subscription access, Plus/Iconic mentoring, and national scholarship tests (UNSAT).
3. **Scaler** (`comp-scaler`): High-ticket tech career acceleration, software engineering, Data Science/Machine Learning, 126% avg salary hike positioning, and 1-on-1 mentorship.

> **Fully Customizable:** Users can dynamically add, edit, or swap competitors through the UI to track any EdTech company: **upGrad**, **Simplilearn**, **Great Learning**, **Vedantu**, **Coursera**, **GeeksforGeeks**, **Testbook**, **Adda247**, **Masai**, etc.

---

## 📸 8 Dedicated Platform Views

| View | Operational Capability |
| :--- | :--- |
| **1. Overview** | Executive KPI dashboard: active EdTech brands, total ads vault, top course category, dominant hooks, scheduler status, and latest creatives. |
| **2. Competitors** | Fleet management for PW, Unacademy, Scaler, and custom brands with ads count, promoted categories, single-brand collection trigger, and edit/delete controls. |
| **3. Ad Library** | Comprehensive searchable and filterable creative vault. Filter by brand, 22 course categories, platform, Google placement, offer type, CTA, and `LIVE REAL AD` vs `DEMO` transparency status. |
| **4. Cross-Platform** | Deep-dive Meta Ad Library vs Google Ads comparison. Placement integrity audit (Verified Discover vs Demand Gen vs Search vs Placement Unknown) and side-by-side creative comparison. |
| **5. Creative Insights** | Frequency bars of promoted course categories, dominant marketing hooks, pricing models, value propositions, and messaging opportunities. |
| **6. Intelligence Reports** | The full 7-section weekly AI intelligence digest. Section 1 Executive Summary through Section 7 Source References. One-click Slack & Email dispatch. |
| **7. Automation & Logs** | Weekly cadence configuration (day, time, timezone), manual "Run Scan" trigger, real-time **Collection Logs Table** (strict transparency), and delivery history. |
| **8. Settings & Integrations** | Meta Ad Library API token, Google Ads transparency key, Slack Incoming Webhook (with URL validation and error sanitization), SMTP email configuration, and AI providers. |

---

## ⚡ Quick Start Guide (Under 30 Seconds)

### Step 1: Run the Server
On Windows:
```bash
run.bat
```
*(Or run `python app.py`)*

The server boots at `http://localhost:8000` (zero external dependencies required; powered by Python 3 standard library and SQLite).

### Step 2: Open in Browser
Navigate to:
```
http://localhost:8000
```
The database will automatically initialize, migrate schema tables, and populate initial competitor data and authentic EdTech ads.

### Step 3: Run the Verification Suite
To verify all 14 REST endpoints, cross-platform routes, and background pipeline execution:
```bash
python test_endpoints.py
```

---

## ⚙️ Configuration & Environment Variables

Copy `.env.example` to `.env` or configure directly through the **Settings Modal** in the web dashboard:

```env
# Meta Ad Library API (Graph API v19.0)
META_ACCESS_TOKEN=your_meta_ad_library_access_token_here

# Google Ads Transparency API
GOOGLE_ADS_API_KEY=your_google_api_key_here
GOOGLE_CUSTOMER_ID=your_google_customer_id_here

# Slack Incoming Webhook
# IMPORTANT: Must be an Incoming Webhook starting with https://hooks.slack.com/services/...
SLACK_WEBHOOK_URL=your_slack_incoming_webhook_url_here

# Email SMTP Delivery
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=growth@yourcompany.com
SMTP_PASS=your_app_specific_password
SMTP_FROM="AdPulse Intelligence <growth@yourcompany.com>"
EMAIL_RECIPIENTS=cmo@yourcompany.com,marketing-leads@yourcompany.com

# Weekly Automation Schedule
SCHEDULE_ENABLED=true
SCHEDULE_DAY=monday
SCHEDULE_HOUR=9
SCHEDULE_MINUTE=0
TIMEZONE=Asia/Kolkata

# AI Synthesis Engine (auto, openai, gemini, or built-in local NLP heuristic)
AI_PROVIDER=auto
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AIza...
```

---

## 🛡️ Strict Data Transparency & Collection Integrity

AdPulse enforces strict standards regarding advertising data collection:
- **No Fabricated Data:** If the Meta Ad Library API or Google Transparency Center fails or is unconfigured, the system never creates fake ad IDs, fake copy, or fake URLs.
- **Explicit Error Logging:** Failures are logged directly in the `collection_logs` database table and displayed transparently in the **Automation & Logs** view.
- **Benchmark Distinction:** Initial benchmark reference data is explicitly tagged with `is_demo = 1` and clearly badged as `DEMO` in the UI. Live collected ads from the API or manual verified imports are badged as `LIVE REAL AD`.
- **Verified Placements:** Google Discover is classified strictly when verified through creative feed telemetry; unverified placements are labeled `Google Ad – Placement Unknown` or `Demand Gen`.

---

## 📡 REST API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/competitors` | List active EdTech competitors |
| `POST` | `/api/competitors` | Add or update an EdTech competitor |
| `DELETE` | `/api/competitors/:id` | Remove a competitor |
| `GET` | `/api/ads` | Query ads with category, platform, offer, CTA, and transparency filters |
| `POST` | `/api/ads/collect` | Trigger ad collection across all monitored brands |
| `POST` | `/api/ads/collect-single` | Trigger ad collection for a specific competitor brand |
| `POST` | `/api/ads/import-manual` | Transparent manual import of verified real ad link |
| `GET` | `/api/digests/latest` | Fetch the latest 7-section AI intelligence digest |
| `GET` | `/api/digests` | List historical intelligence digests |
| `POST` | `/api/digests/generate` | Synthesize a new 7-section intelligence report |
| `GET` | `/api/analytics/cross-platform` | Meta vs Google comparative analytics and placement distribution |
| `GET` | `/api/collection-logs` | Transparent audit log of API collection requests |
| `GET` | `/api/stats` | Dashboard KPI metrics |
| `GET` | `/api/scheduler/status` | Current weekly cron state and next execution countdown |
| `POST` | `/api/scheduler/update` | Update cadence day, hour, minute, and enabled status |
| `POST` | `/api/pipeline/run-now` | Execute full end-to-end audit (Collect → Categorize → AI Digest → Dispatch) |
| `POST` | `/api/notifications/slack` | Dispatch latest digest to configured Slack channel |
| `POST` | `/api/notifications/email` | Dispatch latest digest via SMTP HTML newsletter |
| `POST` | `/api/notifications/test-slack` | Send test ping to Slack webhook (with validation) |
| `POST` | `/api/notifications/test-email` | Send test verification email |
| `GET` | `/api/notifications/preview-slack` | Inspect raw Slack Block Kit JSON payload |
| `GET` | `/api/notifications/preview-email` | Inspect responsive HTML newsletter template |

---

## 📄 License & Attribution

Built for growth marketers, performance leads, and product marketing managers in the EdTech ecosystem. Designed with ❤️ for competitive intelligence excellence.
