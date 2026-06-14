"""
Real, researched dataset for appsaavy.space — the agentic-ready B2B data provider landscape.
All entries are REAL companies / signals (no mock data). Sourced from 2026 GTM research.
Used by seed_zite.py to populate the Zite database.
"""

# ---------------------------------------------------------------------------
# PROVIDERS  (galaxies)
# universes: subset of ["Intent","Enrichment","Technographic","MCP Hub"]
# node_size: 1-5 rank (mapped to 18-32px on the canvas)
# ---------------------------------------------------------------------------
PROVIDERS = [
    {"slug": "apollo-io", "name": "Apollo.io", "pricing_tier": "Freemium", "node_size": 5,
     "website_url": "https://www.apollo.io", "docs_url": "https://docs.apollo.io/",
     "coverage_summary": "275M+ contacts, 73M+ companies, global",
     "universes": ["Enrichment", "Intent", "MCP Hub"],
     "description": "All-in-one B2B sales intelligence and engagement platform. High-density contact and company database with real-time intent signals, email sequencing, and a native MCP server (launched 2026) for agentic workflows."},

    {"slug": "zoominfo", "name": "ZoomInfo", "pricing_tier": "Enterprise", "node_size": 5,
     "website_url": "https://www.zoominfo.com", "docs_url": "https://api-docs.zoominfo.com/",
     "coverage_summary": "174M+ emails, 70M+ direct dials, 100M+ companies",
     "universes": ["Enrichment", "Intent", "Technographic", "MCP Hub"],
     "description": "The enterprise standard for US B2B data. Deepest firmographic, technographic and intent coverage with Universal Access via REST API and a native MCP server (GTM.AI) for AI agents."},

    {"slug": "6sense", "name": "6sense", "pricing_tier": "Enterprise", "node_size": 5,
     "website_url": "https://6sense.com", "docs_url": "https://6sense.com/platform/",
     "coverage_summary": "AI predictive intent + dark-funnel account graph",
     "universes": ["Intent", "Technographic"],
     "description": "AI-powered ABM orchestration platform. Maps anonymous buying activity to accounts, predicts buying-stage, and surfaces in-market accounts via a proprietary intent graph plus third-party signals."},

    {"slug": "clearbit", "name": "Clearbit", "pricing_tier": "Paid", "node_size": 4,
     "website_url": "https://clearbit.com", "docs_url": "https://dashboard.clearbit.com/docs",
     "coverage_summary": "Company + contact enrichment, IP-to-company reveal",
     "universes": ["Enrichment", "Technographic"],
     "description": "Real-time enrichment API (now HubSpot Breeze Intelligence). Resolves domains and emails into rich firmographic, technographic and demographic attributes, plus IP-based visitor de-anonymization."},

    {"slug": "bombora", "name": "Bombora", "pricing_tier": "Enterprise", "node_size": 4,
     "website_url": "https://bombora.com", "docs_url": "https://bombora.com/data/",
     "coverage_summary": "Company Surge intent across 5,000+ B2B sites",
     "universes": ["Intent"],
     "description": "The intent-data backbone of B2B. Tracks content consumption across a 5,000+ site co-op to surface companies actively researching specific topics (Company Surge), consumed via most major GTM platforms."},

    {"slug": "cognism", "name": "Cognism", "pricing_tier": "Enterprise", "node_size": 4,
     "website_url": "https://www.cognism.com", "docs_url": "https://www.cognism.com/api",
     "coverage_summary": "400M+ profiles, phone-verified EU mobiles (Diamond Data)",
     "universes": ["Enrichment", "Intent"],
     "description": "GDPR/CCPA-compliant data provider strongest in EMEA. Phone-verified 'Diamond' mobile numbers, verified emails, and Bombora-powered intent for compliant European outreach."},

    {"slug": "lusha", "name": "Lusha", "pricing_tier": "Freemium", "node_size": 3,
     "website_url": "https://www.lusha.com", "docs_url": "https://www.lusha.com/docs/",
     "coverage_summary": "100M+ profiles, strong US/NA direct dials",
     "universes": ["Enrichment"],
     "description": "Fast contact-data tool known for accurate US direct dials and a frictionless Chrome extension + REST API for on-demand email and phone enrichment."},

    {"slug": "peopledatalabs", "name": "PeopleDataLabs", "pricing_tier": "Paid", "node_size": 4,
     "website_url": "https://www.peopledatalabs.com", "docs_url": "https://docs.peopledatalabs.com/",
     "coverage_summary": "3B+ person profiles, 70M+ companies — raw API",
     "universes": ["Enrichment"],
     "description": "Raw, usage-priced person and company datasets built for engineers. The go-to for building custom data products and large-scale enrichment pipelines at ~$0.01/record."},

    {"slug": "crunchbase", "name": "Crunchbase", "pricing_tier": "Paid", "node_size": 3,
     "website_url": "https://www.crunchbase.com", "docs_url": "https://data.crunchbase.com/docs",
     "coverage_summary": "Company funding, M&A, leadership, and growth data",
     "universes": ["Enrichment"],
     "description": "Authoritative source for company funding rounds, investors, acquisitions and leadership changes — a key signal layer for timing outreach around capital events."},

    {"slug": "hg-insights", "name": "HG Insights", "pricing_tier": "Enterprise", "node_size": 3,
     "website_url": "https://hginsights.com", "docs_url": "https://hginsights.com/platform/",
     "coverage_summary": "Technographics + IT spend across millions of companies",
     "universes": ["Technographic"],
     "description": "Technology install and IT-spend intelligence. Maps the verified tech stack and budgets of companies to power technographic targeting and competitive displacement plays."},

    {"slug": "trigify", "name": "Trigify", "pricing_tier": "Paid", "node_size": 2,
     "website_url": "https://trigify.io", "docs_url": "https://trigify.io",
     "coverage_summary": "Social + job-change signals from LinkedIn activity",
     "universes": ["Intent"],
     "description": "Social-signal monitoring that tracks LinkedIn engagement, job changes and post activity to surface warm, timely outreach moments for founders and sellers."},

    {"slug": "builtwith", "name": "BuiltWith", "pricing_tier": "Paid", "node_size": 3,
     "website_url": "https://builtwith.com", "docs_url": "https://api.builtwith.com/",
     "coverage_summary": "Tech profiles for 1B+ websites",
     "universes": ["Technographic"],
     "description": "Website technology profiler that detects the full tech stack of any domain — analytics, CMS, payment, hosting, and martech — via a simple lookup API."},

    {"slug": "wappalyzer", "name": "Wappalyzer", "pricing_tier": "Freemium", "node_size": 2,
     "website_url": "https://www.wappalyzer.com", "docs_url": "https://www.wappalyzer.com/docs/",
     "coverage_summary": "Technology lookups + lead lists by tech",
     "universes": ["Technographic"],
     "description": "Lightweight technology-detection API and lead lists. Identify the technologies a company uses and build target lists filtered by installed tech."},

    {"slug": "datanyze", "name": "Datanyze", "pricing_tier": "Freemium", "node_size": 2,
     "website_url": "https://www.datanyze.com", "docs_url": "https://www.datanyze.com",
     "coverage_summary": "Technographics + contact data for SMB targeting",
     "universes": ["Technographic", "Enrichment"],
     "description": "Technographic and contact data tool focused on SMB prospecting, surfacing the tools a company uses alongside lightweight contact enrichment."},

    {"slug": "g2", "name": "G2", "pricing_tier": "Enterprise", "node_size": 4,
     "website_url": "https://www.g2.com", "docs_url": "https://buyerintent.g2.com/",
     "coverage_summary": "Buyer Intent from software review-category research",
     "universes": ["Intent"],
     "description": "Buyer Intent data from the largest software review marketplace. Surfaces accounts actively researching your category and your competitors on G2."},

    {"slug": "demandbase", "name": "Demandbase", "pricing_tier": "Enterprise", "node_size": 4,
     "website_url": "https://www.demandbase.com", "docs_url": "https://developers.demandbase.com/",
     "coverage_summary": "Account intelligence + intent + technographics",
     "universes": ["Intent", "Technographic"],
     "description": "Enterprise ABM and account-intelligence platform combining first- and third-party intent, technographics and firmographics to prioritize in-market accounts."},

    {"slug": "warmly", "name": "Warmly", "pricing_tier": "Freemium", "node_size": 3,
     "website_url": "https://www.warmly.ai", "docs_url": "https://www.warmly.ai/p/help-center",
     "coverage_summary": "Person & account-level website de-anonymization",
     "universes": ["Intent"],
     "description": "Signal-based revenue orchestration that de-anonymizes website visitors at person and account level using 20+ data sources, then auto-engages via chat, email and routing."},

    {"slug": "rb2b", "name": "RB2B", "pricing_tier": "Freemium", "node_size": 3,
     "website_url": "https://www.rb2b.com", "docs_url": "https://www.rb2b.com",
     "coverage_summary": "Person-level US website visitor identification",
     "universes": ["Intent"],
     "description": "Identifies anonymous US website visitors at the person level and pushes their LinkedIn profile straight to Slack — built for fast, manual founder-led outreach."},

    {"slug": "vector", "name": "Vector", "pricing_tier": "Paid", "node_size": 2,
     "website_url": "https://www.vector.co", "docs_url": "https://www.vector.co",
     "coverage_summary": "Person-level identity resolution + buying signals",
     "universes": ["Intent"],
     "description": "Lightweight identity resolution that de-anonymizes website visitors at the person level and layers on contact-level buying signals for precise outreach."},

    {"slug": "koala", "name": "Koala", "pricing_tier": "Freemium", "node_size": 2,
     "website_url": "https://getkoala.com", "docs_url": "https://getkoala.com/docs",
     "coverage_summary": "Product + web intent scoring for PLG",
     "universes": ["Intent"],
     "description": "Product-led intent platform that scores account and visitor activity across your website and product to tell sellers exactly which accounts are heating up."},

    {"slug": "common-room", "name": "Common Room", "pricing_tier": "Paid", "node_size": 3,
     "website_url": "https://www.commonroom.io", "docs_url": "https://www.commonroom.io/docs/",
     "coverage_summary": "Signal aggregation across community, web & social",
     "universes": ["Intent"],
     "description": "Signal-capture platform that unifies website, community, social and product signals into person/account profiles, with automations to route the hottest prospects."},

    {"slug": "dealfront", "name": "Dealfront", "pricing_tier": "Paid", "node_size": 3,
     "website_url": "https://www.dealfront.com", "docs_url": "https://www.dealfront.com/developers/",
     "coverage_summary": "EU-focused company visitor ID + B2B data (Leadfeeder)",
     "universes": ["Intent", "Enrichment"],
     "description": "GDPR-first company-level website visitor identification (formerly Leadfeeder + Echobot) with European firmographic data and trigger events for compliant EU pipelines."},

    {"slug": "coresignal", "name": "Coresignal", "pricing_tier": "Paid", "node_size": 3,
     "website_url": "https://coresignal.com", "docs_url": "https://docs.coresignal.com/",
     "coverage_summary": "Multi-source company, employee & jobs data via API/MCP",
     "universes": ["Enrichment", "MCP Hub"],
     "description": "Fresh, multi-source company, employee and job-postings datasets delivered via REST API and a native MCP server — ideal for headcount, hiring and talent-flow signals."},

    {"slug": "crustdata", "name": "Crustdata", "pricing_tier": "Paid", "node_size": 3,
     "website_url": "https://crustdata.com", "docs_url": "https://docs.crustdata.com/",
     "coverage_summary": "Real-time company & people data API + MCP",
     "universes": ["Enrichment", "Intent", "MCP Hub"],
     "description": "Real-time company and people data API with headcount trends, job changes and growth metrics, exposed through a native MCP server for agentic GTM workflows."},

    {"slug": "predictleads", "name": "PredictLeads", "pricing_tier": "Paid", "node_size": 2,
     "website_url": "https://predictleads.com", "docs_url": "https://docs.predictleads.com/",
     "coverage_summary": "Hiring, funding & technology event signals via API",
     "universes": ["Intent", "Technographic"],
     "description": "Company-event signal API surfacing job openings, funding events, technology adoption and news triggers — a structured feed of buying-intent events for engineers."},

    {"slug": "hunter-io", "name": "Hunter.io", "pricing_tier": "Freemium", "node_size": 2,
     "website_url": "https://hunter.io", "docs_url": "https://hunter.io/api-documentation/v2",
     "coverage_summary": "100M+ emails, domain search, ~95% email accuracy",
     "universes": ["Enrichment"],
     "description": "Email-finding specialist. Domain search and email-finder API with high deliverability accuracy, ideal as a verification layer in an enrichment waterfall."},

    {"slug": "prospeo", "name": "Prospeo", "pricing_tier": "Freemium", "node_size": 2,
     "website_url": "https://prospeo.io", "docs_url": "https://prospeo.io/api",
     "coverage_summary": "300M+ profiles, 143M+ verified emails, 7-day refresh",
     "universes": ["Enrichment"],
     "description": "Freshness-focused enrichment API with verified emails and mobile numbers at ~$0.01/record, refreshed weekly for high-accuracy automated pipelines."},

    {"slug": "leadmagic", "name": "LeadMagic", "pricing_tier": "Paid", "node_size": 2,
     "website_url": "https://leadmagic.io", "docs_url": "https://docs.leadmagic.io/",
     "coverage_summary": "Email/mobile finder + B2B social enrichment",
     "universes": ["Enrichment"],
     "description": "Usage-based enrichment API for email and mobile finding, email-to-profile and B2B social enrichment — popular as a Clay-native waterfall source."},

    {"slug": "findymail", "name": "Findymail", "pricing_tier": "Paid", "node_size": 2,
     "website_url": "https://www.findymail.com", "docs_url": "https://www.findymail.com/api",
     "coverage_summary": "Email finder + 99% verification, phone & reverse lookup",
     "universes": ["Enrichment"],
     "description": "Email finding and validation suite with phone and reverse lookup, known for high verification accuracy and cost-efficient credits in enrichment waterfalls."},

    {"slug": "ocean-io", "name": "Ocean.io", "pricing_tier": "Paid", "node_size": 2,
     "website_url": "https://www.ocean.io", "docs_url": "https://www.ocean.io",
     "coverage_summary": "Lookalike company targeting + firmographics",
     "universes": ["Enrichment"],
     "description": "AI lookalike company search that builds target lists from your best customers using firmographic and similarity modeling for precise TAM expansion."},

    {"slug": "harmonic", "name": "Harmonic", "pricing_tier": "Paid", "node_size": 2,
     "website_url": "https://harmonic.ai", "docs_url": "https://console.harmonic.ai/docs",
     "coverage_summary": "Startup & growth-company data for VC/GTM",
     "universes": ["Enrichment", "Intent"],
     "description": "Startup intelligence database tracking funding, headcount growth and founder signals across millions of private companies — built for sourcing emerging accounts."},

    {"slug": "explorium", "name": "Explorium", "pricing_tier": "Enterprise", "node_size": 3,
     "website_url": "https://www.explorium.ai", "docs_url": "https://www.explorium.ai/data/",
     "coverage_summary": "External data + agentic GTM data access",
     "universes": ["Enrichment", "Intent"],
     "description": "External-data platform that connects thousands of signals and datasets into GTM systems and AI agents, offering enrichment and intent through a unified data layer."},
]

# ---------------------------------------------------------------------------
# SIGNALS  (Entities = suns, Properties = stars, Signals = planets)
# signal_type: "Entity" | "Property" | "Signal"
# universe: which universe it primarily belongs to
# field_type: String|Number|Boolean|Array|Object ; update_cadence: Real-time|Daily|Weekly|On Request
# ---------------------------------------------------------------------------
SIGNALS = [
    # ---- Entities (suns) ----
    {"slug": "company", "name": "Company", "signal_type": "Entity", "universe": "Enrichment",
     "field_name": "company", "field_type": "Object", "update_cadence": "On Request",
     "description": "The core account entity — a business organization with firmographic attributes."},
    {"slug": "contact", "name": "Contact", "signal_type": "Entity", "universe": "Enrichment",
     "field_name": "contact", "field_type": "Object", "update_cadence": "On Request",
     "description": "A person entity tied to a company — the human you are trying to reach."},
    {"slug": "account-visitor", "name": "Website Visitor", "signal_type": "Entity", "universe": "Intent",
     "field_name": "visitor", "field_type": "Object", "update_cadence": "Real-time",
     "description": "An identified (de-anonymized) visitor entity captured from your web traffic."},

    # ---- Properties (stars — firmographic/contact attributes) ----
    {"slug": "domain", "name": "Domain", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "domain", "field_type": "String", "update_cadence": "On Request",
     "description": "The primary web domain used as the canonical key for company resolution."},
    {"slug": "industry", "name": "Industry", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "industry", "field_type": "String", "update_cadence": "On Request",
     "description": "Industry / vertical classification of the company (NAICS, SIC or custom)."},
    {"slug": "employee-count", "name": "Employee Count", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "employee_count", "field_type": "Number", "update_cadence": "Weekly",
     "description": "Current headcount of the company — a core firmographic sizing attribute."},
    {"slug": "revenue", "name": "Revenue", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "annual_revenue", "field_type": "Number", "update_cadence": "On Request",
     "description": "Estimated annual revenue used for ICP sizing and segmentation."},
    {"slug": "hq-location", "name": "HQ Location", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "hq_location", "field_type": "String", "update_cadence": "On Request",
     "description": "Headquarters geography of the company (country / region / city)."},
    {"slug": "verified-email", "name": "Verified Email", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "email", "field_type": "String", "update_cadence": "On Request",
     "description": "A deliverability-verified business email address for a contact."},
    {"slug": "direct-dial", "name": "Direct Dial / Mobile", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "phone_mobile", "field_type": "String", "update_cadence": "On Request",
     "description": "A verified direct-dial or mobile phone number for a decision maker."},
    {"slug": "job-title", "name": "Job Title", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "job_title", "field_type": "String", "update_cadence": "On Request",
     "description": "Current role / title of a contact, used for persona and seniority targeting."},
    {"slug": "seniority", "name": "Seniority", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "seniority", "field_type": "String", "update_cadence": "On Request",
     "description": "Seniority level of a contact (IC, Manager, Director, VP, C-Suite)."},
    {"slug": "linkedin-url", "name": "LinkedIn URL", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "linkedin_url", "field_type": "String", "update_cadence": "On Request",
     "description": "Canonical LinkedIn profile URL for a contact — the identity backbone for B2B."},
    {"slug": "tech-stack", "name": "Tech Stack", "signal_type": "Property", "universe": "Technographic",
     "field_name": "technologies", "field_type": "Array", "update_cadence": "Weekly",
     "description": "The set of technologies a company has installed across its web and martech stack."},

    # ---- Signals (planets — dynamic buying events) ----
    {"slug": "job-change", "name": "Job Change", "signal_type": "Signal", "universe": "Intent",
     "field_name": "job_change_event", "field_type": "Object", "update_cadence": "Daily",
     "description": "A tracked contact changes companies or roles — a prime warm-outreach trigger."},
    {"slug": "champion-tracking", "name": "Champion Tracking", "signal_type": "Signal", "universe": "Intent",
     "field_name": "champion_move", "field_type": "Object", "update_cadence": "Daily",
     "description": "A past champion or buyer moves to a new company — a high-conversion re-engagement signal."},
    {"slug": "funding-round", "name": "New Funding Round", "signal_type": "Signal", "universe": "Intent",
     "field_name": "funding_event", "field_type": "Object", "update_cadence": "Daily",
     "description": "A company raises new capital — signals budget availability and growth motion."},
    {"slug": "hiring-surge", "name": "Hiring Surge", "signal_type": "Signal", "universe": "Intent",
     "field_name": "open_roles", "field_type": "Number", "update_cadence": "Daily",
     "description": "A spike in relevant open roles indicating team expansion and tooling needs."},
    {"slug": "leadership-hire", "name": "Leadership Hire", "signal_type": "Signal", "universe": "Intent",
     "field_name": "exec_hire", "field_type": "Object", "update_cadence": "Daily",
     "description": "A new executive joins — new leaders re-evaluate vendors in their first 90 days."},
    {"slug": "tech-install", "name": "Technology Install", "signal_type": "Signal", "universe": "Technographic",
     "field_name": "tech_added", "field_type": "Array", "update_cadence": "Weekly",
     "description": "A company adopts a new technology — a complement or competitive-displacement trigger."},
    {"slug": "tech-drop", "name": "Technology Drop", "signal_type": "Signal", "universe": "Technographic",
     "field_name": "tech_removed", "field_type": "Array", "update_cadence": "Weekly",
     "description": "A company removes a technology — a window to displace an incumbent vendor."},
    {"slug": "web-visit", "name": "Website Visit (De-anon)", "signal_type": "Signal", "universe": "Intent",
     "field_name": "visit_event", "field_type": "Object", "update_cadence": "Real-time",
     "description": "An identified visitor lands on your site — the highest-intent first-party signal."},
    {"slug": "intent-surge", "name": "Intent Topic Surge", "signal_type": "Signal", "universe": "Intent",
     "field_name": "surging_topics", "field_type": "Array", "update_cadence": "Weekly",
     "description": "Third-party content-consumption spike on your topics (Company Surge style)."},
    {"slug": "g2-research", "name": "G2 Category Research", "signal_type": "Signal", "universe": "Intent",
     "field_name": "g2_intent", "field_type": "Object", "update_cadence": "Daily",
     "description": "An account researches your category or competitors on review marketplaces."},
    {"slug": "headcount-growth", "name": "Headcount Growth Rate", "signal_type": "Signal", "universe": "Intent",
     "field_name": "headcount_growth", "field_type": "Number", "update_cadence": "Weekly",
     "description": "Rate of employee growth over time — a momentum signal for prioritization."},
    {"slug": "ma-activity", "name": "M&A Activity", "signal_type": "Signal", "universe": "Intent",
     "field_name": "ma_event", "field_type": "Object", "update_cadence": "Daily",
     "description": "Mergers, acquisitions or IPO events that reshape buying authority and budget."},
    {"slug": "product-launch", "name": "Product Launch", "signal_type": "Signal", "universe": "Intent",
     "field_name": "product_launch", "field_type": "Object", "update_cadence": "Daily",
     "description": "A company ships a new product — signals GTM investment and adjacent needs."},
    {"slug": "social-engagement", "name": "Social Engagement", "signal_type": "Signal", "universe": "Intent",
     "field_name": "social_activity", "field_type": "Object", "update_cadence": "Real-time",
     "description": "A prospect engages with relevant LinkedIn posts or topics — a soft warm signal."},
]

# ---------------------------------------------------------------------------
# PROVIDER -> SIGNALS  (provider_signals junction)
# value: list of (signal_slug, coverage_quality)  coverage_quality in Primary|Secondary|Limited
# ---------------------------------------------------------------------------
PROVIDER_SIGNALS = {
    "apollo-io": [("company", "Primary"), ("contact", "Primary"), ("verified-email", "Primary"),
                  ("direct-dial", "Secondary"), ("job-title", "Primary"), ("intent-surge", "Secondary"),
                  ("job-change", "Secondary"), ("linkedin-url", "Primary")],
    "zoominfo": [("company", "Primary"), ("contact", "Primary"), ("verified-email", "Primary"),
                 ("direct-dial", "Primary"), ("revenue", "Primary"), ("tech-stack", "Primary"),
                 ("intent-surge", "Primary"), ("employee-count", "Primary")],
    "6sense": [("intent-surge", "Primary"), ("g2-research", "Secondary"), ("web-visit", "Secondary"),
               ("tech-stack", "Secondary"), ("account-visitor", "Primary")],
    "clearbit": [("company", "Primary"), ("domain", "Primary"), ("industry", "Primary"),
                 ("revenue", "Secondary"), ("tech-stack", "Secondary"), ("web-visit", "Primary"),
                 ("account-visitor", "Primary")],
    "bombora": [("intent-surge", "Primary"), ("company", "Secondary")],
    "cognism": [("verified-email", "Primary"), ("direct-dial", "Primary"), ("contact", "Primary"),
                ("intent-surge", "Secondary"), ("hq-location", "Primary")],
    "lusha": [("direct-dial", "Primary"), ("verified-email", "Primary"), ("contact", "Secondary"),
              ("linkedin-url", "Secondary")],
    "peopledatalabs": [("contact", "Primary"), ("company", "Primary"), ("verified-email", "Primary"),
                       ("linkedin-url", "Primary"), ("job-title", "Primary"), ("employee-count", "Secondary")],
    "crunchbase": [("funding-round", "Primary"), ("ma-activity", "Primary"), ("company", "Secondary"),
                   ("leadership-hire", "Secondary")],
    "hg-insights": [("tech-stack", "Primary"), ("tech-install", "Primary"), ("tech-drop", "Secondary")],
    "trigify": [("social-engagement", "Primary"), ("job-change", "Primary")],
    "builtwith": [("tech-stack", "Primary"), ("tech-install", "Primary")],
    "wappalyzer": [("tech-stack", "Primary"), ("tech-install", "Secondary")],
    "datanyze": [("tech-stack", "Primary"), ("contact", "Limited"), ("verified-email", "Limited")],
    "g2": [("g2-research", "Primary"), ("intent-surge", "Secondary")],
    "demandbase": [("intent-surge", "Primary"), ("account-visitor", "Primary"), ("tech-stack", "Secondary"),
                   ("web-visit", "Secondary")],
    "warmly": [("web-visit", "Primary"), ("account-visitor", "Primary"), ("intent-surge", "Secondary")],
    "rb2b": [("web-visit", "Primary"), ("account-visitor", "Primary"), ("linkedin-url", "Secondary")],
    "vector": [("web-visit", "Primary"), ("account-visitor", "Primary")],
    "koala": [("web-visit", "Primary"), ("intent-surge", "Secondary"), ("account-visitor", "Secondary")],
    "common-room": [("web-visit", "Secondary"), ("social-engagement", "Primary"), ("intent-surge", "Secondary")],
    "dealfront": [("web-visit", "Primary"), ("account-visitor", "Primary"), ("company", "Secondary"),
                  ("hq-location", "Secondary")],
    "coresignal": [("company", "Primary"), ("employee-count", "Primary"), ("hiring-surge", "Primary"),
                   ("headcount-growth", "Primary"), ("job-change", "Secondary")],
    "crustdata": [("headcount-growth", "Primary"), ("job-change", "Primary"), ("hiring-surge", "Primary"),
                  ("company", "Secondary"), ("champion-tracking", "Secondary")],
    "predictleads": [("hiring-surge", "Primary"), ("funding-round", "Secondary"), ("tech-install", "Primary"),
                     ("product-launch", "Secondary")],
    "hunter-io": [("verified-email", "Primary"), ("domain", "Secondary")],
    "prospeo": [("verified-email", "Primary"), ("direct-dial", "Secondary")],
    "leadmagic": [("verified-email", "Primary"), ("direct-dial", "Secondary"), ("linkedin-url", "Secondary")],
    "findymail": [("verified-email", "Primary"), ("direct-dial", "Limited")],
    "ocean-io": [("company", "Primary"), ("industry", "Primary"), ("employee-count", "Secondary")],
    "harmonic": [("funding-round", "Primary"), ("headcount-growth", "Primary"), ("company", "Secondary"),
                 ("leadership-hire", "Secondary")],
    "explorium": [("company", "Primary"), ("intent-surge", "Secondary"), ("tech-stack", "Limited"),
                  ("revenue", "Secondary")],
}

# ---------------------------------------------------------------------------
# CONNECTORS  (per provider)  -> connectors table
# connector_type in: MCP Server | REST API | Clay Native | N8N Native | Snowflake | GraphQL | Webhook | CSV Export
# ---------------------------------------------------------------------------
def _rest(provider, url, docs, auth="API Key", rate="varies", verified=True):
    return {"connector_type": "REST API", "auth_method": auth, "endpoint_url": url,
            "docs_url": docs, "rate_limit": rate, "is_verified": verified}

CONNECTORS = {
    "apollo-io": [
        _rest("apollo-io", "https://api.apollo.io/v1", "https://docs.apollo.io/", "API Key", "varies by plan"),
        {"connector_type": "MCP Server", "auth_method": "API Key", "mcp_url": "https://mcp.apollo.io",
         "docs_url": "https://docs.apollo.io/", "rate_limit": "plan-based", "is_verified": True},
        {"connector_type": "Clay Native", "auth_method": "API Key", "docs_url": "https://www.clay.com/integrations/apollo", "is_verified": True},
    ],
    "zoominfo": [
        _rest("zoominfo", "https://api.zoominfo.com", "https://api-docs.zoominfo.com/", "OAuth 2.0", "enterprise"),
        {"connector_type": "MCP Server", "auth_method": "OAuth 2.0", "mcp_url": "https://mcp.zoominfo.com",
         "docs_url": "https://api-docs.zoominfo.com/", "rate_limit": "enterprise", "is_verified": True},
        {"connector_type": "Snowflake", "auth_method": "None", "docs_url": "https://www.zoominfo.com/data-cube", "is_verified": True},
    ],
    "6sense": [
        _rest("6sense", "https://api.6sense.com", "https://6sense.com/platform/", "API Key", "enterprise"),
        {"connector_type": "Snowflake", "auth_method": "None", "docs_url": "https://6sense.com/platform/", "is_verified": True},
    ],
    "clearbit": [
        _rest("clearbit", "https://person.clearbit.com/v2", "https://dashboard.clearbit.com/docs", "Bearer Token", "600/min"),
        {"connector_type": "Clay Native", "auth_method": "API Key", "docs_url": "https://www.clay.com/integrations/clearbit", "is_verified": True},
    ],
    "bombora": [
        _rest("bombora", "https://api.bombora.com", "https://bombora.com/data/", "API Key", "enterprise"),
        {"connector_type": "Snowflake", "auth_method": "None", "docs_url": "https://bombora.com/data/", "is_verified": True},
    ],
    "cognism": [
        _rest("cognism", "https://app.cognism.com/api", "https://www.cognism.com/api", "API Key", "enterprise"),
        {"connector_type": "Clay Native", "auth_method": "API Key", "docs_url": "https://www.clay.com/integrations/cognism", "is_verified": True},
    ],
    "lusha": [
        _rest("lusha", "https://api.lusha.com", "https://www.lusha.com/docs/", "API Key", "plan-based"),
        {"connector_type": "Clay Native", "auth_method": "API Key", "docs_url": "https://www.clay.com/integrations/lusha", "is_verified": True},
    ],
    "peopledatalabs": [
        _rest("peopledatalabs", "https://api.peopledatalabs.com/v5", "https://docs.peopledatalabs.com/", "API Key", "usage-based"),
        {"connector_type": "Clay Native", "auth_method": "API Key", "docs_url": "https://www.clay.com/integrations/people-data-labs", "is_verified": True},
        {"connector_type": "Snowflake", "auth_method": "None", "docs_url": "https://www.peopledatalabs.com/data", "is_verified": True},
    ],
    "crunchbase": [
        _rest("crunchbase", "https://api.crunchbase.com/api/v4", "https://data.crunchbase.com/docs", "API Key", "plan-based"),
    ],
    "hg-insights": [
        _rest("hg-insights", "https://api.hginsights.com", "https://hginsights.com/platform/", "API Key", "enterprise"),
        {"connector_type": "Snowflake", "auth_method": "None", "docs_url": "https://hginsights.com/platform/", "is_verified": True},
    ],
    "trigify": [_rest("trigify", "https://api.trigify.io", "https://trigify.io", "API Key", "plan-based")],
    "builtwith": [
        _rest("builtwith", "https://api.builtwith.com/v21/api.json", "https://api.builtwith.com/", "API Key", "plan-based"),
        {"connector_type": "Clay Native", "auth_method": "API Key", "docs_url": "https://www.clay.com/integrations/builtwith", "is_verified": True},
    ],
    "wappalyzer": [_rest("wappalyzer", "https://api.wappalyzer.com/v2", "https://www.wappalyzer.com/docs/", "API Key", "plan-based")],
    "datanyze": [_rest("datanyze", "https://api.datanyze.com", "https://www.datanyze.com", "API Key", "plan-based", verified=False)],
    "g2": [
        _rest("g2", "https://buyerintent.g2.com/api", "https://buyerintent.g2.com/", "API Key", "enterprise"),
        {"connector_type": "Snowflake", "auth_method": "None", "docs_url": "https://buyerintent.g2.com/", "is_verified": True},
    ],
    "demandbase": [
        _rest("demandbase", "https://api.demandbase.com", "https://developers.demandbase.com/", "API Key", "enterprise"),
    ],
    "warmly": [
        _rest("warmly", "https://api.warmly.ai", "https://www.warmly.ai/p/help-center", "API Key", "plan-based"),
        {"connector_type": "Webhook", "auth_method": "API Key", "docs_url": "https://www.warmly.ai/p/help-center", "is_verified": True},
    ],
    "rb2b": [
        {"connector_type": "Webhook", "auth_method": "API Key", "docs_url": "https://www.rb2b.com", "rate_limit": "real-time", "is_verified": True},
        _rest("rb2b", "https://api.rb2b.com", "https://www.rb2b.com", "API Key", "plan-based", verified=False),
    ],
    "vector": [_rest("vector", "https://api.vector.co", "https://www.vector.co", "API Key", "plan-based", verified=False)],
    "koala": [
        _rest("koala", "https://api.getkoala.com", "https://getkoala.com/docs", "API Key", "plan-based"),
        {"connector_type": "Webhook", "auth_method": "API Key", "docs_url": "https://getkoala.com/docs", "is_verified": True},
    ],
    "common-room": [
        _rest("common-room", "https://api.commonroom.io/community/v1", "https://www.commonroom.io/docs/", "API Key", "plan-based"),
    ],
    "dealfront": [_rest("dealfront", "https://api.dealfront.com", "https://www.dealfront.com/developers/", "API Key", "plan-based")],
    "coresignal": [
        _rest("coresignal", "https://api.coresignal.com/cdapi/v2", "https://docs.coresignal.com/", "Bearer Token", "usage-based"),
        {"connector_type": "MCP Server", "auth_method": "Bearer Token", "mcp_url": "https://mcp.coresignal.com",
         "docs_url": "https://docs.coresignal.com/", "rate_limit": "usage-based", "is_verified": True},
    ],
    "crustdata": [
        _rest("crustdata", "https://api.crustdata.com", "https://docs.crustdata.com/", "Bearer Token", "usage-based"),
        {"connector_type": "MCP Server", "auth_method": "Bearer Token", "mcp_url": "https://mcp.crustdata.com",
         "docs_url": "https://docs.crustdata.com/", "rate_limit": "usage-based", "is_verified": True},
    ],
    "predictleads": [_rest("predictleads", "https://predictleads.com/api/v3", "https://docs.predictleads.com/", "API Key", "plan-based")],
    "hunter-io": [
        _rest("hunter-io", "https://api.hunter.io/v2", "https://hunter.io/api-documentation/v2", "API Key", "plan-based"),
        {"connector_type": "Clay Native", "auth_method": "API Key", "docs_url": "https://www.clay.com/integrations/hunter", "is_verified": True},
    ],
    "prospeo": [
        _rest("prospeo", "https://api.prospeo.io", "https://prospeo.io/api", "API Key", "usage-based"),
        {"connector_type": "Clay Native", "auth_method": "API Key", "docs_url": "https://www.clay.com/integrations/prospeo", "is_verified": True},
    ],
    "leadmagic": [
        _rest("leadmagic", "https://api.leadmagic.io", "https://docs.leadmagic.io/", "API Key", "usage-based"),
        {"connector_type": "Clay Native", "auth_method": "API Key", "docs_url": "https://www.clay.com/integrations/leadmagic", "is_verified": True},
    ],
    "findymail": [_rest("findymail", "https://app.findymail.com/api", "https://www.findymail.com/api", "API Key", "usage-based")],
    "ocean-io": [_rest("ocean-io", "https://api.ocean.io", "https://www.ocean.io", "API Key", "plan-based")],
    "harmonic": [
        _rest("harmonic", "https://api.harmonic.ai", "https://console.harmonic.ai/docs", "API Key", "plan-based"),
    ],
    "explorium": [
        _rest("explorium", "https://api.explorium.ai", "https://www.explorium.ai/data/", "API Key", "enterprise"),
    ],
}

# ---------------------------------------------------------------------------
# AGGREGATOR -> PROVIDERS  (aggregator_providers junction)
# aggregator_name must match existing aggregators table names.
# integration_depth in: "Native — built-in, no config" | "Deep — full API surface" | "Partial — limited fields"
# ---------------------------------------------------------------------------
NATIVE = "Native — built-in, no config"
DEEP = "Deep — full API surface"
PARTIAL = "Partial — limited fields"

AGGREGATOR_PROVIDERS = {
    "Clay": [("apollo-io", NATIVE), ("clearbit", NATIVE), ("cognism", NATIVE), ("lusha", NATIVE),
             ("peopledatalabs", NATIVE), ("hunter-io", NATIVE), ("prospeo", NATIVE), ("leadmagic", NATIVE),
             ("builtwith", NATIVE), ("zoominfo", DEEP), ("crustdata", NATIVE), ("findymail", NATIVE),
             ("ocean-io", PARTIAL)],
    "N8N": [("apollo-io", DEEP), ("zoominfo", DEEP), ("hunter-io", DEEP), ("clearbit", DEEP),
            ("coresignal", DEEP), ("crustdata", DEEP)],
    "Relay.app": [("apollo-io", DEEP), ("clearbit", DEEP), ("hunter-io", DEEP)],
    "Make": [("apollo-io", DEEP), ("hunter-io", DEEP), ("clearbit", DEEP), ("lusha", PARTIAL)],
    "Zapier": [("apollo-io", PARTIAL), ("hunter-io", DEEP), ("lusha", PARTIAL), ("clearbit", PARTIAL)],
    "Bardeen": [("apollo-io", PARTIAL), ("clearbit", PARTIAL)],
}
