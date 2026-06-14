"""Transforms Zite tables into a force-graph payload (nodes + links) and provider details.
Visual identity (locked):
  providers (galaxies)  -> #E8600A  size 18-32 by node_size
  signal_type Entity (suns) / Signal (planets) -> #E8A01E  size 8-14
  signal_type Property (stars) -> #1EE8D8  size 4-8
  aggregators (orchestration hubs) -> rendered as galaxies, flagged isAggregator
"""
import zite_client as zite

PROVIDER_COLOR = "#E8600A"
SIGNAL_COLOR = "#E8A01E"
PROPERTY_COLOR = "#1EE8D8"
AGG_COLOR = "#E8600A"

ALL_UNIVERSES = ["Intent", "Enrichment", "Technographic", "MCP Hub"]
UNI_SLUG = {"intent": "Intent", "enrichment": "Enrichment",
            "technographic": "Technographic", "mcp_hub": "MCP Hub"}


def _provider_size(node_size):
    try:
        n = float(node_size or 2)
    except (TypeError, ValueError):
        n = 2
    n = max(1, min(5, n))
    return round(16 + n * 3.2, 1)  # 1->19.2 .. 5->32


def _signal_size(signal_type, providers_count=1):
    base = max(1, min(providers_count, 6))
    if signal_type == "Property":
        return round(4 + base * 0.7, 1)          # 4-8
    if signal_type == "Entity":
        return round(10 + base * 0.7, 1)         # 10-14 (suns, slightly bigger)
    return round(8 + base * 1.0, 1)              # Signal planets 8-14


def _agg_size(node_size):
    try:
        n = float(node_size or 3)
    except (TypeError, ValueError):
        n = 3
    return round(15 + max(1, min(5, n)) * 2.6, 1)


async def build_graph():
    data = await zite.get_all_tables()
    providers = data["providers"]
    signals = data["signals"]
    aggregators = data["aggregators"]
    provider_signals = data["provider_signals"]
    aggregator_providers = data["aggregator_providers"]

    nodes = []
    links = []
    seen = set()

    # how many providers serve each signal (for sizing)
    sig_provider_count = {}
    for j in provider_signals:
        sn = (j["fields"].get("signal_name") or "").strip()
        if sn:
            sig_provider_count[sn] = sig_provider_count.get(sn, 0) + 1

    # ---- provider nodes ----
    prov_name_to_id = {}
    for p in providers:
        f = p["fields"]
        name = f.get("name")
        if not name:
            continue
        nid = f"provider::{f.get('slug') or name}"
        prov_name_to_id[name] = nid
        if nid in seen:
            continue
        seen.add(nid)
        nodes.append({
            "id": nid,
            "label": name,
            "slug": f.get("slug"),
            "type": "provider",
            "color": PROVIDER_COLOR,
            "size": _provider_size(f.get("node_size")),
            "universes": f.get("universes") or [],
            "pricing_tier": f.get("pricing_tier"),
            "coverage_summary": f.get("coverage_summary"),
            "description": f.get("description"),
        })

    # ---- signal nodes ----
    sig_name_to_id = {}
    for s in signals:
        f = s["fields"]
        name = f.get("name")
        if not name:
            continue
        nid = f"signal::{f.get('slug') or name}"
        sig_name_to_id[name] = nid
        if nid in seen:
            continue
        seen.add(nid)
        stype = f.get("signal_type") or "Signal"
        nodes.append({
            "id": nid,
            "label": name,
            "slug": f.get("slug"),
            "type": "signal",
            "signal_type": stype,
            "color": PROPERTY_COLOR if stype == "Property" else SIGNAL_COLOR,
            "size": _signal_size(stype, sig_provider_count.get(name, 1)),
            "universes": [f.get("universe")] if f.get("universe") else [],
            "field_type": f.get("field_type"),
            "update_cadence": f.get("update_cadence"),
            "description": f.get("description"),
        })

    # ---- aggregator nodes ----
    agg_name_to_id = {}
    for a in aggregators:
        f = a["fields"]
        name = f.get("name")
        if not name:
            continue
        nid = f"aggregator::{f.get('slug') or name}"
        agg_name_to_id[name] = nid
        if nid in seen:
            continue
        seen.add(nid)
        nodes.append({
            "id": nid,
            "label": name,
            "slug": f.get("slug"),
            "type": "aggregator",
            "color": AGG_COLOR,
            "size": _agg_size(f.get("node_size")),
            "isAggregator": True,
            "universes": ALL_UNIVERSES,  # orchestration hubs span all universes
            "aggregator_type": f.get("aggregator_type"),
            "has_mcp": bool(f.get("has_mcp")),
            "description": f.get("description"),
        })

    # ---- links: provider <-> signal ----
    for j in provider_signals:
        f = j["fields"]
        pn = (f.get("provider_name") or "").strip()
        sn = (f.get("signal_name") or "").strip()
        src = prov_name_to_id.get(pn)
        tgt = sig_name_to_id.get(sn)
        if src and tgt:
            links.append({"source": src, "target": tgt, "kind": "provider_signal",
                          "quality": f.get("coverage_quality")})

    # ---- links: aggregator <-> provider ----
    for j in aggregator_providers:
        f = j["fields"]
        an = (f.get("aggregator_name") or "").strip()
        pn = (f.get("provider_name") or "").strip()
        src = agg_name_to_id.get(an)
        tgt = prov_name_to_id.get(pn)
        if src and tgt:
            links.append({"source": src, "target": tgt, "kind": "aggregator_provider",
                          "depth": f.get("integration_depth")})

    return {"nodes": nodes, "links": links,
            "stats": {"providers": len(prov_name_to_id), "signals": len(sig_name_to_id),
                      "aggregators": len(agg_name_to_id), "links": len(links)}}


async def list_universes():
    rows = await zite.get_table("universes")
    items = [{"name": r["fields"].get("name"), "slug": r["fields"].get("slug"),
             "description": r["fields"].get("description"), "color_hex": r["fields"].get("color_hex"),
             "icon": r["fields"].get("icon"), "display_order": r["fields"].get("display_order") or 0}
            for r in rows]
    items.sort(key=lambda x: x["display_order"])
    return items


async def list_providers():
    rows = await zite.get_table("providers")
    out = []
    for r in rows:
        f = r["fields"]
        if not f.get("name"):
            continue
        out.append({"name": f.get("name"), "slug": f.get("slug"),
                    "description": f.get("description"), "pricing_tier": f.get("pricing_tier"),
                    "coverage_summary": f.get("coverage_summary"), "universes": f.get("universes") or [],
                    "website_url": f.get("website_url"), "docs_url": f.get("docs_url"),
                    "node_size": f.get("node_size")})
    out.sort(key=lambda x: (-(x.get("node_size") or 0), x["name"]))
    return out


async def provider_detail(slug):
    data = await zite.get_all_tables()
    prov = next((r for r in data["providers"] if r["fields"].get("slug") == slug), None)
    if not prov:
        return None
    f = prov["fields"]
    name = f.get("name")

    connectors = [
        {"connector_type": c["fields"].get("connector_type"),
         "auth_method": c["fields"].get("auth_method"),
         "endpoint_url": c["fields"].get("endpoint_url"),
         "mcp_url": c["fields"].get("mcp_url"),
         "docs_url": c["fields"].get("docs_url"),
         "rate_limit": c["fields"].get("rate_limit"),
         "is_verified": bool(c["fields"].get("is_verified"))}
        for c in data["connectors"] if (c["fields"].get("provider_name") or "").strip() == name
    ]
    signals = [
        {"signal_name": j["fields"].get("signal_name"),
         "coverage_quality": j["fields"].get("coverage_quality"),
         "slug": _signal_slug(data["signals"], j["fields"].get("signal_name"))}
        for j in data["provider_signals"] if (j["fields"].get("provider_name") or "").strip() == name
    ]
    aggregators = [
        {"aggregator_name": j["fields"].get("aggregator_name"),
         "integration_depth": j["fields"].get("integration_depth")}
        for j in data["aggregator_providers"] if (j["fields"].get("provider_name") or "").strip() == name
    ]
    mcp_url = next((c["mcp_url"] for c in connectors if c.get("mcp_url")), None)

    return {
        "name": name, "slug": f.get("slug"), "description": f.get("description"),
        "website_url": f.get("website_url"), "docs_url": f.get("docs_url"),
        "pricing_tier": f.get("pricing_tier"), "coverage_summary": f.get("coverage_summary"),
        "universes": f.get("universes") or [], "node_size": f.get("node_size"),
        "connectors": connectors, "signals": signals, "aggregators": aggregators,
        "mcp_url": mcp_url,
    }


def _signal_slug(signals, name):
    if not name:
        return None
    r = next((s for s in signals if s["fields"].get("name") == name), None)
    return r["fields"].get("slug") if r else None


async def grounding_context():
    """Compact text context of the entire graph for the AI assistant."""
    data = await zite.get_all_tables()
    lines = ["PROVIDERS (galaxies):"]
    # signals per provider
    psig = {}
    for j in data["provider_signals"]:
        pn = j["fields"].get("provider_name"); sn = j["fields"].get("signal_name")
        if pn and sn:
            psig.setdefault(pn, []).append(sn)
    for p in data["providers"]:
        f = p["fields"]
        if not f.get("name"):
            continue
        sigs = ", ".join(psig.get(f["name"], [])[:8])
        lines.append(f"- {f['name']} [{f.get('pricing_tier')}] universes={f.get('universes')}: "
                     f"{(f.get('description') or '')[:140]} | signals: {sigs}")
    lines.append("\nSIGNALS (planets/stars):")
    for s in data["signals"]:
        f = s["fields"]
        if not f.get("name"):
            continue
        lines.append(f"- {f['name']} ({f.get('signal_type')}, {f.get('universe')}): {(f.get('description') or '')[:110]}")
    lines.append("\nAGGREGATORS (orchestration hubs):")
    for a in data["aggregators"]:
        f = a["fields"]
        if not f.get("name"):
            continue
        lines.append(f"- {f['name']} ({f.get('aggregator_type')}, mcp={bool(f.get('has_mcp'))})")
    names = ([p["fields"].get("name") for p in data["providers"] if p["fields"].get("name")]
             + [s["fields"].get("name") for s in data["signals"] if s["fields"].get("name")]
             + [a["fields"].get("name") for a in data["aggregators"] if a["fields"].get("name")])
    return "\n".join(lines), names


async def list_signals():
    """Catalog of all data points (Entity/Signal/Property) with their providers."""
    data = await zite.get_all_tables()
    prov_slug_by_name = {p["fields"].get("name"): p["fields"].get("slug")
                         for p in data["providers"] if p["fields"].get("name")}
    # providers per signal
    by_signal = {}
    for j in data["provider_signals"]:
        f = j["fields"]
        sn = (f.get("signal_name") or "").strip()
        pn = (f.get("provider_name") or "").strip()
        if not sn or not pn:
            continue
        by_signal.setdefault(sn, []).append(
            {"name": pn, "slug": prov_slug_by_name.get(pn), "quality": f.get("coverage_quality")})
    quality_rank = {"Primary": 0, "Secondary": 1, "Limited": 2}
    out = []
    for s in data["signals"]:
        f = s["fields"]
        if not f.get("name"):
            continue
        provs = by_signal.get(f["name"], [])
        provs.sort(key=lambda x: (quality_rank.get(x.get("quality"), 3), x["name"]))
        out.append({
            "name": f.get("name"), "slug": f.get("slug"),
            "signal_type": f.get("signal_type") or "Signal",
            "universe": f.get("universe"), "field_name": f.get("field_name"),
            "field_type": f.get("field_type"), "update_cadence": f.get("update_cadence"),
            "description": f.get("description"), "providers": provs,
            "provider_count": len(provs),
        })
    # order: Property, Signal, Entity then by provider_count desc
    type_rank = {"Property": 0, "Signal": 1, "Entity": 2}
    out.sort(key=lambda x: (type_rank.get(x["signal_type"], 3), -x["provider_count"], x["name"]))
    return out


async def list_crawl_jobs():
    rows = await zite.get_table("crawl_jobs")
    return [{"provider_name": r["fields"].get("provider_name"), "status": r["fields"].get("status"),
             "target_url": r["fields"].get("target_url"), "fields_extracted": r["fields"].get("fields_extracted"),
             "confidence_score": r["fields"].get("confidence_score"), "created_at": r["fields"].get("created_at")}
            for r in rows]
