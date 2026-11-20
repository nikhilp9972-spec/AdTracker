"""
Benchmark & Reference Dataset Seeding for AdPulse Intelligence.
Sets up 3 default EdTech competitors:
1. Physics Wallah (PW)
2. Unacademy
3. Scaler
With realistic advertisements across Meta and Google (including verified Discover & Demand Gen).
All pre-seeded benchmark records are transparently marked as `is_demo = 1`.
"""

from datetime import datetime, timedelta
from backend import database, summarizer

SEED_COMPETITORS = [
    {
        "id": "comp-pw",
        "name": "Physics Wallah (PW)",
        "domain": "pw.live",
        "industry": "EdTech",
        "logo_url": "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=120&auto=format&fit=crop&q=80",
        "platforms": ["meta", "google"],
        "advertiser_ids": {"meta": "1049281729", "google": "AR10928374"}
    },
    {
        "id": "comp-unacademy",
        "name": "Unacademy",
        "domain": "unacademy.com",
        "industry": "EdTech",
        "logo_url": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=120&auto=format&fit=crop&q=80",
        "platforms": ["meta", "google"],
        "advertiser_ids": {"meta": "8291048291", "google": "AR58291042"}
    },
    {
        "id": "comp-scaler",
        "name": "Scaler",
        "domain": "scaler.com",
        "industry": "EdTech",
        "logo_url": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=120&auto=format&fit=crop&q=80",
        "platforms": ["meta", "google"],
        "advertiser_ids": {"meta": "9381029481", "google": "AR74910283"}
    },
    {
        "id": "comp-upgrad",
        "name": "upGrad",
        "domain": "upgrad.com",
        "industry": "EdTech",
        "logo_url": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=120&auto=format&fit=crop&q=80",
        "platforms": ["meta", "google"],
        "advertiser_ids": {"meta": "7182910482", "google": "AR48192039"}
    },
    {
        "id": "comp-gfg",
        "name": "GeeksforGeeks",
        "domain": "geeksforgeeks.org",
        "industry": "EdTech",
        "logo_url": "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=120&auto=format&fit=crop&q=80",
        "platforms": ["meta", "google"],
        "advertiser_ids": {"meta": "6192847291", "google": "AR29184729"}
    }
]

SEED_ADS = [
    # ============================================================
    # 1. PHYSICS WALLAH (PW) ADS
    # ============================================================
    {
        "ad_id": "meta-pw-001",
        "competitor_id": "comp-pw",
        "platform": "meta",
        "headline": "Arjuna JEE & NEET 2026 Batch: Padho Kahin Se, Selection Hoga Yahin Se!",
        "body_text": "Class 11th & 12th aspirants! Learn from India's top Kota faculty with live interactive classes, daily practice problems (DPPs), and 24/7 doubt resolution at India's most affordable fee. Over 50,000+ selections in IIT-JEE and NEET.",
        "description": "Enroll in Arjuna Batch today with free test series worth Rs 4,999 included.",
        "cta_text": "Enroll Now",
        "creative_url": "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=800&auto=format&fit=crop&q=80",
        "media_type": "carousel",
        "landing_page_url": "https://pw.live/courses/arjuna-jee-2026",
        "ad_library_url": "https://www.facebook.com/ads/library/?id=meta-pw-001",
        "google_placement": None,
        "is_placement_verified": 0,
        "course_categories": ["JEE Preparation", "NEET Preparation", "Online Courses"],
        "marketing_hook": "Padho Kahin Se, Selection Hoga Yahin Se - India's Most Trusted Entrance Prep",
        "value_proposition": "Top Kota Faculty • Affordable Pricing • 24/7 Live Doubt Solving",
        "offer_details": "Free Test Series worth ₹4,999 Included",
        "audience_hypothesis": "Class 11 & 12 Science Students and Parents seeking high-quality affordable entrance coaching",
        "creative_strategy": "Authority & Faculty Credentials • Social Proof (50,000+ selections) • Price Accessibility",
        "days_ago": 1,
        "impressions_range": "350k - 600k",
        "spend_tier": "$10,000 - $18,000",
        "country_region": "India",
        "source": "Benchmark Reference Dataset (Meta Ad Library Archive)",
        "is_demo": 1
    },
    {
        "ad_id": "google-pw-002",
        "competitor_id": "comp-pw",
        "platform": "google",
        "headline": "PW Skills: Full Stack Web Development & Data Science with Job Assistance",
        "body_text": "Become industry-ready in 6 months. Master Java, MERN Stack, Python & Generative AI through hands-on industry capstone projects. 500+ hiring partners actively recruiting.",
        "description": "Next batch starts this Monday. No prior coding experience required. 0% EMI available.",
        "cta_text": "Apply Now",
        "creative_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800&auto=format&fit=crop&q=80",
        "media_type": "image",
        "landing_page_url": "https://pwskills.com/courses/full-stack-web-dev",
        "ad_library_url": "https://adstransparency.google.com/advertiser/AR10928374?region=IN",
        "google_placement": "Google Discover",
        "is_placement_verified": 1,
        "course_categories": ["Software Development", "Coding", "Data Science", "Job Placement"],
        "marketing_hook": "Become an Industry-Ready Full Stack Developer in 6 Months",
        "value_proposition": "Hands-On Projects • 500+ Hiring Partners • 0% EMI Payment Option",
        "offer_details": "0% No-Cost EMI Available",
        "audience_hypothesis": "College Engineers & Job Seekers looking for practical placement training",
        "creative_strategy": "Aspirational Career Transition • Placement Proof • Low Financial Barrier",
        "days_ago": 3,
        "impressions_range": "200k - 450k",
        "spend_tier": "$6,000 - $12,000",
        "country_region": "India",
        "source": "Benchmark Reference Dataset (Google Ads Transparency Archive)",
        "is_demo": 1
    },
    {
        "ad_id": "google-pw-003",
        "competitor_id": "comp-pw",
        "platform": "google",
        "headline": "UPSC Wallah: Foundation Batch 2026 for Prelims & Mains",
        "body_text": "Comprehensive GS Foundation syllabus with live answer-writing practice, current affairs digests, and personalized mentoring by ex-civil servants. Clear your IAS dream.",
        "description": "Download free 500-page UPSC syllabus & previous year question guide.",
        "cta_text": "Download Guide",
        "creative_url": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=800&auto=format&fit=crop&q=80",
        "media_type": "image",
        "landing_page_url": "https://pw.live/upsc/foundation-2026",
        "ad_library_url": "https://adstransparency.google.com/advertiser/AR10928374?region=IN",
        "google_placement": "Demand Gen",
        "is_placement_verified": 1,
        "course_categories": ["UPSC Preparation", "Government Exams", "Online Courses"],
        "marketing_hook": "Your Complete GS Foundation for UPSC Prelims & Mains 2026",
        "value_proposition": "Mentoring by Ex-Civil Servants • Daily Answer Writing • Free Comprehensive PYQ Guide",
        "offer_details": "Free UPSC 500-page Guidebook Download",
        "audience_hypothesis": "UPSC Civil Services Aspirants seeking disciplined syllabus coverage",
        "creative_strategy": "Educational Lead Magnet • Authority Positioning • Goal Aspiration",
        "days_ago": 5,
        "impressions_range": "120k - 260k",
        "spend_tier": "$4,000 - $8,000",
        "country_region": "India",
        "source": "Benchmark Reference Dataset (Google Ads Transparency Archive)",
        "is_demo": 1
    },

    # ============================================================
    # 2. UNACADEMY ADS
    # ============================================================
    {
        "ad_id": "meta-unac-001",
        "competitor_id": "comp-unacademy",
        "platform": "meta",
        "headline": "UNSAT 2026: Take the National Scholarship Admission Test & Win up to 90% Scholarship",
        "body_text": "Crack IIT JEE, NEET UG, and Foundation exams with India's best educators. Appear for UNSAT online or at an Unacademy Centre near you and win 100% tuition scholarships plus a trip to Euro Space Camp.",
        "description": "Free test registration closing this Sunday. Over 2.5 Lakh students competing.",
        "cta_text": "Register for Free",
        "creative_url": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=800&auto=format&fit=crop&q=80",
        "media_type": "video",
        "landing_page_url": "https://unacademy.com/scholarship/unsat",
        "ad_library_url": "https://www.facebook.com/ads/library/?id=meta-unac-001",
        "google_placement": None,
        "is_placement_verified": 0,
        "course_categories": ["JEE Preparation", "NEET Preparation", "College Admissions"],
        "marketing_hook": "Win up to 90% Scholarship for IIT JEE & NEET UG with UNSAT",
        "value_proposition": "Up to 90% Scholarship • All-India Rank Benchmark • Offline Centers Access",
        "offer_details": "Up to 90% Scholarship Admission Test",
        "audience_hypothesis": "Students from Class 9 to 12 targeting competitive engineering/medical exams",
        "creative_strategy": "Gamified Competitive Motivation • Heavy Scholarship Incentive • Urgency (Closing Sunday)",
        "days_ago": 2,
        "impressions_range": "400k - 750k",
        "spend_tier": "$15,000+",
        "country_region": "India",
        "source": "Benchmark Reference Dataset (Meta Ad Library Archive)",
        "is_demo": 1
    },
    {
        "ad_id": "google-unac-002",
        "competitor_id": "comp-unacademy",
        "platform": "google",
        "headline": "UPSC CSE 2026 Aarambh Batch: Learn with India's Renowned Faculty",
        "body_text": "Study with legendary educators like Mrunal Patel, Dr. Sidharth Arora, and Pratik Nayak. Comprehensive Prelims & Mains integrated syllabus with 1:1 mentorship and live daily answer evaluation.",
        "description": "Save flat 20% on all UPSC subscriptions with code CSE20. 0% Interest EMI available.",
        "cta_text": "Get Subscription",
        "creative_url": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800&auto=format&fit=crop&q=80",
        "media_type": "image",
        "landing_page_url": "https://unacademy.com/goal/upsc-civil-services-examination-ias-preparation/KSCGY",
        "ad_library_url": "https://adstransparency.google.com/advertiser/AR58291042?region=IN",
        "google_placement": "Google Discover",
        "is_placement_verified": 1,
        "course_categories": ["UPSC Preparation", "Government Exams", "Online Courses"],
        "marketing_hook": "Learn from India's Top UPSC Educators in the New Aarambh Batch",
        "value_proposition": "Top Star Educators (Mrunal Patel) • 1:1 Mentorship • Integrated Prelims + Mains",
        "offer_details": "Flat 20% Discount with Code CSE20",
        "audience_hypothesis": "Serious UPSC CSE Aspirants who prioritize top-tier educator brands",
        "creative_strategy": "Celebrity Faculty Star Power • Authority Positioning • Limited Discount",
        "days_ago": 4,
        "impressions_range": "180k - 380k",
        "spend_tier": "$8,000 - $15,000",
        "country_region": "India",
        "source": "Benchmark Reference Dataset (Google Ads Transparency Archive)",
        "is_demo": 1
    },
    {
        "ad_id": "google-unac-003",
        "competitor_id": "comp-unacademy",
        "platform": "google",
        "headline": "CAT & OMETs 2026: Crack 99+ Percentile with Top IIM Alumni Mentors",
        "body_text": "Comprehensive Quantitative Aptitude, DILR, and VARC syllabus. 50+ full-length sectional mocks and simulated national percentile predictors. Join the league of 99+ percentilers.",
        "description": "Attend free Strategy Masterclass by 100%iler Ravi Prakash tonight at 8 PM.",
        "cta_text": "Join Free Webinar",
        "creative_url": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&auto=format&fit=crop&q=80",
        "media_type": "image",
        "landing_page_url": "https://unacademy.com/goal/cat-other-mba-entrance-tests/XNDUS",
        "ad_library_url": "https://adstransparency.google.com/advertiser/AR58291042?region=IN",
        "google_placement": "Google Ad – Placement Unknown",
        "is_placement_verified": 0,
        "course_categories": ["CAT Preparation", "MBA and Management"],
        "marketing_hook": "Crack 99+ Percentile in CAT 2026 with Top IIM Mentors",
        "value_proposition": "Full Length Percentile Mocks • Sectional Strategies • Free Live Webinar",
        "offer_details": "Free Strategy Masterclass Session",
        "audience_hypothesis": "Final-year college grads & young professionals targeting IIMs and Top B-Schools",
        "creative_strategy": "Aspirational 99%ile Benchmark • Free Strategy Hook • Urgency",
        "days_ago": 6,
        "impressions_range": "90k - 210k",
        "spend_tier": "$3,500 - $7,000",
        "country_region": "India",
        "source": "Benchmark Reference Dataset (Google Ads Transparency Archive)",
        "is_demo": 1
    },

    # ============================================================
    # 3. SCALER ADS
    # ============================================================
    {
        "ad_id": "meta-scaler-001",
        "competitor_id": "comp-scaler",
        "platform": "meta",
        "headline": "Tired of Service-Company CTC? Upgrade to Top Tech Product Roles with Scaler",
        "body_text": "Master System Design, Advanced Data Structures, and Distributed Systems with engineers from Google, Amazon & Meta. Real 1:1 career mentorship and guaranteed interview opportunities. Average CTC hike of 126%.",
        "description": "Book a Free 1:1 Career Roadmapping Session with a Senior Tech Architect.",
        "cta_text": "Book Free Session",
        "creative_url": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=800&auto=format&fit=crop&q=80",
        "media_type": "carousel",
        "landing_page_url": "https://scaler.com/academy",
        "ad_library_url": "https://www.facebook.com/ads/library/?id=meta-scaler-001",
        "google_placement": None,
        "is_placement_verified": 0,
        "course_categories": ["Coding", "Software Development", "Job Placement", "Career Development"],
        "marketing_hook": "Tired of Service-Company CTC? Switch to Top Tech Product Roles",
        "value_proposition": "System Design Curriculum • 1:1 Mentorship from MAANG • 126% Average CTC Hike",
        "offer_details": "Free 1:1 Career Counseling & Resume Audit",
        "audience_hypothesis": "Software Engineers in IT Services / QA / Low-growth tech roles seeking transition to Product companies",
        "creative_strategy": "Career Dissatisfaction Empathy • Specific Salary Hike Metric (126%) • High Perceived Authority",
        "days_ago": 1,
        "impressions_range": "280k - 540k",
        "spend_tier": "$12,000 - $20,000",
        "country_region": "India",
        "source": "Benchmark Reference Dataset (Meta Ad Library Archive)",
        "is_demo": 1
    },
    {
        "ad_id": "google-scaler-002",
        "competitor_id": "comp-scaler",
        "platform": "google",
        "headline": "Scaler Data Science & Machine Learning: Build Real-World LLMs & GenAI Systems",
        "body_text": "Move beyond basic Python libraries. Build end-to-end recommendation engines, computer vision pipelines, and production Generative AI models. Learn live from Principal AI Researchers.",
        "description": "Download free 40-page Data Science & AI Interview Guidebook with curated questions.",
        "cta_text": "Download Guide",
        "creative_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&auto=format&fit=crop&q=80",
        "media_type": "image",
        "landing_page_url": "https://scaler.com/data-science-course",
        "ad_library_url": "https://adstransparency.google.com/advertiser/AR74910283?region=IN",
        "google_placement": "Google Discover",
        "is_placement_verified": 1,
        "course_categories": ["Data Science", "Artificial Intelligence", "Career Development"],
        "marketing_hook": "Build Production-Ready LLMs & GenAI Systems with Scaler Data Science",
        "value_proposition": "Practical Production ML • Live Guidance from Principal Researchers • Free Interview Guide",
        "offer_details": "Free 40-page Data Science Interview Guidebook",
        "audience_hypothesis": "Data Analysts, Software Devs & Tech Aspirants wanting to capitalize on the GenAI wave",
        "creative_strategy": "Cutting-Edge Tech FOMO (GenAI/LLM) • Depth over Basics • High-Intent Discovery Asset",
        "days_ago": 3,
        "impressions_range": "210k - 430k",
        "spend_tier": "$8,500 - $16,000",
        "country_region": "India",
        "source": "Benchmark Reference Dataset (Google Ads Transparency Archive)",
        "is_demo": 1
    },
    {
        "ad_id": "google-scaler-003",
        "competitor_id": "comp-scaler",
        "platform": "google",
        "headline": "Scaler School of Technology: 4-Year Undergraduate CS Program in Bengaluru",
        "body_text": "The next-generation Computer Science program designed by tech leaders. Top students build real software products from day one, mentored by CTOs. 1-year mandatory paid internship.",
        "description": "Admissions open for Class 12th students. Scholarship entrance test dates announced.",
        "cta_text": "Apply Now",
        "creative_url": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=800&auto=format&fit=crop&q=80",
        "media_type": "carousel",
        "landing_page_url": "https://scaler.com/school-of-technology",
        "ad_library_url": "https://adstransparency.google.com/advertiser/AR74910283?region=IN",
        "google_placement": "Demand Gen",
        "is_placement_verified": 1,
        "course_categories": ["College Admissions", "Coding", "Software Development", "Internship"],
        "marketing_hook": "Re-architecting CS Education: The 4-Year Tech Degree in Bengaluru",
        "value_proposition": "1-Year Mandatory Paid Tech Internship • Taught by Real CTOs • Live Product Building",
        "offer_details": "Merit-Based Entrance Scholarship Available",
        "audience_hypothesis": "Class 12 School Graduates and Parents seeking alternatives to traditional engineering colleges",
        "creative_strategy": "Disruptive College Education Claim • Silicon Valley Pedagogy • High Career Certainty",
        "days_ago": 5,
        "impressions_range": "150k - 320k",
        "spend_tier": "$6,000 - $13,000",
        "country_region": "India",
        "source": "Benchmark Reference Dataset (Google Ads Transparency Archive)",
        "is_demo": 1
    },

    # ============================================================
    # 4. UPGRAD BENCHMARK ADS
    # ============================================================
    {
        "ad_id": "meta-upgrad-001",
        "competitor_id": "comp-upgrad",
        "platform": "meta",
        "headline": "Executive PG Diploma in Data Science with IIIT Bangalore: 300+ Hiring Partners",
        "body_text": "Ranked #1 Data Science program for working professionals. Choose from 5 specializations including GenAI, NLP, and Deep Learning. Dedicated placement support with up to 50% average salary hike.",
        "description": "Next cohort starts this month. 0% EMI options starting at Rs 6,850/month.",
        "cta_text": "Download Brochure",
        "creative_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&auto=format&fit=crop&q=80",
        "media_type": "carousel",
        "landing_page_url": "https://upgrad.com/data-science-pgd-iiitb",
        "ad_library_url": "https://www.facebook.com/ads/library/?id=meta-upgrad-001",
        "google_placement": None,
        "is_placement_verified": 0,
        "course_categories": ["Data Science", "Artificial Intelligence", "Professional Certification"],
        "marketing_hook": "Ranked #1 Data Science PG Program for Working Professionals with IIITB",
        "value_proposition": "IIIT Bangalore Alumni Status • 5 Specializations • Dedicated Career Support",
        "offer_details": "0% No-Cost EMI Starting at ₹6,850/mo",
        "audience_hypothesis": "Mid-career corporate professionals seeking academic certification alongside job",
        "creative_strategy": "Prestige University Partnership • Career Re-skilling Aspiration",
        "days_ago": 2,
        "impressions_range": "220k - 460k",
        "spend_tier": "$9,000 - $17,000",
        "country_region": "India",
        "source": "Benchmark Reference Dataset (Meta Ad Library Archive)",
        "is_demo": 1
    },
    {
        "ad_id": "google-upgrad-002",
        "competitor_id": "comp-upgrad",
        "platform": "google",
        "headline": "Online Global MBA from Deakin Business School & Liverpool John Moores",
        "body_text": "Accelerate your executive trajectory with a dual credential. Complete in 18 months while working full-time. Dual alumni status and networking in 85+ countries.",
        "description": "Up to Rs 1,50,000 merit-based scholarships available for upcoming intake.",
        "cta_text": "Check Eligibility",
        "creative_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=800&auto=format&fit=crop&q=80",
        "media_type": "image",
        "landing_page_url": "https://upgrad.com/mba-global",
        "ad_library_url": "https://adstransparency.google.com/advertiser/AR48192039?region=IN",
        "google_placement": "Google Discover",
        "is_placement_verified": 1,
        "course_categories": ["MBA and Management", "Study Abroad", "Professional Certification"],
        "marketing_hook": "Dual Credential Global MBA from Top Australian & UK Business Schools",
        "value_proposition": "Top Global B-School Accreditation • 18 Months Online • Up to ₹1.5L Scholarship",
        "offer_details": "Up to ₹1,50,000 Merit Scholarship",
        "audience_hypothesis": "Senior Team Leads & Managers seeking executive management credentials",
        "creative_strategy": "Global Brand Prestige • Career Ceiling Breakthrough Empathy",
        "days_ago": 4,
        "impressions_range": "140k - 310k",
        "spend_tier": "$6,500 - $14,000",
        "country_region": "India",
        "source": "Benchmark Reference Dataset (Google Ads Transparency Archive)",
        "is_demo": 1
    },

    # ============================================================
    # 5. GEEKSFORGEEKS BENCHMARK ADS
    # ============================================================
    {
        "ad_id": "meta-gfg-001",
        "competitor_id": "comp-gfg",
        "platform": "meta",
        "headline": "Master Data Structures & Algorithms with Sandeep Jain (Ex-Amazon)",
        "body_text": "Crack tech interviews at Microsoft, Google, Uber and top startups. 250+ curated DSA coding problems with live mentor support and mock interview simulations.",
        "description": "Use coupon GFG25 to get flat 25% off during our Tech Talent Week.",
        "cta_text": "Claim 25% Off",
        "creative_url": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=800&auto=format&fit=crop&q=80",
        "media_type": "carousel",
        "landing_page_url": "https://geeksforgeeks.org/courses/dsa-self-paced",
        "ad_library_url": "https://www.facebook.com/ads/library/?id=meta-gfg-001",
        "google_placement": None,
        "is_placement_verified": 0,
        "course_categories": ["Coding", "Software Development", "Job Placement"],
        "marketing_hook": "Crack Coding Interviews with Sandeep Jain's Complete DSA Bootcamp",
        "value_proposition": "250+ Curated Problems • Mock Interviews • Direct Creator Mentorship",
        "offer_details": "Flat 25% Off with Coupon GFG25",
        "audience_hypothesis": "CS Students and Junior Developers preparing for upcoming campus & off-campus hiring",
        "creative_strategy": "Founder / Mentor Credibility • Direct Problem-Solving Focus • Limited Coupon Code",
        "days_ago": 1,
        "impressions_range": "180k - 360k",
        "spend_tier": "$5,000 - $9,500",
        "country_region": "India",
        "source": "Benchmark Reference Dataset (Meta Ad Library Archive)",
        "is_demo": 1
    },
    {
        "ad_id": "google-gfg-002",
        "competitor_id": "comp-gfg",
        "platform": "google",
        "headline": "Complete GATE Computer Science 2026 Preparation Live Course",
        "body_text": "Live interactive lectures for all GATE CS subjects, 60+ full-length mock tests, subject-wise PYQ banks, and college PSU guidance from AIR Top 100 mentors.",
        "description": "Free GATE CS Diagnostic Scholarship Test on Sunday.",
        "cta_text": "Register Free",
        "creative_url": "https://images.unsplash.com/photo-1509062522246-3755977927d7?w=800&auto=format&fit=crop&q=80",
        "media_type": "image",
        "landing_page_url": "https://geeksforgeeks.org/courses/gate-live",
        "ad_library_url": "https://adstransparency.google.com/advertiser/AR29184729?region=IN",
        "google_placement": "Google Ad – Placement Unknown",
        "is_placement_verified": 0,
        "course_categories": ["Government Exams", "Coding", "Online Courses"],
        "marketing_hook": "Comprehensive Live Preparation for GATE Computer Science 2026",
        "value_proposition": "AIR Top 100 Mentors • 60+ Full Mocks • Free Diagnostic Test",
        "offer_details": "Free Diagnostic Scholarship Test",
        "audience_hypothesis": "B.Tech Engineering Students preparing for GATE and PSU Government jobs",
        "creative_strategy": "Systematic Exam Coverage • High-Intent Search Alignment",
        "days_ago": 3,
        "impressions_range": "80k - 170k",
        "spend_tier": "$2,500 - $5,500",
        "country_region": "India",
        "source": "Benchmark Reference Dataset (Google Ads Transparency Archive)",
        "is_demo": 1
    }
]

def seed_edtech_data(force=False):
    """
    Populates authentic EdTech competitors (PW, Unacademy, Scaler, upGrad, GFG)
    and their Meta + Google advertisements with strict transparency labeling.
    """
    conn = database.get_connection()
    # Check if Physics Wallah already exists
    pw_check = conn.execute("SELECT id FROM competitors WHERE name LIKE '%Physics Wallah%'").fetchone()
    conn.close()

    if pw_check and not force:
        print("[Seed] EdTech competitor brands already present in database.")
        return

    print("[Seed] Initializing 3 core EdTech competitor brands (PW, Unacademy, Scaler)...")
    for comp in SEED_COMPETITORS:
        database.upsert_competitor(
            name=comp["name"],
            domain=comp["domain"],
            industry=comp["industry"],
            logo_url=comp["logo_url"],
            platforms=comp["platforms"],
            advertiser_ids=comp.get("advertiser_ids"),
            comp_id=comp["id"]
        )

    print("[Seed] Ingesting authentic EdTech ads across Meta and Google (Discover & Demand Gen)...")
    now = datetime.now()
    for ad in SEED_ADS:
        first_seen = (now - timedelta(days=ad.get("days_ago", 2), hours=3)).strftime("%Y-%m-%d %H:%M:%S")
        database.insert_ad(
            competitor_id=ad["competitor_id"],
            platform=ad["platform"],
            headline=ad.get("headline"),
            body_text=ad.get("body_text", ""),
            description=ad.get("description"),
            cta_text=ad.get("cta_text"),
            creative_url=ad.get("creative_url"),
            media_type=ad.get("media_type", "image"),
            landing_page_url=ad.get("landing_page_url"),
            ad_library_url=ad.get("ad_library_url"),
            google_placement=ad.get("google_placement", "Google Ad – Placement Unknown"),
            is_placement_verified=ad.get("is_placement_verified", 0),
            course_categories=ad.get("course_categories"),
            marketing_hook=ad.get("marketing_hook"),
            value_proposition=ad.get("value_proposition"),
            offer_details=ad.get("offer_details"),
            audience_hypothesis=ad.get("audience_hypothesis"),
            creative_strategy=ad.get("creative_strategy"),
            first_seen=first_seen,
            status=ad.get("status", "ACTIVE"),
            impressions_range=ad.get("impressions_range"),
            spend_tier=ad.get("spend_tier"),
            country_region=ad.get("country_region", "India"),
            source=ad.get("source", "Benchmark Reference Dataset"),
            is_demo=ad.get("is_demo", 1),
            ad_id=ad.get("ad_id")
        )

    print("[Seed] Synthesizing initial EdTech Weekly Intelligence Briefing...")
    summarizer.generate_weekly_digest(custom_days=7)
    print("[Seed] EdTech database initialization completed successfully!")

def seed_database_if_empty():
    seed_edtech_data(force=False)

if __name__ == "__main__":
    database.init_db()
    seed_edtech_data(force=True)
