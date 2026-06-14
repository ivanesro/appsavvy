import React from "react";

// Renders Intel text: supports ## / ### headings, - bullets, --- rules,
// and [[Entity Name]] tokens -> clickable orange links if the name is a known node.
export default function EntityText({ text, knownNames, onEntityClick }) {
  const lines = (text || "").split("\n");
  const known = knownNames || new Set();

  const renderInline = (str, keyPrefix) => {
    const parts = str.split(/(\[\[[^\]]+\]\])/g);
    return parts.map((p, i) => {
      const m = p.match(/^\[\[([^\]]+)\]\]$/);
      if (m) {
        const name = m[1];
        if (known.has(name)) {
          return (
            <span
              key={`${keyPrefix}-${i}`}
              className="ent"
              data-testid="intel-entity"
              onClick={() => onEntityClick(name)}
            >
              {name}
            </span>
          );
        }
        return <span key={`${keyPrefix}-${i}`}>{name}</span>;
      }
      // simple bold **x**
      const boldParts = p.split(/(\*\*[^*]+\*\*)/g);
      return boldParts.map((bp, j) => {
        const bm = bp.match(/^\*\*([^*]+)\*\*$/);
        if (bm) return <strong key={`${keyPrefix}-${i}-${j}`}>{bm[1]}</strong>;
        return <span key={`${keyPrefix}-${i}-${j}`}>{bp}</span>;
      });
    });
  };

  return (
    <div className="itx">
      {lines.map((ln, idx) => {
        const t = ln.trim();
        if (!t) return <div key={idx} style={{ height: 4 }} />;
        if (t === "---") return <hr key={idx} />;
        if (t.startsWith("### ")) return <h3 key={idx}>{renderInline(t.slice(4), idx)}</h3>;
        if (t.startsWith("## ")) return <h2 key={idx}>{renderInline(t.slice(3), idx)}</h2>;
        if (t.startsWith("# ")) return <h2 key={idx}>{renderInline(t.slice(2), idx)}</h2>;
        if (/^[-*]\s/.test(t)) return <div className="li" key={idx}>{renderInline(t.replace(/^[-*]\s/, ""), idx)}</div>;
        if (/^\d+\.\s/.test(t)) return <div className="li" key={idx}>{renderInline(t.replace(/^\d+\.\s/, ""), idx)}</div>;
        return <p key={idx}>{renderInline(t, idx)}</p>;
      })}
    </div>
  );
}
