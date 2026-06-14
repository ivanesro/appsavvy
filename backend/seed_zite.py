"""
Idempotent seeder for the appsaavy.space Zite database.
- Upserts providers & signals by `slug`.
- Upserts connectors / provider_signals / aggregator_providers / provider_universes by a unique `label`.
- Sets both denormalized name fields AND linked_record fields so edges are robust.

Run: cd /app/backend && python seed_zite.py
"""
import os
import time
import requests
from dotenv import load_dotenv
import seed_data as D

load_dotenv()

KEY = os.environ["ZITE_API_KEY"]
BASE_ID = os.environ["ZITE_BASE_ID"]
API = os.environ["ZITE_API_URL"]
HEAD = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

T = {
    "providers": "tjynJoa3Z9k",
    "signals": "tfbPMxULzzJ",
    "universes": "tx3ax8wwSnj",
    "provider_universes": "tg3gnEwKv56",
    "provider_signals": "tuDAEwuWL85",
    "aggregators": "toKLFjsZ5hK",
    "aggregator_providers": "tnoaYzkwLBH",
    "connectors": "tfgYfRx6uie",
}


def _req(method, url, **kw):
    for attempt in range(5):
        r = requests.request(method, url, headers=HEAD, timeout=40, **kw)
        if r.status_code == 429:
            time.sleep(1.5 * (attempt + 1)); continue
        return r
    return r


def list_all(table):
    out, offset = [], 0
    while True:
        r = _req("POST", f"{API}/bases/{BASE_ID}/tables/{T[table]}/records/list", json={"limit": 500, "offset": offset})
        r.raise_for_status()
        d = r.json()
        out.extend(d["records"])
        if not d.get("hasMore"):
            break
        offset += 500
    return out


def create(table, record):
    r = _req("POST", f"{API}/bases/{BASE_ID}/tables/{T[table]}/records", json={"record": record})
    if r.status_code not in (200, 201):
        raise RuntimeError(f"CREATE {table} failed {r.status_code}: {r.text[:300]} | rec={record}")
    time.sleep(0.04)
    return r.json()


def update(table, rec_id, record):
    r = _req("PATCH", f"{API}/bases/{BASE_ID}/tables/{T[table]}/records/{rec_id}", json={"record": record})
    if r.status_code not in (200, 201):
        # some deployments use PUT
        r = _req("PUT", f"{API}/bases/{BASE_ID}/tables/{T[table]}/records/{rec_id}", json={"record": record})
    time.sleep(0.04)
    return r.status_code in (200, 201)


def main():
    print("Loading existing records...")
    prov_rows = list_all("providers")
    sig_rows = list_all("signals")
    uni_rows = list_all("universes")
    agg_rows = list_all("aggregators")
    ps_rows = list_all("provider_signals")
    ap_rows = list_all("aggregator_providers")
    pu_rows = list_all("provider_universes")
    conn_rows = list_all("connectors")

    prov_by_slug = {r["fields"].get("slug"): r for r in prov_rows if r["fields"].get("slug")}
    sig_by_slug = {r["fields"].get("slug"): r for r in sig_rows if r["fields"].get("slug")}
    uni_by_slug = {r["fields"].get("slug"): r for r in uni_rows if r["fields"].get("slug")}
    agg_by_name = {r["fields"].get("name"): r for r in agg_rows if r["fields"].get("name")}

    # ---------- PROVIDERS ----------
    print(f"\nProviders: {len(prov_by_slug)} existing")
    for p in D.PROVIDERS:
        rec = {
            "name": p["name"], "slug": p["slug"], "description": p["description"],
            "website_url": p["website_url"], "docs_url": p["docs_url"],
            "pricing_tier": p["pricing_tier"], "coverage_summary": p["coverage_summary"],
            "universes": p["universes"], "node_size": p["node_size"],
        }
        if p["slug"] in prov_by_slug:
            ex = prov_by_slug[p["slug"]]
            ok = update("providers", ex["id"], rec)
            print(f"  ~ updated {p['name']} ({'ok' if ok else 'noop'})")
        else:
            r = create("providers", rec)
            prov_by_slug[p["slug"]] = r
            print(f"  + created {p['name']}")

    # refresh provider map (ids)
    prov_id = {slug: row["id"] for slug, row in prov_by_slug.items()}

    # ---------- SIGNALS ----------
    print(f"\nSignals: {len(sig_by_slug)} existing")
    for s in D.SIGNALS:
        rec = {
            "name": s["name"], "slug": s["slug"], "signal_type": s["signal_type"],
            "universe": s["universe"], "description": s["description"],
            "field_name": s["field_name"], "field_type": s["field_type"],
            "update_cadence": s["update_cadence"], "provider_name": "",
        }
        if s["slug"] in sig_by_slug:
            ex = sig_by_slug[s["slug"]]
            update("signals", ex["id"], rec)
        else:
            r = create("signals", rec)
            sig_by_slug[s["slug"]] = r
            print(f"  + signal {s['name']}")
    sig_id = {slug: row["id"] for slug, row in sig_by_slug.items()}

    # ---------- CONNECTORS ----------
    existing_conn = {r["fields"].get("label") for r in conn_rows}
    print(f"\nConnectors: {len(existing_conn)} existing")
    c_count = 0
    for pslug, conns in D.CONNECTORS.items():
        pname = next((p["name"] for p in D.PROVIDERS if p["slug"] == pslug), pslug)
        for c in conns:
            label = f"{pslug}::{c['connector_type']}"
            if label in existing_conn:
                continue
            rec = {"label": label, "provider_name": pname, "connector_type": c["connector_type"],
                   "is_verified": c.get("is_verified", True)}
            for k in ("auth_method", "endpoint_url", "mcp_url", "docs_url", "rate_limit"):
                if c.get(k):
                    rec[k] = c[k]
            create("connectors", rec)
            c_count += 1
    print(f"  + created {c_count} connectors")

    # ---------- PROVIDER_SIGNALS ----------
    existing_ps = {r["fields"].get("label") for r in ps_rows}
    print(f"\nprovider_signals: {len(existing_ps)} existing")
    ps_count = 0
    for pslug, sigs in D.PROVIDER_SIGNALS.items():
        pname = next((p["name"] for p in D.PROVIDERS if p["slug"] == pslug), pslug)
        pid = prov_id.get(pslug)
        for sslug, quality in sigs:
            sname = next((s["name"] for s in D.SIGNALS if s["slug"] == sslug), sslug)
            label = f"{pslug}::{sslug}"
            if label in existing_ps:
                continue
            rec = {"label": label, "provider_name": pname, "signal_name": sname,
                   "coverage_quality": quality}
            if pid:
                rec["providers"] = [pid]
            if sig_id.get(sslug):
                rec["signals"] = [sig_id[sslug]]
            create("provider_signals", rec)
            ps_count += 1
    print(f"  + created {ps_count} provider_signals")

    # ---------- AGGREGATOR_PROVIDERS ----------
    existing_ap = {r["fields"].get("label") for r in ap_rows}
    print(f"\naggregator_providers: {len(existing_ap)} existing")
    ap_count = 0
    for aname, provs in D.AGGREGATOR_PROVIDERS.items():
        agg_row = agg_by_name.get(aname)
        aid = agg_row["id"] if agg_row else None
        for pslug, depth in provs:
            pname = next((p["name"] for p in D.PROVIDERS if p["slug"] == pslug), pslug)
            pid = prov_id.get(pslug)
            label = f"{aname}::{pslug}"
            if label in existing_ap:
                continue
            rec = {"label": label, "aggregator_name": aname, "provider_name": pname,
                   "integration_depth": depth}
            if aid:
                rec["aggregators"] = [aid]
            if pid:
                rec["providers"] = [pid]
            create("aggregator_providers", rec)
            ap_count += 1
    print(f"  + created {ap_count} aggregator_providers")

    # ---------- PROVIDER_UNIVERSES ----------
    existing_pu = set()
    for r in pu_rows:
        existing_pu.add((r["fields"].get("provider_name"), r["fields"].get("universe_slug")))
    uni_slug_by_label = {"Intent": "intent", "Enrichment": "enrichment",
                         "Technographic": "technographic", "MCP Hub": "mcp_hub"}
    print(f"\nprovider_universes: {len(existing_pu)} existing")
    pu_count = 0
    for p in D.PROVIDERS:
        pid = prov_id.get(p["slug"])
        for ulabel in p["universes"]:
            uslug = uni_slug_by_label.get(ulabel, ulabel.lower())
            if (p["name"], uslug) in existing_pu:
                continue
            rec = {"provider_name": p["name"], "universe_slug": uslug}
            if pid:
                rec["providers"] = [pid]
            urow = uni_by_slug.get(uslug)
            if urow:
                rec["universes"] = [urow["id"]]
            create("provider_universes", rec)
            pu_count += 1
    print(f"  + created {pu_count} provider_universes")

    print("\n✅ SEED COMPLETE")
    for t in T:
        print(f"  {t:22s}: {len(list_all(t))} rows")


if __name__ == "__main__":
    main()
