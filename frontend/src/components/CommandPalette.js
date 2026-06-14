import React, { useEffect } from "react";
import { Command } from "cmdk";

const COLOR = { provider: "#E8600A", signal: "#E8A01E", aggregator: "#E8600A" };

export default function CommandPalette({ open, onClose, nodes, onPick }) {
  useEffect(() => {
    const onKey = (e) => { if (e.key === "Escape") onClose(); };
    if (open) window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  if (!open) return null;

  const ordered = [...(nodes || [])].sort((a, b) => {
    const order = { provider: 0, aggregator: 1, signal: 2 };
    return (order[a.type] - order[b.type]) || a.label.localeCompare(b.label);
  });

  return (
    <div className="cmdk-overlay" data-testid="command-palette" onClick={onClose}>
      <div className="cmdk-box" onClick={(e) => e.stopPropagation()}>
        <Command label="Search the graph">
          <Command.Input autoFocus placeholder="Search providers, signals, aggregators…" data-testid="command-input" />
          <Command.List>
            <Command.Empty>No matching nodes in the graph.</Command.Empty>
            {ordered.map((n) => (
              <Command.Item
                key={n.id}
                value={`${n.label} ${n.type} ${(n.universes || []).join(" ")}`}
                onSelect={() => onPick(n)}
                data-testid="command-item"
              >
                <span className="cmdk-dot" style={{ background: COLOR[n.type] || "#888", boxShadow: n.type !== "signal" ? `0 0 6px ${COLOR[n.type]}` : "none" }} />
                <span className="mono" style={{ fontSize: 13 }}>{n.label}</span>
                <span className="cmdk-type">{n.type === "signal" ? (n.signal_type || "signal") : n.type}</span>
              </Command.Item>
            ))}
          </Command.List>
        </Command>
      </div>
    </div>
  );
}
