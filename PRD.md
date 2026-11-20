# Product Requirements Document (PRD)

## Project: Competitor Ad Tracker & Intelligence Engine
**Document Version:** 1.0.0  
**Status:** Approved for Implementation  
**Target Delivery:** Production-Ready MVP & Enterprise Extensible  
**Owner:** Growth & Marketing Engineering  

---

## 1. Executive Summary & Problem Statement

### 1.1 Executive Summary
The **Competitor Ad Tracker** is an automated intelligence platform designed for growth marketers, product strategists, and brand leaders. Every week, the system automatically collects active ad creatives and copy from 3 primary competitor brands across major digital channels (Meta, Google, TikTok, LinkedIn), synthesizes what competitors are messaging through an AI summarization engine, and delivers an executive brief directly to the team's Slack channel or Email inbox.

The platform provides a consumer-grade, premium web dashboard where marketing teams can visually explore competitor ad creatives, search historical copy, inspect creative formats, review AI-synthesized battle cards, and trigger on-demand market audits.

### 1.2 The Problem
1. **Manual Ad Reconnaissance is Tedious & Scattered:** Marketers waste 4–8 hours weekly manually searching Meta Ad Library, Google Ads Transparency Center, and TikTok Creative Center to see what competitors are launching.
2. **Data Without Synthesis:** Even when ads are gathered in spreadsheets or screenshots, teams lack structured synthesis of what competitors are actually saying (e.g., Are they discounting heavily? Testing fear-of-missing-out hooks? Pivoting to video UGC? Highlighting enterprise compliance?).
3. **Information Silos:** Ad insights remain stuck with individual media buyers and never reach product managers, copywriters, or executives who need to counter competitor positioning in real time.
4. **Lack of Automated Delivery:** Without scheduled weekly briefings pushed to Slack or Email, competitor tracking falls off the priority list after a few weeks.

### 1.3 The Solution
An end-to-end automated platform that:
- Runs continuous or weekly scheduled ingestions of competitor ad creatives.
- Employs an AI intelligence engine to decode core messaging themes, promotional offers, emotional angles, and creative distribution.
- Formats actionable briefs into native Slack Block Kit cards and responsive HTML email digests.
- Provides an intuitive, high-end web dashboard requiring zero technical expertise for day-to-day users.

---

## 2. Target Personas & Use Cases

| Persona | Role | Core Need | Key Value Obtained |
| :--- | :--- | :--- | :--- |
| **Growth Lead / Media Buyer** | Paid Ads & Acquisition | Identify high-performing hooks, formats (UGC vs carousel), and promotional offers. | Steal winning creative angles, spot competitor budget surges, prevent ad fatigue. |
| **Product Marketing Manager (PMM)** | Positioning & Messaging | Monitor competitor value propositions and claims. | Adjust counter-messaging, landing page copy, and battlecards before losing market share. |
| **Marketing Executive / CMO** | Strategic Leadership | High-level summary of competitor market positioning without getting bogged down in pixels. | Weekly Slack/Email briefing with actionable counter-strategies. |
| **Solo Founder / Startup Operator** | All-in-One Marketer | Fast, automated tracking of 3 key incumbents with zero setup friction. | Set-and-forget weekly automated intelligence. |

---

## 3. Goals & Success Metrics

### 3.1 Primary Goals
1. **Zero-Friction Operation:** Non-technical marketing staff can track 3 competitors and receive weekly digests without touching code or running complex servers.
2. **Actionable Insights:** AI summaries must extract real strategic intelligence (hooks, offers, angles, recommendations), not just regurgitate raw copy.
3. **Multi-Channel Delivery:** Seamless notifications directly into company communication hubs (Slack channels and Email inboxes).
4. **Visual Ad Vault:** An interactive visual library of competitor creatives with filterable metadata.

### 3.2 Success Metrics (KPIs)
- **Time Saved:** Reduce weekly competitive audit time from 6 hours to < 5 minutes.
- **Delivery Reliability:** > 99% scheduled digest delivery rate to Slack and Email.
- **Engagement Rate:** > 80% open/click-through rate on weekly Slack and Email briefs.
- **Setup Time:** Under 3 minutes for a new user from git clone to first live digest.

---

## 4. System Architecture & Information Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                        COMPETITOR AD TRACKER                          │
└────────────────────────────────────────────────────────────────────────┘
                                    │
    ┌───────────────────────────────┴───────────────────────────────┐
    ▼                                                               ▼
┌─────────────────────────────────┐               ┌─────────────────────────────────┐
│     FRONTEND APPLICATION        │               │         PYTHON BACKEND          │
│  (Modern Premium SPA / HTML5)   │               │   (REST API + Background Engine)│
│                                 │               │                                 │
│  • Executive Digest View        │   HTTP / JSON │  • Ad Ingestion & Web Scraper   │
│  • Interactive Ad Vault         │ ◄───────────► │  • AI Intelligence Summarizer   │
│  • Competitor Brand Manager     │               │  • APScheduler (Weekly Cron)    │
│  • Slack / Email Previewer      │               │  • Slack Block Kit Dispatcher   │
│  • Settings & Scheduler Modal   │               │  • SMTP Responsive Email Engine │
└─────────────────────────────────┘               │  • SQLite Storage & Analytics   │
                                                  └─────────────────────────────────┘
                                                                   │
                                  ┌────────────────────────────────┴────────────────┐
                                  ▼                                                 ▼
                    ┌───────────────────────────┐                     ┌───────────────────────────┐
                    │      SLACK WORKSPACE      │                     │        EMAIL INBOX        │
                    │   (Incoming Webhook /     │                     │  (HTML Weekly Digest via  │
                    │    Block Kit Cards)       │                     │    SMTP / SendGrid)       │
                    └───────────────────────────┘                     └───────────────────────────┘
```

---

## 5. Functional Requirements (FR)

### FR-1: Competitor Brand Management
- **FR-1.1 Default 3-Competitor Slot:** The system comes pre-configured with 3 active competitors (e.g. Nike, Gymshark, Lululemon or customizable to any SaaS/eCommerce brand).
- **FR-1.2 CRUD Competitors:** Users can add new competitors, edit existing ones (Brand Name, Domain, Industry, Logo URL), or deactivate competitors.
- **FR-1.3 Multi-Platform Tracking:** For each competitor, users can toggle which platforms to monitor (Meta / Instagram, Google Ads, TikTok, LinkedIn).

### FR-2: Ad Collection & Creative Ingestion Engine
- **FR-2.1 Scheduled Weekly Ingestion:** Automatically ingests new ads on a configured weekly cadence (e.g., Every Monday at 09:00 AM).
- **FR-2.2 On-Demand Ingestion:** Users can click "Fetch Fresh Ads" or "Run Pipeline Now" to trigger an instant ad crawl.
- **FR-2.3 Ad Creative Data Model:** Ingests and stores:
  - Brand Name & Logo
  - Advertising Channel (Meta, Google, TikTok, LinkedIn)
  - Primary Ad Copy & Headline
  - Call-To-Action (CTA) label (e.g., "Shop Now", "Claim 50% Off", "Start Free Trial")
  - Media Format (Static Image, Short Video, Carousel)
  - Creative Asset Preview URL / Visual Thumbnail
  - Landing Page Destination URL
  - Estimated Impressions / Spend Tier
  - Date First Detected & Active Status
- **FR-2.4 Meta Ad Library API & Fallback Scraper:** Supports official Meta Graph API token when configured; otherwise falls back gracefully to a robust multi-source ad scraper / simulation engine that generates industry-accurate, realistic ad campaigns so the app is always 100% operational.

### FR-3: AI-Powered Weekly Intelligence & Summarization Engine
- **FR-3.1 Automated Synthesis:** Analyzes all ads collected across the 3 competitor brands over the past 7 days.
- **FR-3.2 Structured Output:**
  - **Executive Summary:** 2–3 sentence executive synopsis of competitor movements.
  - **Brand-by-Brand Breakdown:**
    - Primary Messaging Angle & Narrative.
    - Active Offers, Discounts & Pricing Incentives (e.g. "Buy 1 Get 1", "Save 25%").
    - Dominant Hooks & Emotional Triggers (Urgency, Social Proof, FOMO, Aspiration).
    - Creative Formats & Asset Allocation (% Video vs % Image vs % Carousel).
  - **Macro Market Themes:** Cross-brand trends (e.g. "Competitors are aggressively pushing seasonal winter clearance with bundle discounts").
  - **Actionable Counter-Strategies:** 3 concrete tactics our brand can execute to exploit competitor messaging gaps.
- **FR-3.3 Dual AI Modes:**
  - **Online Mode:** Connects to OpenAI (GPT-4o/GPT-3.5) or Google Gemini API via `.env`.
  - **Smart Offline NLP Mode:** Integrated rule-based heuristic NLP engine (analyzing regex patterns, sentiment, keywords, CTA verbs, price tags) that operates with zero API keys or costs.

### FR-4: Multi-Channel Notification Engine
- **FR-4.1 Slack Integration:**
  - Posts using Slack Incoming Webhook URLs.
  - Employs Slack Block Kit formatting: visual banner headers, stat section blocks, brand callouts, bulleted takeaways, and a direct button linking to the web dashboard.
  - Includes a "Test Webhook" button in the UI for instant connectivity check.
- **FR-4.2 Email Integration:**
  - Delivers a responsive, beautifully styled HTML email newsletter digest via standard SMTP (Gmail, Outlook, Amazon SES, SendGrid, Mailgun).
  - Works on both desktop and mobile email clients with dark/light mode compatibility.
  - Includes a "Send Test Email" button in the UI.
- **FR-4.3 Interactive Previews:** The UI provides real-time preview modals for both Slack messages and HTML emails before dispatch.

### FR-5: Automated Weekly Scheduling & Background Jobs
- **FR-5.1 Configurable Cadence:** Default weekly execution (Every Monday at 09:00 AM local time).
- **FR-5.2 Background Thread Execution:** Runs asynchronously using Python background scheduler without blocking API requests.
- **FR-5.3 Audit Log:** Logs every scheduled execution, count of ads scraped, digest generated, and delivery status (success/failure timestamp).

### FR-6: Premium Web Dashboard (Frontend)
- **FR-6.1 Visual Aesthetics:** Premium dark-mode default with luxury glassmorphism, glowing accents, polished micro-interactions, responsive grid layout, and toggleable clean light mode.
- **FR-6.2 Key Views:**
  1. **Top Control Bar:** System status pill, countdown to next scheduled weekly run, "Run Pipeline Now" trigger, Settings button.
  2. **Executive KPI Cards:** Active competitors, total ads collected this week, dominant creative format, active notification channels.
  3. **Weekly Digest Hub:** Displays the latest generated AI briefing, brand-by-brand comparison cards, counter-strategy recommendations, and one-click dispatch triggers.
  4. **Ad Vault & Creative Explorer:** Filterable grid with search bar, competitor filter chips, platform icons, media format filters, and detailed ad view.
  5. **Competitor Brand Manager:** View and update the 3 tracked competitor brands.
  6. **Settings & Integration Modal:** Configure Slack webhook URL, SMTP credentials, schedule day/time, and AI engine preferences.

---

## 6. Non-Functional Requirements (NFR)

1. **Zero-Config Dependency Barrier:** Built using standard Python 3 capabilities so non-technical users can launch with a single command without encountering compilation or version compatibility errors.
2. **Speed & Latency:** Dashboard page load < 500ms; Ad filtering and search instant (< 50ms); Digest generation < 3s.
3. **Data Persistence:** All competitors, ads, digests, and settings are stored locally in an atomic SQLite database (`data/ad_tracker.db`).
4. **Security & Privacy:** API keys, webhook URLs, and SMTP passwords are kept local, never sent to external telemetry servers.
5. **Cross-Platform Compatibility:** Runs seamlessly on Windows 10/11, macOS, and Linux.

---

## 7. Data Models (Schema)

```sql
-- Competitor Brands
CREATE TABLE competitors (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    domain TEXT,
    industry TEXT,
    logo_url TEXT,
    platforms TEXT, -- JSON array: ["meta", "google", "tiktok"]
    active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ingested Ads
CREATE TABLE ads (
    id TEXT PRIMARY KEY,
    competitor_id TEXT NOT NULL,
    platform TEXT NOT NULL, -- meta | google | tiktok | linkedin
    headline TEXT,
    body_text TEXT NOT NULL,
    cta_text TEXT,
    creative_url TEXT,
    media_type TEXT DEFAULT 'image', -- image | video | carousel
    landing_page_url TEXT,
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'ACTIVE',
    impressions_range TEXT,
    spend_tier TEXT,
    FOREIGN KEY(competitor_id) REFERENCES competitors(id)
);

-- Weekly AI Digests
CREATE TABLE digests (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    period_start DATE,
    period_end DATE,
    executive_summary TEXT NOT NULL,
    brand_breakdowns TEXT NOT NULL, -- JSON
    macro_themes TEXT NOT NULL,      -- JSON
    counter_strategies TEXT NOT NULL,-- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Notification Audit Logs
CREATE TABLE notification_logs (
    id TEXT PRIMARY KEY,
    digest_id TEXT,
    channel TEXT NOT NULL, -- slack | email
    recipient TEXT NOT NULL,
    status TEXT NOT NULL, -- SUCCESS | FAILED
    error_message TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Application Settings
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
```

---

## 8. Release Milestones & Implementation Plan

- **Phase 1 (Database & Models):** SQLite setup, tables, seeding script with 3 default competitor brands and authentic ad library data.
- **Phase 2 (Ad Collector & AI Summarizer):** Multi-platform ad scraper engine, intelligent NLP & LLM synthesis engine.
- **Phase 3 (Notifier & Scheduler):** Slack Block Kit payload generator, SMTP responsive HTML email dispatcher, background scheduler.
- **Phase 4 (Backend REST API):** Python HTTP server with full JSON REST API, static asset server, and error handling.
- **Phase 5 (Frontend UI):** High-end glassmorphism dashboard, reactive state controller, modals, Ad Vault, and notification previewers.
- **Phase 6 (Documentation & Polish):** Production README, quickstart scripts (`run.bat`, `run.sh`), verification and automated testing.
