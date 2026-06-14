import React, { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Search, Network, LayoutGrid, Clock, Database, ArrowRight } from "lucide-react";
import { fetchSignals } from "../lib/api";

const TYPE_META = {
  Property: { color: "#1EE8D8", label: "Property", glyph: "Planet" },
  Signal: { color: "#E8A01E", label: "Signal", glyph: "Sun" },
  Entity: { color: "#E8600A", label: "Entity", glyph: "Sun" },
};
const TYPE_FILTERS = ["All", "Property", "Signal", "Entity"];
const UNI_FILTERS = ["All", "Intent", "Enrichment", "Technographic", "MCP Hub"];

const QCOLOR = { Primary: "var(--signal)", Secondary: "var(--muted)", Limited: "var(--faint)" };

export default function CatalogView() {
  const navigate = useNavigate();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [type, setType] = useState("All");
  const [uni, setUni] = useState("All");
  const [q, setQ] = useState("");

  useEffect(() => {
    fetchSignals().then((d) => { setItems(d); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  const providerCount = useMemo(() => {
    const s = new Set();
    items.forEach((i) => i.providers.forEach((p) => s.add(p.name)));
    return s.size;
  }, [items]);

  const filtered = useMemo(() => {
    return items.filter((i) => {
      if (type !== "All" && i.signal_type !== type) return false;
      if (uni !== "All" && i.universe !== uni) return false;
      if (q) {
        const hay = `${i.name} ${i.description} ${i.field_name} ${i.providers.map((p) => p.name).join(" ")}`.toLowerCase();
        if (!hay.includes(q.toLowerCase())) return false;
      }
      return true;
    });
  }, [items, type, uni, q]);

  return (
    <div className="catalog-page" data-testid="catalog-page">
      <div className="topbar catalog-topbar">
        <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
          <a href="/" className="logo">appsaavy<span className="dot">.</span>space</a>
          <div className="nav-seg">
            <button className="nav-pill" data-testid="nav-graph" onClick={() => navigate("/")}><Network size={12} /> Graph</button>
            <button className="nav-pill active" data-testid="nav-catalog"><LayoutGrid size={12} /> Catalog</button>
          </div>
        </div>
        <div />
        <div style={{ width: 190 }} />
      </div>

      <div className="catalog-scroll">
        <div className="catalog-wrap">
          <div className="catalog-hero">
            <div className="gp-label">Signal Catalog</div>
            <h1 className="catalog-title">The data points builders can wire up</h1>
            <p className="catalog-sub">
              {loading ? "Loading…" : `${items.length} data points · ${providerCount} providers · browse every property, signal & entity in the graph`}
            </p>
          </div>

          <div className="catalog-filters">
            <div className="filter-group" data-testid="type-filters">
              {TYPE_FILTERS.map((t) => (
                <button key={t} className={`chip ${type === t ? "on" : ""}`} data-testid={`type-${t.toLowerCase()}`} onClick={() => setType(t)}>
                  {t !== "All" && <span className="chip-dot" style={{ background: TYPE_META[t]?.color }} />}{t}
                </button>
              ))}
            </div>
            <div className="filter-group" data-testid="universe-filters">
              {UNI_FILTERS.map((u) => (
                <button key={u} className={`chip ${uni === u ? "on" : ""}`} onClick={() => setUni(u)}>{u}</button>
              ))}
            </div>
            <div className="catalog-search">
              <Search size={14} />
              <input
                data-testid="catalog-search"
                placeholder="Search properties, signals, providers…"
                value={q}
                onChange={(e) => setQ(e.target.value)}
              />
            </div>
          </div>

          <div className="catalog-grid" data-testid="catalog-grid">
            {filtered.map((s) => {
              const m = TYPE_META[s.signal_type] || TYPE_META.Signal;
              return (
                <div key={s.slug} className="catalog-card" data-testid="catalog-card">
                  <div className="cc-head">
                    <span className="cc-type" style={{ color: m.color }}>
                      <span className="chip-dot" style={{ background: m.color }} />{m.label}
                    </span>
                    {s.universe && <span className="cc-uni">{s.universe}</span>}
                  </div>
                  <div className="cc-name">{s.name}</div>
                  <div className="cc-meta">
                    <span><Database size={11} /> {s.field_type}</span>
                    <span><Clock size={11} /> {s.update_cadence}</span>
                  </div>
                  <div className="cc-desc">{s.description}</div>
                  {s.field_name && <div className="cc-field">{s.field_name}</div>}
                  <div className="cc-providers">
                    <div className="cc-provtitle">{s.provider_count} {s.provider_count === 1 ? "provider" : "providers"}</div>
                    <div className="cc-chips">
                      {s.providers.slice(0, 7).map((p) => (
                        <button
                          key={p.name}
                          className="prov-chip"
                          data-testid="catalog-provider-chip"
                          style={{ borderColor: QCOLOR[p.quality] === "var(--signal)" ? "rgba(232,160,30,0.4)" : "var(--hairline)" }}
                          onClick={() => p.slug && navigate(`/?node=${p.slug}`)}
                          title={`${p.name} · ${p.quality || ""}`}
                        >
                          {p.name}
                        </button>
                      ))}
                      {s.providers.length > 7 && <span className="prov-more">+{s.providers.length - 7}</span>}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
          {!loading && filtered.length === 0 && (
            <div style={{ color: "var(--faint)", fontFamily: "var(--mono)", fontSize: 13, padding: "40px 0" }}>
              No data points match these filters.
            </div>
          )}
          <div style={{ marginTop: 40 }}>
            <button className="view-graph-btn" data-testid="open-graph" onClick={() => navigate("/")}>
              Explore in the Graph <ArrowRight size={14} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
