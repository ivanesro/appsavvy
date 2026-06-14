import React from "react";
import { Search, Network, LayoutGrid } from "lucide-react";
import { useNavigate } from "react-router-dom";

const TABS = [
  { label: "Intent Universe", match: "Intent" },
  { label: "Enrichment", match: "Enrichment" },
  { label: "Technographic", match: "Technographic" },
  { label: "MCP Hub", match: "MCP Hub" },
];

export default function TopBar({ activeUniverse, onTab, onOpenSearch, view }) {
  const navigate = useNavigate();
  const isGraph = view !== "catalog";
  return (
    <div className="topbar">
      <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
        <a href="/" className="logo" data-testid="logo">
          appsaavy<span className="dot">.</span>space
        </a>
        <div className="nav-seg" data-testid="view-nav">
          <button className={`nav-pill ${isGraph ? "active" : ""}`} data-testid="nav-graph" onClick={() => navigate("/")}>
            <Network size={12} /> Graph
          </button>
          <button className={`nav-pill ${!isGraph ? "active" : ""}`} data-testid="nav-catalog" onClick={() => navigate("/catalog")}>
            <LayoutGrid size={12} /> Catalog
          </button>
        </div>
      </div>

      {isGraph ? (
        <div className="uni-tabs" data-testid="universe-tabs">
          {TABS.map((t) => (
            <button
              key={t.match}
              className={`uni-tab ${activeUniverse === t.match ? "active" : ""}`}
              data-testid={`tab-${t.match.toLowerCase().replace(/\s+/g, "-")}`}
              onClick={() => onTab(activeUniverse === t.match ? null : t.match)}
            >
              {t.label}
            </button>
          ))}
        </div>
      ) : <div />}

      {isGraph ? (
        <div className="search-box" data-testid="search-trigger" onClick={onOpenSearch}>
          <Search size={14} />
          <span>Search the graph</span>
          <span className="kbd">⌘K</span>
        </div>
      ) : <div style={{ width: 190 }} />}
    </div>
  );
}
