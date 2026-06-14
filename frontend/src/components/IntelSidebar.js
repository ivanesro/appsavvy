import React, { useState, useRef, useEffect, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, ArrowUp, Sparkles } from "lucide-react";
import { streamIntel } from "../lib/api";
import EntityText from "./EntityText";

const SUGGESTIONS = [
  "Which providers give verified mobile numbers in EMEA?",
  "Build a pipeline to detect job changes then enrich emails",
  "Best intent signals for ABM prioritization?",
];

export default function IntelSidebar({ open, onClose, knownNames, onEntityClick }) {
  const [turns, setTurns] = useState([]); // {q, a, streaming}
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const sessionRef = useRef(null);
  const bodyRef = useRef();

  const known = useMemo(() => new Set(knownNames || []), [knownNames]);

  useEffect(() => {
    if (bodyRef.current) bodyRef.current.scrollTop = bodyRef.current.scrollHeight;
  }, [turns]);

  const ask = (q) => {
    const question = (q ?? input).trim();
    if (!question || busy) return;
    setInput("");
    setBusy(true);
    const idx = turns.length;
    setTurns((prev) => [...prev, { q: question, a: "", streaming: true }]);
    streamIntel(question, sessionRef.current, {
      onSession: (sid) => { sessionRef.current = sid; },
      onDelta: (c) => setTurns((prev) => {
        const copy = [...prev];
        if (copy[idx]) copy[idx] = { ...copy[idx], a: copy[idx].a + c };
        return copy;
      }),
      onError: (msg) => setTurns((prev) => {
        const copy = [...prev];
        if (copy[idx]) copy[idx] = { ...copy[idx], a: copy[idx].a + `\n\n_Error: ${msg}_`, streaming: false };
        return copy;
      }),
      onDone: () => {
        setTurns((prev) => {
          const copy = [...prev];
          if (copy[idx]) copy[idx] = { ...copy[idx], streaming: false };
          return copy;
        });
        setBusy(false);
      },
    });
  };

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          className="intel-panel"
          data-testid="intel-panel"
          initial={{ opacity: 0, y: 30, scale: 0.96 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 30, scale: 0.96 }}
          transition={{ type: "spring", stiffness: 320, damping: 30 }}
        >
          <div className="intel-head">
            <span className="title">Universe Intelligence</span>
            <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
              <span className="model">Claude Sonnet</span>
              <button className="icon-btn" data-testid="intel-close" onClick={onClose}><X size={15} /></button>
            </div>
          </div>
          <div className="intel-body" ref={bodyRef}>
            {turns.length === 0 && (
              <div className="intel-empty">
                <div style={{ display: "flex", gap: 8, alignItems: "center", color: "var(--provider)", marginBottom: 12 }}>
                  <Sparkles size={15} /> <span className="mono" style={{ fontSize: 11, letterSpacing: "0.08em" }}>ASK THE GRAPH</span>
                </div>
                Grounded in {known.size} real nodes. Describe a pipeline or signal you need — answers reference only providers that exist in the graph.
                <div style={{ marginTop: 16, display: "flex", flexDirection: "column", gap: 8 }}>
                  {SUGGESTIONS.map((s) => (
                    <button key={s} className="icon-btn" data-testid="intel-suggestion"
                      style={{ textAlign: "left", padding: "9px 11px", border: "1px solid var(--hairline)", borderRadius: 8, color: "var(--muted)", fontSize: 12.5, fontFamily: "var(--sans)" }}
                      onClick={() => ask(s)}>{s}</button>
                  ))}
                </div>
              </div>
            )}
            {turns.map((t, i) => (
              <div key={i} style={{ marginBottom: 18 }}>
                <div className="mono" style={{ fontSize: 11, color: "var(--faint)", letterSpacing: "0.06em", marginBottom: 6 }}>
                  › {t.q}
                </div>
                <div className={t.streaming && !t.a ? "blink" : ""}>
                  <EntityText text={t.a} knownNames={known} onEntityClick={onEntityClick} />
                  {t.streaming && t.a ? <span className="blink" /> : null}
                </div>
              </div>
            ))}
          </div>
          <div className="intel-foot">
            <input
              className="intel-input"
              data-testid="intel-input"
              placeholder="Describe the signal you need…"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter") ask(); }}
            />
            <button className="intel-send" data-testid="intel-send" disabled={busy || !input.trim()} onClick={() => ask()}>
              <ArrowUp size={16} />
            </button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
