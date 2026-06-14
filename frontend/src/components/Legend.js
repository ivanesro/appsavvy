import React from "react";

const ITEMS = [
  { key: "galaxy", label: "Galaxy: Provider", color: "#E8600A", glow: true },
  { key: "sun", label: "Sun: Entity / Signal", color: "#E8A01E", glow: false },
  { key: "property", label: "Planet: Property", color: "#1EE8D8", glow: false },
];

export default function Legend({ visibleTypes, onToggle }) {
  const vt = visibleTypes || { galaxy: true, sun: true, property: true };
  return (
    <div className="legend" data-testid="legend">
      {ITEMS.map((it) => {
        const on = vt[it.key];
        return (
          <button
            key={it.key}
            className={`legend-row ${on ? "" : "off"}`}
            data-testid={`legend-toggle-${it.key}`}
            onClick={() => onToggle(it.key)}
            title={on ? "Hide" : "Show"}
          >
            <span
              className="legend-dot"
              style={{
                background: on ? it.color : "transparent",
                border: on ? "none" : `1px solid rgba(255,255,255,0.3)`,
                boxShadow: on && it.glow ? `0 0 8px ${it.color}` : "none",
              }}
            />
            {it.label}
          </button>
        );
      })}
    </div>
  );
}
