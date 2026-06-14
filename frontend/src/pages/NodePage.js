import React, { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { ArrowLeft, ExternalLink, BookOpen, Copy, Check } from "lucide-react";
import { fetchProvider } from "../lib/api";

const BADGE = {
  "MCP Server": "#E8600A", "REST API": "#E8A01E", "Clay Native": "#1EE8D8",
  "N8N Native": "#1EE8D8", "Snowflake": "#A78BFA", "GraphQL": "#E879B9",
  "Webhook": "#8Fb8ff", "CSV Export": "#9aa3b2",
};

export default function NodePage() {
  const { slug } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetchProvider(slug).then((d) => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, [slug]);

  const types = data ? [...new Set(data.connectors.map((c) => c.connector_type))] : [];

  return (
    <div className="node-page">
      {/* React 19 renders these into <head> for SEO */}
      {data && <title>{`${data.name} — Signals, Connectors & Pricing | appsaavy.space`}</title>}
      {data && <meta name="description" content={(data.description || "").slice(0, 155)} />}
      <div className="node-wrap">
        <Link to="/" className="node-back" data-testid="node-back"><ArrowLeft size={12} style={{ verticalAlign: "middle" }} /> BACK TO GRAPH</Link>
        {loading && <p style={{ color: "var(--faint)", fontFamily: "var(--mono)", marginTop: 40 }}>LOADING…</p>}
        {!loading && !data && <p style={{ color: "var(--faint)", marginTop: 40 }}>Provider not found.</p>}
        {!loading && data && (
          <>
            <div className="gp-label" style={{ marginTop: 30 }}>Provider Galaxy</div>
            <h1 className="node-title" data-testid="node-title">{data.name}</h1>
            <div className="node-universes">
              {(data.universes || []).map((u) => <span className="uni-chip" key={u}>{u}</span>)}
            </div>
            <p className="gp-desc" style={{ maxWidth: 680, fontSize: 15 }}>{data.description}</p>

            <div className="gp-tiles" style={{ maxWidth: 420 }}>
              <div className="gp-tile"><div className="k">Coverage</div><div className="v" style={{ fontSize: 12 }}>{data.coverage_summary || "—"}</div></div>
              <div className="gp-tile"><div className="k">Pricing Tier</div><div className="v">{data.pricing_tier || "—"}</div></div>
            </div>

            <div className="gp-section-title">Agentic Connectors</div>
            <div className="badges">
              {types.map((t) => (
                <span key={t} className="badge" style={{ color: BADGE[t] || "#9aa3b2", borderColor: (BADGE[t] || "#9aa3b2") + "55", background: (BADGE[t] || "#9aa3b2") + "18" }}>{t}</span>
              ))}
            </div>

            {data.mcp_url && (
              <>
                <div className="gp-section-title">MCP Endpoint</div>
                <div className="mcp-field" style={{ maxWidth: 420 }}>
                  <code>{data.mcp_url}</code>
                  <button className="icon-btn" onClick={() => { navigator.clipboard.writeText(data.mcp_url); setCopied(true); setTimeout(() => setCopied(false), 1500); }}>
                    {copied ? <Check size={14} color="#1EE8D8" /> : <Copy size={14} />}
                  </button>
                </div>
              </>
            )}

            <div className="gp-section-title">Signals in this Galaxy ({data.signals.length})</div>
            <div className="sig-list" style={{ maxWidth: 480 }}>
              {data.signals.map((s) => (
                <div className="sig-item" key={s.signal_name} style={{ cursor: "default" }}>
                  <span className="nm">{s.signal_name}</span>
                  <span className={`sig-quality q-${(s.coverage_quality || "").toLowerCase()}`}>{s.coverage_quality}</span>
                </div>
              ))}
            </div>

            <div style={{ display: "flex", gap: 14, marginTop: 22 }}>
              {data.website_url && <a className="gp-link" href={data.website_url} target="_blank" rel="noreferrer"><ExternalLink size={12} /> Website</a>}
              {data.docs_url && <a className="gp-link" href={data.docs_url} target="_blank" rel="noreferrer"><BookOpen size={12} /> API Docs</a>}
            </div>

            <button className="view-graph-btn" data-testid="view-in-graph" onClick={() => navigate(`/?node=${data.slug}`)}>
              View in Graph →
            </button>
          </>
        )}
      </div>
    </div>
  );
}
