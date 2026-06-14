import React from "react";
import { Search } from "lucide-react";

const TABS = [
  { label: "Intent Universe", match: "Intent" },
  { label: "Enrichment", match: "Enrichment" },
  { label: "Technographic", match: "Technographic" },
  { label: "MCP Hub", match: "MCP Hub" },
];

export default function TopBar({ activeUniverse, onTab, onOpenSearch }) {
  return (
    <div className="topbar">
      <a href="/" className="logo" data-testid="logo">
        appsaavy<span className="dot">.</span>space
      </a>
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
      <div className="search-box" data-testid="search-trigger" onClick={onOpenSearch}>
        <Search size={14} />
        <span>Search the graph</span>
        <span className="kbd">⌘K</span>
      </div>
    </div>
  );
}
