import React, { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Copy, Check, ExternalLink, BookOpen } from "lucide-react";
import { fetchProvider } from "../lib/api";

const BADGE_STYLES = {
  "MCP Server": { color: "#E8600A", bg: "rgba(232,96,10,0.1)" },
  "REST API": { color: "#E8A01E", bg: "rgba(232,160,30,0.1)" },
  "Clay Native": { color: "#1EE8D8", bg: "rgba(30,232,216,0.1)" },
  "N8N Native": { color: "#1EE8D8", bg: "rgba(30,232,216,0.1)" },
  "Snowflake": { color: "#A78BFA", bg: "rgba(167,139,250,0.12)" },
  "GraphQL": { color: "#E879B9", bg: "rgba(232,121,185,0.1)" },
  "Webhook": { color: "#8Fb8ff", bg: "rgba(143,184,255,0.1)" },
  "CSV Export": { color: "#9aa3b2", bg: "rgba(154,163,178,0.1)" },
};

function Badge({ type }) {
  const s = BADGE_STYLES[type] || { color: "#9aa3b2", bg: "rgba(154,163,178,0.1)" };
  return (
    <span className="badge" style={{ color: s.color, borderColor: s.color + "55", background: s.bg }}>
      {type}
    </span>
  );
}

export default function GalaxyPanel({ slug, onClose, onHighlightSignal }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    let alive = true;
    setLoading(true);
    fetchProvider(slug)
      .then((d) => { if (alive) { setData(d); setLoading(false); } })
      .catch(() => { if (alive) setLoading(false); });
    return () => { alive = false; };
  }, [slug]);

  const copyMcp = () => {
    if (!data?.mcp_url) return;
    navigator.clipboard.writeText(data.mcp_url);
    setCopied(true);
    setTimeout(() => setCopied(false), 1600);
  };

  const connectorTypes = data ? [...new Set(data.connectors.map((c) => c.connector_type))] : [];

  return (
    <AnimatePresence>
      <motion.div
        className="galaxy-panel"
        data-testid="galaxy-panel"
        initial={{ x: 400, opacity: 0.4 }}
        animate={{ x: 0, opacity: 1 }}
        exit={{ x: 420, opacity: 0 }}
        transition={{ type: "spring", stiffness: 280, damping: 32 }}
      >
        <button className="icon-btn gp-close" data-testid="panel-close" onClick={onClose}>
          <X size={18} />
        </button>
        <div className="gp-scroll">
          {loading && <div style={{ color: "var(--faint)", fontFamily: "var(--mono)", fontSize: 12, marginTop: 40 }}>LOADING GALAXY…</div>}
          {!loading && data && (
            <>
              <div className="gp-label">Galaxy Details</div>
              <h1 className="gp-name" data-testid="panel-provider-name">{data.name}</h1>
              <p className="gp-desc">{data.description}</p>

              <div className="gp-tiles">
                <div className="gp-tile">
                  <div className="k">Coverage</div>
                  <div className="v" style={{ fontSize: 11.5, lineHeight: 1.4 }}>{data.coverage_summary || "—"}</div>
                </div>
                <div className="gp-tile">
                  <div className="k">Pricing Tier</div>
                  <div className="v">{data.pricing_tier || "—"}</div>
                </div>
              </div>

              <div className="gp-section-title">Agentic Connectors</div>
              <div className="badges" data-testid="connector-badges">
                {connectorTypes.length ? connectorTypes.map((t) => <Badge key={t} type={t} />)
                  : <span style={{ color: "var(--faint)", fontSize: 12 }}>No connectors listed</span>}
              </div>

              {data.mcp_url && (
                <>
                  <div className="gp-section-title">MCP Endpoint</div>
                  <div className="mcp-field">
                    <code data-testid="mcp-url">{data.mcp_url}</code>
                    <button className="icon-btn" data-testid="copy-mcp" onClick={copyMcp} title="Copy MCP URL">
                      {copied ? <Check size={14} color="#1EE8D8" /> : <Copy size={14} />}
                    </button>
                  </div>
                </>
              )}

              <div className="gp-section-title">Signals in this Galaxy ({data.signals.length})</div>
              <div className="sig-list" data-testid="signals-list">
                {data.signals.map((s) => (
                  <div
                    key={s.signal_name}
                    className="sig-item"
                    data-testid="signal-item"
                    onClick={() => onHighlightSignal(s.signal_name)}
                  >
                    <span className="nm">{s.signal_name}</span>
                    <span className={`sig-quality q-${(s.coverage_quality || "").toLowerCase()}`}>
                      {s.coverage_quality}
                    </span>
                  </div>
                ))}
              </div>

              {data.aggregators?.length > 0 && (
                <>
                  <div className="gp-section-title">Reachable Via</div>
                  <div className="badges">
                    {data.aggregators.map((a) => (
                      <span key={a.aggregator_name} className="badge" style={{ color: "#9aa3b2", borderColor: "var(--hairline)", background: "rgba(255,255,255,0.03)" }}>
                        {a.aggregator_name}
                      </span>
                    ))}
                  </div>
                </>
              )}

              <div className="gp-links">
                {data.website_url && (
                  <a className="gp-link" href={data.website_url} target="_blank" rel="noreferrer">
                    <ExternalLink size={12} /> Website
                  </a>
                )}
                {data.docs_url && (
                  <a className="gp-link" href={data.docs_url} target="_blank" rel="noreferrer">
                    <BookOpen size={12} /> API Docs
                  </a>
                )}
                <a className="gp-link" href={`/node/${data.slug}`}>
                  <ExternalLink size={12} /> Full Page
                </a>
              </div>
            </>
          )}
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
