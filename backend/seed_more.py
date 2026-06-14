"""
Additive, idempotent seed of NEW data properties/signals discovered from the
Crustdata API docs (company, person, job, web, social areas). Re-runnable:
only creates signals/junctions that don't already exist (by slug / label).

Run: cd /app/backend && python seed_more.py
"""
import os, time, requests
from dotenv import load_dotenv

load_dotenv()
KEY = os.environ["ZITE_API_KEY"]; BASE_ID = os.environ["ZITE_BASE_ID"]; API = os.environ["ZITE_API_URL"]
HEAD = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
T = {"providers": "tjynJoa3Z9k", "signals": "tfbPMxULzzJ", "provider_signals": "tuDAEwuWL85"}

# ---- NEW real data points (mostly Properties — Crustdata-inspired) ----
NEW_SIGNALS = [
    {"slug": "year-founded", "name": "Year Founded", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "basic_info.year_founded", "field_type": "Number", "update_cadence": "On Request",
     "description": "The year a company was founded — used for maturity and segmentation."},
    {"slug": "total-funding", "name": "Total Funding Raised", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "funding.total_investment_usd", "field_type": "Number", "update_cadence": "Weekly",
     "description": "Cumulative capital a company has raised across all rounds (USD)."},
    {"slug": "last-funding-round", "name": "Last Funding Round", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "funding.last_round", "field_type": "Object", "update_cadence": "Daily",
     "description": "Type, size and date of the most recent funding round."},
    {"slug": "investors", "name": "Investors / Cap Table", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "funding.investors", "field_type": "Array", "update_cadence": "Weekly",
     "description": "The investors backing a company — useful for warm-intro pathing."},
    {"slug": "headcount-by-department", "name": "Headcount by Department", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "headcount.by_department", "field_type": "Object", "update_cadence": "Weekly",
     "description": "Employee distribution across functions (Eng, Sales, Marketing, etc.)."},
    {"slug": "web-traffic", "name": "Web Traffic", "signal_type": "Property", "universe": "Technographic",
     "field_name": "web_traffic.monthly_visits", "field_type": "Number", "update_cadence": "Weekly",
     "description": "Estimated monthly website visits — a proxy for company scale and demand."},
    {"slug": "web-traffic-growth", "name": "Web Traffic Growth", "signal_type": "Signal", "universe": "Intent",
     "field_name": "web_traffic.growth", "field_type": "Number", "update_cadence": "Weekly",
     "description": "Month-over-month change in web traffic — a momentum signal."},
    {"slug": "glassdoor-rating", "name": "Glassdoor Rating", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "reviews.glassdoor_rating", "field_type": "Number", "update_cadence": "Weekly",
     "description": "Employer rating on Glassdoor — a culture and stability indicator."},
    {"slug": "g2-rating", "name": "G2 Rating", "signal_type": "Property", "universe": "Technographic",
     "field_name": "reviews.g2_rating", "field_type": "Number", "update_cadence": "Weekly",
     "description": "Average product rating on G2 — software quality / market perception."},
    {"slug": "linkedin-followers", "name": "LinkedIn Followers", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "social.linkedin_followers", "field_type": "Number", "update_cadence": "Weekly",
     "description": "Company LinkedIn follower count — brand reach and audience size."},
    {"slug": "linkedin-follower-growth", "name": "LinkedIn Follower Growth", "signal_type": "Signal", "universe": "Intent",
     "field_name": "social.linkedin_follower_growth", "field_type": "Number", "update_cadence": "Weekly",
     "description": "Rate of LinkedIn follower growth — a brand-momentum signal."},
    {"slug": "social-followers", "name": "Social Follower Count", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "social.x_followers", "field_type": "Number", "update_cadence": "Weekly",
     "description": "X/Twitter follower count for a company or person."},
    {"slug": "decision-makers", "name": "Decision Makers", "signal_type": "Entity", "universe": "Enrichment",
     "field_name": "decision_makers", "field_type": "Array", "update_cadence": "On Request",
     "description": "Key decision-maker contacts at an account (by seniority & function)."},
    {"slug": "open-roles-count", "name": "Open Roles Count", "signal_type": "Property", "universe": "Intent",
     "field_name": "jobs.open_count", "field_type": "Number", "update_cadence": "Daily",
     "description": "Current number of open job listings at a company."},
    {"slug": "job-openings-by-function", "name": "Job Openings by Function", "signal_type": "Property", "universe": "Intent",
     "field_name": "jobs.by_function", "field_type": "Object", "update_cadence": "Daily",
     "description": "Open roles broken down by department — shows where a company is investing."},
    {"slug": "news-mention", "name": "News Mention", "signal_type": "Signal", "universe": "Intent",
     "field_name": "web.news_mention", "field_type": "Object", "update_cadence": "Real-time",
     "description": "A company is mentioned in the news — a timely conversation trigger."},
    {"slug": "employee-skills", "name": "Employee Skills", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "headcount.skills_distribution", "field_type": "Array", "update_cadence": "Weekly",
     "description": "Aggregate skills across a company's workforce — capability mapping."},
    {"slug": "normalized-title", "name": "Normalized Title", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "basic_profile.normalized_title", "field_type": "String", "update_cadence": "On Request",
     "description": "A standardized job-title classification for consistent persona targeting."},
    {"slug": "years-experience", "name": "Years of Experience", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "experience.years_total", "field_type": "Number", "update_cadence": "On Request",
     "description": "Total professional experience of a contact in years."},
    {"slug": "past-companies", "name": "Past Companies", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "experience.employment_details", "field_type": "Array", "update_cadence": "On Request",
     "description": "A contact's employment history — powers champion & alumni plays."},
    {"slug": "education-history", "name": "Education History", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "education.schools", "field_type": "Array", "update_cadence": "On Request",
     "description": "Schools, degrees and fields of study for a contact."},
    {"slug": "linkedin-connections", "name": "LinkedIn Connections", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "professional_network.connections", "field_type": "Number", "update_cadence": "On Request",
     "description": "A contact's LinkedIn connection count — network influence proxy."},
    {"slug": "profile-headline", "name": "Profile Headline", "signal_type": "Property", "universe": "Enrichment",
     "field_name": "basic_profile.headline", "field_type": "String", "update_cadence": "On Request",
     "description": "A contact's self-written LinkedIn headline — context for personalization."},
    {"slug": "recent-social-posts", "name": "Recent Social Posts", "signal_type": "Signal", "universe": "Intent",
     "field_name": "social_posts.recent", "field_type": "Array", "update_cadence": "Real-time",
     "description": "Recent LinkedIn/X posts by a person or company — engagement openers."},
]

P, S, L, ALL = "Primary", "Secondary", "Limited", None
NEW_LINKS = {
    "crustdata": [("year-founded", S), ("total-funding", P), ("headcount-by-department", P), ("web-traffic", P),
                  ("web-traffic-growth", P), ("glassdoor-rating", P), ("g2-rating", S), ("linkedin-followers", P),
                  ("linkedin-follower-growth", P), ("social-followers", S), ("decision-makers", P),
                  ("open-roles-count", P), ("job-openings-by-function", P), ("news-mention", P),
                  ("employee-skills", P), ("normalized-title", P), ("years-experience", P), ("past-companies", P),
                  ("education-history", P), ("linkedin-connections", P), ("profile-headline", P),
                  ("recent-social-posts", P), ("investors", S), ("last-funding-round", S)],
    "harmonic": [("total-funding", P), ("last-funding-round", P), ("investors", P), ("year-founded", S),
                 ("headcount-by-department", S)],
    "crunchbase": [("total-funding", P), ("last-funding-round", P), ("investors", P), ("year-founded", P)],
    "coresignal": [("headcount-by-department", P), ("open-roles-count", P), ("job-openings-by-function", P),
                   ("linkedin-followers", S), ("past-companies", S), ("employee-skills", S)],
    "predictleads": [("open-roles-count", P), ("job-openings-by-function", P), ("news-mention", P)],
    "g2": [("g2-rating", P)],
    "peopledatalabs": [("normalized-title", P), ("years-experience", P), ("past-companies", P),
                       ("education-history", P), ("employee-skills", S)],
    "apollo-io": [("decision-makers", S), ("normalized-title", S)],
    "zoominfo": [("decision-makers", P), ("web-traffic", S), ("news-mention", S)],
    "common-room": [("recent-social-posts", P), ("news-mention", S)],
    "trigify": [("recent-social-posts", P), ("profile-headline", S)],
    "explorium": [("web-traffic", S), ("news-mention", L)],
    "clearbit": [("linkedin-followers", S), ("social-followers", S)],
}


def _req(method, url, **kw):
    for a in range(5):
        r = requests.request(method, url, headers=HEAD, timeout=40, **kw)
        if r.status_code == 429:
            time.sleep(1.2 * (a + 1)); continue
        return r
    return r


def list_all(table):
    out, off = [], 0
    while True:
        r = _req("POST", f"{API}/bases/{BASE_ID}/tables/{T[table]}/records/list", json={"limit": 500, "offset": off})
        r.raise_for_status(); d = r.json(); out.extend(d["records"])
        if not d.get("hasMore"):
            break
        off += 500
    return out


def create(table, rec):
    r = _req("POST", f"{API}/bases/{BASE_ID}/tables/{T[table]}/records", json={"record": rec})
    if r.status_code not in (200, 201):
        raise RuntimeError(f"create {table} {r.status_code}: {r.text[:200]}")
    time.sleep(0.04); return r.json()


def main():
    provs = list_all("providers"); sigs = list_all("signals"); links = list_all("provider_signals")
    prov_id = {r["fields"].get("slug"): r["id"] for r in provs if r["fields"].get("slug")}
    prov_name = {r["fields"].get("slug"): r["fields"].get("name") for r in provs if r["fields"].get("slug")}
    sig_by_slug = {r["fields"].get("slug"): r for r in sigs if r["fields"].get("slug")}
    existing_labels = {r["fields"].get("label") for r in links}

    new_sig = 0
    for s in NEW_SIGNALS:
        if s["slug"] in sig_by_slug:
            continue
        r = create("signals", {"name": s["name"], "slug": s["slug"], "signal_type": s["signal_type"],
                               "universe": s["universe"], "description": s["description"],
                               "field_name": s["field_name"], "field_type": s["field_type"],
                               "update_cadence": s["update_cadence"], "provider_name": ""})
        sig_by_slug[s["slug"]] = r; new_sig += 1
        print(f"  + signal {s['name']}")
    sig_id = {slug: row["id"] for slug, row in sig_by_slug.items()}
    sig_name = {s["slug"]: s["name"] for s in NEW_SIGNALS}
    sig_name.update({r["fields"].get("slug"): r["fields"].get("name") for r in sigs if r["fields"].get("slug")})

    new_link = 0
    for pslug, items in NEW_LINKS.items():
        for sslug, quality in items:
            label = f"{pslug}::{sslug}"
            if label in existing_labels:
                continue
            rec = {"label": label, "provider_name": prov_name.get(pslug, pslug),
                   "signal_name": sig_name.get(sslug, sslug)}
            if quality:
                rec["coverage_quality"] = quality
            if prov_id.get(pslug):
                rec["providers"] = [prov_id[pslug]]
            if sig_id.get(sslug):
                rec["signals"] = [sig_id[sslug]]
            create("provider_signals", rec); new_link += 1
    print(f"\n✅ added {new_sig} new signals, {new_link} new provider_signals links")
    print(f"  signals total now: {len(list_all('signals'))}")
    print(f"  provider_signals total now: {len(list_all('provider_signals'))}")


if __name__ == "__main__":
    main()
