"""
Database layer for AdPulse Intelligence using SQLite3.
Thread-safe, self-initializing, and auto-migrating.
"""

import sqlite3
import json
import uuid
import re
from datetime import datetime, timedelta
from backend.config import DB_PATH

def get_connection():
    """Returns a new SQLite connection with dict-like row access."""
    conn = sqlite3.connect(str(DB_PATH), timeout=20.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """Initializes tables, indexes, and applies automatic schema migrations."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Competitors Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS competitors (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        domain TEXT,
        industry TEXT DEFAULT 'EdTech',
        logo_url TEXT,
        platforms TEXT, -- JSON array of platforms e.g. ["meta","google"]
        advertiser_ids TEXT, -- JSON: {"meta": "...", "google": "..."}
        active INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Ads Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ads (
        id TEXT PRIMARY KEY,
        ad_id TEXT, -- Real Meta / Google ad ID
        competitor_id TEXT NOT NULL,
        platform TEXT NOT NULL, -- meta | google
        google_placement TEXT DEFAULT 'Google Ad – Placement Unknown',
        is_placement_verified INTEGER DEFAULT 0,
        headline TEXT,
        body_text TEXT NOT NULL,
        description TEXT,
        cta_text TEXT,
        creative_url TEXT,
        media_type TEXT DEFAULT 'image', -- image | video | carousel
        landing_page_url TEXT,
        ad_library_url TEXT,
        course_categories TEXT, -- JSON array of EdTech categories
        marketing_hook TEXT,
        value_proposition TEXT,
        offer_details TEXT,
        audience_hypothesis TEXT,
        creative_strategy TEXT,
        first_seen TEXT DEFAULT CURRENT_TIMESTAMP,
        last_seen TEXT,
        status TEXT DEFAULT 'ACTIVE',
        impressions_range TEXT,
        spend_tier TEXT,
        country_region TEXT DEFAULT 'India',
        source TEXT DEFAULT 'Meta Ad Library API',
        is_demo INTEGER DEFAULT 0, -- 1 for simulated/benchmark, 0 for authentic API
        FOREIGN KEY(competitor_id) REFERENCES competitors(id) ON DELETE CASCADE
    );
    """)

    # 3. Weekly Intelligence Digests Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS digests (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        period_start TEXT,
        period_end TEXT,
        executive_summary TEXT NOT NULL,
        brand_breakdowns TEXT NOT NULL, -- JSON
        macro_themes TEXT NOT NULL,      -- JSON
        counter_strategies TEXT NOT NULL,-- JSON
        cross_platform_intelligence TEXT,-- JSON (Meta vs Google comparison)
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 4. Notification Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notification_logs (
        id TEXT PRIMARY KEY,
        digest_id TEXT,
        channel TEXT NOT NULL, -- slack | email
        recipient TEXT NOT NULL,
        status TEXT NOT NULL, -- SUCCESS | FAILED
        error_message TEXT,
        sent_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 5. Collection Audit Logs Table (Transparent Collection History)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS collection_logs (
        id TEXT PRIMARY KEY,
        competitor_id TEXT,
        competitor_name TEXT,
        platform TEXT NOT NULL,
        status TEXT NOT NULL, -- SUCCESS | FAILED | EMPTY | RATE_LIMITED
        ads_collected INTEGER DEFAULT 0,
        error_message TEXT,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 6. Settings Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    );
    """)

    # Auto-Migration for existing DBs: ensure newly added columns exist in `ads`
    existing_ad_cols = [r["name"] for r in cursor.execute("PRAGMA table_info(ads)").fetchall()]
    new_cols = [
        ("ad_id", "TEXT"),
        ("google_placement", "TEXT DEFAULT 'Google Ad – Placement Unknown'"),
        ("is_placement_verified", "INTEGER DEFAULT 0"),
        ("description", "TEXT"),
        ("ad_library_url", "TEXT"),
        ("course_categories", "TEXT"),
        ("marketing_hook", "TEXT"),
        ("value_proposition", "TEXT"),
        ("offer_details", "TEXT"),
        ("audience_hypothesis", "TEXT"),
        ("creative_strategy", "TEXT"),
        ("last_seen", "TEXT"),
        ("country_region", "TEXT DEFAULT 'India'"),
        ("source", "TEXT DEFAULT 'Meta Ad Library API'"),
        ("is_demo", "INTEGER DEFAULT 0")
    ]
    for col_name, col_def in new_cols:
        if col_name not in existing_ad_cols:
            try:
                cursor.execute(f"ALTER TABLE ads ADD COLUMN {col_name} {col_def}")
            except Exception as e:
                pass

    existing_digest_cols = [r["name"] for r in cursor.execute("PRAGMA table_info(digests)").fetchall()]
    if "cross_platform_intelligence" not in existing_digest_cols:
        try:
            cursor.execute("ALTER TABLE digests ADD COLUMN cross_platform_intelligence TEXT")
        except Exception:
            pass

    existing_comp_cols = [r["name"] for r in cursor.execute("PRAGMA table_info(competitors)").fetchall()]
    if "advertiser_ids" not in existing_comp_cols:
        try:
            cursor.execute("ALTER TABLE competitors ADD COLUMN advertiser_ids TEXT")
        except Exception:
            pass

    # High performance indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ads_competitor ON ads(competitor_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ads_platform ON ads(platform);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ads_first_seen ON ads(first_seen);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ads_is_demo ON ads(is_demo);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ads_google_placement ON ads(google_placement);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_digests_created ON digests(created_at);")

    conn.commit()
    conn.close()

# --- Competitor Operations ---

def get_competitors(active_only=True):
    conn = get_connection()
    query = "SELECT * FROM competitors"
    if active_only:
        query += " WHERE active = 1"
    query += " ORDER BY name ASC"
    rows = conn.execute(query).fetchall()
    conn.close()
    result = []
    for r in rows:
        item = dict(r)
        item["platforms"] = json.loads(item["platforms"]) if item.get("platforms") else ["meta", "google"]
        item["advertiser_ids"] = json.loads(item["advertiser_ids"]) if item.get("advertiser_ids") else {}
        result.append(item)
    return result

def get_competitor_by_id(comp_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM competitors WHERE id = ?", (comp_id,)).fetchone()
    conn.close()
    if not row:
        return None
    item = dict(row)
    item["platforms"] = json.loads(item["platforms"]) if item.get("platforms") else ["meta", "google"]
    item["advertiser_ids"] = json.loads(item["advertiser_ids"]) if item.get("advertiser_ids") else {}
    return item

def upsert_competitor(name, domain=None, industry="EdTech", logo_url=None, platforms=None, advertiser_ids=None, active=1, comp_id=None):
    conn = get_connection()
    if not comp_id:
        existing = conn.execute("SELECT id FROM competitors WHERE name = ?", (name,)).fetchone()
        comp_id = existing["id"] if existing else f"comp-{re.sub(r'[^a-zA-Z0-9]', '', name).lower()[:12]}"

    plat_json = json.dumps(platforms or ["meta", "google"])
    adv_json = json.dumps(advertiser_ids or {})
    conn.execute("""
        INSERT INTO competitors (id, name, domain, industry, logo_url, platforms, advertiser_ids, active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            name=excluded.name,
            domain=excluded.domain,
            industry=excluded.industry,
            logo_url=excluded.logo_url,
            platforms=excluded.platforms,
            advertiser_ids=excluded.advertiser_ids,
            active=excluded.active
    """, (comp_id, name, domain, industry, logo_url, plat_json, adv_json, active))
    conn.commit()
    conn.close()
    return get_competitor_by_id(comp_id)

def delete_competitor(comp_id):
    conn = get_connection()
    conn.execute("DELETE FROM competitors WHERE id = ?", (comp_id,))
    conn.commit()
    conn.close()

# --- Ad Operations ---

def get_ads(competitor_id=None, platform=None, category=None, offer_type=None, cta=None,
            is_demo=None, search=None, limit=100, offset=0):
    conn = get_connection()
    query = """
        SELECT a.*, c.name as competitor_name, c.logo_url as competitor_logo, c.industry as competitor_industry
        FROM ads a
        JOIN competitors c ON a.competitor_id = c.id
        WHERE 1=1
    """
    params = []
    if competitor_id and competitor_id.lower() != 'all':
        query += " AND a.competitor_id = ?"
        params.append(competitor_id)
    if platform and platform.lower() != 'all':
        query += " AND LOWER(a.platform) = ?"
        params.append(platform.lower())
    if category and category.lower() != 'all':
        query += " AND a.course_categories LIKE ?"
        params.append(f"%{category}%")
    if offer_type and offer_type.lower() != 'all':
        query += " AND a.offer_details LIKE ?"
        params.append(f"%{offer_type}%")
    if cta and cta.lower() != 'all':
        query += " AND LOWER(a.cta_text) = ?"
        params.append(cta.lower())
    if is_demo is not None:
        query += " AND a.is_demo = ?"
        params.append(int(is_demo))
    if search:
        query += " AND (a.headline LIKE ? OR a.body_text LIKE ? OR a.description LIKE ? OR a.marketing_hook LIKE ? OR a.course_categories LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term, term, term, term])

    query += " ORDER BY a.first_seen DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    rows = conn.execute(query, params).fetchall()
    conn.close()
    result = []
    for r in rows:
        item = dict(r)
        if item.get("course_categories"):
            try:
                item["course_categories"] = json.loads(item["course_categories"])
            except Exception:
                item["course_categories"] = [item["course_categories"]]
        else:
            item["course_categories"] = ["Online Courses"]
        result.append(item)
    return result

def insert_ad(competitor_id, platform, body_text, headline=None, description=None,
              cta_text=None, creative_url=None, media_type="image", landing_page_url=None,
              ad_library_url=None, google_placement="Google Ad – Placement Unknown",
              is_placement_verified=0, course_categories=None, marketing_hook=None,
              value_proposition=None, offer_details=None, audience_hypothesis=None,
              creative_strategy=None, first_seen=None, last_seen=None, status="ACTIVE",
              impressions_range=None, spend_tier=None, country_region="India",
              source="Meta Ad Library API", is_demo=0, ad_id=None):
    conn = get_connection()
    if not ad_id:
        ad_id = str(uuid.uuid4())[:12]
    if not first_seen:
        first_seen = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cat_json = json.dumps(course_categories or ["Online Courses"])

    conn.execute("""
        INSERT OR REPLACE INTO ads (
            id, ad_id, competitor_id, platform, google_placement, is_placement_verified,
            headline, body_text, description, cta_text, creative_url, media_type,
            landing_page_url, ad_library_url, course_categories, marketing_hook,
            value_proposition, offer_details, audience_hypothesis, creative_strategy,
            first_seen, last_seen, status, impressions_range, spend_tier,
            country_region, source, is_demo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ad_id, ad_id, competitor_id, platform, google_placement, int(is_placement_verified),
        headline, body_text, description, cta_text, creative_url, media_type,
        landing_page_url, ad_library_url, cat_json, marketing_hook,
        value_proposition, offer_details, audience_hypothesis, creative_strategy,
        first_seen, last_seen, status, impressions_range, spend_tier,
        country_region, source, int(is_demo)
    ))
    conn.commit()
    conn.close()
    return ad_id

def save_ad(ad_dict):
    """Convenience dictionary wrapper around insert_ad."""
    return insert_ad(
        competitor_id=ad_dict.get("competitor_id"),
        platform=ad_dict.get("platform", "meta"),
        body_text=ad_dict.get("body_text", ""),
        headline=ad_dict.get("headline"),
        description=ad_dict.get("description"),
        cta_text=ad_dict.get("cta_text"),
        creative_url=ad_dict.get("creative_url"),
        media_type=ad_dict.get("media_type", "image"),
        landing_page_url=ad_dict.get("landing_page_url"),
        ad_library_url=ad_dict.get("ad_library_url"),
        google_placement=ad_dict.get("google_placement", "Google Ad – Placement Unknown"),
        is_placement_verified=ad_dict.get("is_placement_verified", 0),
        course_categories=ad_dict.get("course_categories"),
        marketing_hook=ad_dict.get("marketing_hook"),
        value_proposition=ad_dict.get("value_proposition"),
        offer_details=ad_dict.get("offer_details"),
        audience_hypothesis=ad_dict.get("audience_hypothesis"),
        creative_strategy=ad_dict.get("creative_strategy"),
        first_seen=ad_dict.get("first_seen"),
        last_seen=ad_dict.get("last_seen"),
        status=ad_dict.get("status", "ACTIVE"),
        impressions_range=ad_dict.get("impressions_range"),
        spend_tier=ad_dict.get("spend_tier"),
        country_region=ad_dict.get("country_region", "India"),
        source=ad_dict.get("source", "manual_import"),
        is_demo=ad_dict.get("is_demo", 0),
        ad_id=ad_dict.get("ad_id") or ad_dict.get("external_ad_id")
    )

def get_recent_ads_for_competitors(days=7):
    conn = get_connection()
    rows = conn.execute("""
        SELECT a.*, c.name as competitor_name, c.logo_url as competitor_logo, c.industry as competitor_industry
        FROM ads a
        JOIN competitors c ON a.competitor_id = c.id
        WHERE c.active = 1
        ORDER BY a.first_seen DESC
    """).fetchall()
    conn.close()
    result = []
    for r in rows:
        item = dict(r)
        if item.get("course_categories"):
            try:
                item["course_categories"] = json.loads(item["course_categories"])
            except Exception:
                item["course_categories"] = [item["course_categories"]]
        result.append(item)
    return result

# --- Digest Operations ---

def save_digest(title, period_start, period_end, executive_summary,
                brand_breakdowns, macro_themes, counter_strategies,
                cross_platform_intelligence=None, digest_id=None):
    conn = get_connection()
    if not digest_id:
        digest_id = str(uuid.uuid4())[:8]

    conn.execute("""
        INSERT INTO digests (
            id, title, period_start, period_end, executive_summary,
            brand_breakdowns, macro_themes, counter_strategies, cross_platform_intelligence
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        digest_id, title, period_start, period_end, executive_summary,
        json.dumps(brand_breakdowns),
        json.dumps(macro_themes),
        json.dumps(counter_strategies),
        json.dumps(cross_platform_intelligence or {})
    ))
    conn.commit()
    conn.close()
    return get_digest_by_id(digest_id)

def get_latest_digest():
    conn = get_connection()
    row = conn.execute("SELECT * FROM digests ORDER BY created_at DESC LIMIT 1").fetchone()
    conn.close()
    if not row:
        return None
    return parse_digest_row(row)

def get_digest_by_id(digest_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM digests WHERE id = ?", (digest_id,)).fetchone()
    conn.close()
    if not row:
        return None
    return parse_digest_row(row)

def get_all_digests(limit=20):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM digests ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [parse_digest_row(r) for r in rows]

def parse_digest_row(row):
    item = dict(row)
    for field in ["brand_breakdowns", "macro_themes", "counter_strategies", "cross_platform_intelligence"]:
        if item.get(field):
            try:
                item[field] = json.loads(item[field])
            except Exception:
                item[field] = [] if field != "cross_platform_intelligence" else {}

    # Ensure brand_breakdowns includes recent ads spotted
    if item.get("brand_breakdowns"):
        conn = get_connection()
        for b in item["brand_breakdowns"]:
            if not b.get("recent_ads") and b.get("competitor_id"):
                c_ads = conn.execute("""
                    SELECT id, headline, body_text, platform, google_placement, is_placement_verified,
                           media_type, cta_text, creative_url, first_seen, impressions_range,
                           spend_tier, landing_page_url, ad_library_url, is_demo, course_categories
                    FROM ads
                    WHERE competitor_id = ?
                    ORDER BY first_seen DESC
                    LIMIT 3
                """, (b["competitor_id"],)).fetchall()
                b["recent_ads"] = []
                for a in c_ads:
                    ad_dict = dict(a)
                    if ad_dict.get("course_categories"):
                        try:
                            ad_dict["course_categories"] = json.loads(ad_dict["course_categories"])
                        except Exception:
                            ad_dict["course_categories"] = []
                    b["recent_ads"].append(ad_dict)
        conn.close()

    return item

# --- Collection Audit Logs ---

def log_collection(platform, status, competitor_id=None, competitor_name=None, ads_collected=0, error_message=None):
    conn = get_connection()
    log_id = str(uuid.uuid4())[:12]
    conn.execute("""
        INSERT INTO collection_logs (id, competitor_id, competitor_name, platform, status, ads_collected, error_message)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (log_id, competitor_id, competitor_name, platform, status, ads_collected, error_message))
    conn.commit()
    conn.close()
    return log_id

def get_collection_logs(limit=25):
    conn = get_connection()
    rows = conn.execute("""
        SELECT * FROM collection_logs ORDER BY timestamp DESC LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

# --- Notification Logs ---

def log_notification(channel, recipient, status, digest_id=None, error_message=None):
    conn = get_connection()
    log_id = str(uuid.uuid4())[:12]
    conn.execute("""
        INSERT INTO notification_logs (id, digest_id, channel, recipient, status, error_message)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (log_id, digest_id, channel, recipient, status, error_message))
    conn.commit()
    conn.close()
    return log_id

def get_notification_logs(limit=25):
    conn = get_connection()
    rows = conn.execute("""
        SELECT * FROM notification_logs ORDER BY sent_at DESC LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

# --- Settings Operations ---

def get_setting(key, default=None):
    conn = get_connection()
    row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    conn.close()
    return row["value"] if row else default

def set_setting(key, value):
    conn = get_connection()
    conn.execute("""
        INSERT INTO settings (key, value) VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
    """, (key, str(value)))
    conn.commit()
    conn.close()

def get_all_settings():
    conn = get_connection()
    rows = conn.execute("SELECT key, value FROM settings").fetchall()
    conn.close()
    # Mask secret tokens for security
    data = {}
    for r in rows:
        k, v = r["key"], r["value"]
        if "key" in k.lower() or "token" in k.lower() or "pass" in k.lower() or "secret" in k.lower():
            data[k] = v[:4] + "••••••••" if len(v) > 6 else ("••••" if v else "")
            data[f"_{k}_configured"] = bool(v)
        else:
            data[k] = v
    return data

# --- Cross-Platform Intelligence (Meta vs Google Analytics) ---

def get_cross_platform_analytics():
    """
    Analyzes Meta vs Google advertising for all active EdTech competitors.
    Returns:
    - Platform ad counts & shares
    - Verified Discover vs Demand Gen vs Display vs Search vs Unknown Google placements
    - Course category breakdown per platform
    - Hook, offer, and CTA comparison
    - Side-by-side ad comparison pairs
    """
    conn = get_connection()
    ads_rows = conn.execute("""
        SELECT a.*, c.name as competitor_name, c.logo_url as competitor_logo
        FROM ads a
        JOIN competitors c ON a.competitor_id = c.id
        WHERE c.active = 1
        ORDER BY a.first_seen DESC
    """).fetchall()
    conn.close()

    meta_ads = []
    google_ads = []
    google_placements = {
        "Google Discover": 0,
        "Demand Gen": 0,
        "YouTube": 0,
        "Display": 0,
        "Search": 0,
        "Google Ad – Placement Unknown": 0
    }

    meta_categories = {}
    google_categories = {}
    meta_ctas = {}
    google_ctas = {}
    meta_offers = {}
    google_offers = {}
    meta_hooks = []
    google_hooks = []

    for row in ads_rows:
        ad = dict(row)
        raw_cats = ad.get("course_categories")
        if raw_cats:
            if isinstance(raw_cats, str):
                ad["course_categories"] = [c.strip() for c in raw_cats.split(",") if c.strip()]
            elif isinstance(raw_cats, list):
                ad["course_categories"] = raw_cats
            else:
                ad["course_categories"] = ["Online Courses"]
        else:
            ad["course_categories"] = ["Online Courses"]

        plat = ad.get("platform", "meta").lower()
        if plat == "google":
            google_ads.append(ad)
            placement = ad.get("google_placement") or "Google Ad – Placement Unknown"
            google_placements[placement] = google_placements.get(placement, 0) + 1

            for cat in ad.get("course_categories") or ["Online Courses"]:
                google_categories[cat] = google_categories.get(cat, 0) + 1
            if ad.get("cta_text"):
                google_ctas[ad["cta_text"]] = google_ctas.get(ad["cta_text"], 0) + 1
            if ad.get("offer_details") and ad.get("offer_details") != "None":
                google_offers[ad["offer_details"]] = google_offers.get(ad["offer_details"], 0) + 1
            if ad.get("marketing_hook"):
                google_hooks.append({"brand": ad["competitor_name"], "hook": ad["marketing_hook"]})
        else:
            meta_ads.append(ad)
            for cat in ad.get("course_categories") or ["Online Courses"]:
                meta_categories[cat] = meta_categories.get(cat, 0) + 1
            if ad.get("cta_text"):
                meta_ctas[ad["cta_text"]] = meta_ctas.get(ad["cta_text"], 0) + 1
            if ad.get("offer_details") and ad.get("offer_details") != "None":
                meta_offers[ad["offer_details"]] = meta_offers.get(ad["offer_details"], 0) + 1
            if ad.get("marketing_hook"):
                meta_hooks.append({"brand": ad["competitor_name"], "hook": ad["marketing_hook"]})

    # Side-by-side ad comparison pairs for the same competitors
    comparison_pairs = []
    comps = get_competitors(active_only=True)
    for c in comps:
        c_meta = [a for a in meta_ads if a["competitor_id"] == c["id"]]
        c_google = [a for a in google_ads if a["competitor_id"] == c["id"]]
        if c_meta and c_google:
            comparison_pairs.append({
                "competitor_name": c["name"],
                "competitor_logo": c.get("logo_url"),
                "meta_ad": c_meta[0],
                "google_ad": c_google[0]
            })

    return {
        "totals": {
            "total_meta_ads": len(meta_ads),
            "total_google_ads": len(google_ads),
            "verified_discover_ads": google_placements.get("Google Discover", 0),
            "demand_gen_ads": google_placements.get("Demand Gen", 0),
            "unknown_placement_ads": google_placements.get("Google Ad – Placement Unknown", 0),
            "total_ads_compared": len(meta_ads) + len(google_ads)
        },
        "google_placements": google_placements,
        "category_comparison": {
            "meta": meta_categories,
            "google": google_categories
        },
        "cta_comparison": {
            "meta": meta_ctas,
            "google": google_ctas
        },
        "offer_comparison": {
            "meta": meta_offers,
            "google": google_offers
        },
        "hooks_sample": {
            "meta": meta_hooks[:6],
            "google": google_hooks[:6]
        },
        "comparison_pairs": comparison_pairs
    }

# --- Dashboard & Reach Stats ---

def get_dashboard_stats():
    conn = get_connection()
    total_competitors = conn.execute("SELECT COUNT(*) as c FROM competitors WHERE active = 1").fetchone()["c"]
    total_ads = conn.execute("SELECT COUNT(*) as c FROM ads").fetchone()["c"]
    total_digests = conn.execute("SELECT COUNT(*) as c FROM digests").fetchone()["c"]

    # New ads in the past 7 days
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
    new_ads_week = conn.execute("SELECT COUNT(*) as c FROM ads WHERE first_seen >= ?", (seven_days_ago,)).fetchone()["c"]

    # Last collection status
    last_log = conn.execute("SELECT * FROM collection_logs ORDER BY timestamp DESC LIMIT 1").fetchone()
    last_collection_status = dict(last_log) if last_log else {"status": "SUCCESS", "timestamp": "Initial sync ready"}

    # Platform distribution
    platform_rows = conn.execute("SELECT platform, COUNT(*) as c FROM ads GROUP BY platform").fetchall()
    platform_dist = {r["platform"]: r["c"] for r in platform_rows}

    # Brand ad counts
    brand_rows = conn.execute("""
        SELECT c.id, c.name, c.logo_url, c.industry, COUNT(a.id) as count
        FROM competitors c
        LEFT JOIN ads a ON c.id = a.competitor_id
        WHERE c.active = 1
        GROUP BY c.id
    """).fetchall()
    brand_counts = [dict(r) for r in brand_rows]

    conn.close()
    return {
        "total_competitors": total_competitors,
        "total_ads": total_ads,
        "new_ads_week": new_ads_week,
        "total_digests": total_digests,
        "last_collection": last_collection_status,
        "platform_distribution": platform_dist,
        "brand_counts": brand_counts
    }
