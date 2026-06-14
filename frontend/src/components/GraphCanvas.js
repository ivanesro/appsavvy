import React, { useRef, useCallback, useEffect, useMemo, useState } from "react";
import ForceGraph2D from "react-force-graph-2d";
import { forceCollide, forceManyBody } from "d3-force";

function hexA(hex, a) {
  const h = hex.replace("#", "");
  const r = parseInt(h.substring(0, 2), 16);
  const g = parseInt(h.substring(2, 4), 16);
  const b = parseInt(h.substring(4, 6), 16);
  return `rgba(${r},${g},${b},${a})`;
}

export default function GraphCanvas({
  data, activeUniverse, searchQuery, selectedId, focusSignal, visibleTypes,
  onSelectProvider, onClearFocus,
}) {
  const fgRef = useRef();
  const wrapRef = useRef();
  const [dims, setDims] = useState({ w: window.innerWidth, h: window.innerHeight });
  const [hoverId, setHoverId] = useState(null);

  const vt = useMemo(() => visibleTypes || { galaxy: true, sun: true, property: true }, [visibleTypes]);
  const nodeCat = useCallback((n) => {
    if (n.type === "provider" || n.type === "aggregator") return "galaxy";
    if (n.signal_type === "Property") return "property";
    return "sun";
  }, []);

  // background starfield (graph-space, pans + zooms with the universe)
  const stars = useMemo(() => {
    const arr = [];
    const tints = ["255,255,255", "200,220,255", "232,160,30", "30,232,216"];
    for (let i = 0; i < 320; i++) {
      arr.push({
        x: (Math.random() - 0.5) * 6000,
        y: (Math.random() - 0.5) * 6000,
        r: Math.random() * 1.5 + 0.5,
        a: Math.random() * 0.55 + 0.18,
        tint: tints[Math.floor(Math.random() * (Math.random() < 0.8 ? 2 : tints.length))],
      });
    }
    return arr;
  }, []);

  const drawStars = useCallback((ctx, globalScale) => {
    const gs = globalScale || 1;
    for (const s of stars) {
      const rr = s.r / gs;
      ctx.beginPath();
      ctx.fillStyle = `rgba(${s.tint},${s.a})`;
      ctx.arc(s.x, s.y, rr, 0, 2 * Math.PI);
      ctx.fill();
    }
  }, [stars]);

  // repaint when category visibility toggles
  useEffect(() => {
    try { fgRef.current && fgRef.current.refresh && fgRef.current.refresh(); } catch (e) {}
  }, [vt]);

  // adjacency for highlight
  const neighbors = useMemo(() => {
    const map = {};
    (data.nodes || []).forEach((n) => (map[n.id] = new Set()));
    (data.links || []).forEach((l) => {
      const s = typeof l.source === "object" ? l.source.id : l.source;
      const t = typeof l.target === "object" ? l.target.id : l.target;
      if (map[s]) map[s].add(t);
      if (map[t]) map[t].add(s);
    });
    return map;
  }, [data]);

  useEffect(() => {
    const onResize = () => setDims({ w: window.innerWidth, h: window.innerHeight });
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  // initial layout framing
  useEffect(() => {
    if (!fgRef.current || !data.nodes?.length) return;
    const t = setTimeout(() => {
      try {
        fgRef.current.d3Force("charge", forceManyBody().strength(-620).distanceMax(1100));
        fgRef.current.d3Force("collide", forceCollide((n) => n.size / 2 + 22).strength(0.95));
        const lf = fgRef.current.d3Force("link");
        if (lf) lf.distance(98).strength(0.12);
        fgRef.current.d3ReheatSimulation();
      } catch (e) {}
    }, 60);
    // backup fit in case engine settles silently
    const f = setTimeout(() => fitView(), 3800);
    return () => { clearTimeout(t); clearTimeout(f); };
  }, [data]); // eslint-disable-line

  const fitView = useCallback(() => {
    try {
      if (activeUniverse) {
        fgRef.current.zoomToFit(700, 120, (n) => (n.universes || []).includes(activeUniverse));
      } else {
        fgRef.current.zoomToFit(800, 70);
      }
    } catch (e) {}
  }, [activeUniverse]);

  // recenter on active universe cluster
  useEffect(() => {
    if (!fgRef.current || !data.nodes?.length) return;
    const t = setTimeout(() => {
      try {
        if (activeUniverse) {
          fgRef.current.zoomToFit(700, 110, (n) =>
            (n.universes || []).includes(activeUniverse));
        } else {
          fgRef.current.zoomToFit(700, 90);
        }
      } catch (e) {}
    }, 60);
    return () => clearTimeout(t);
  }, [activeUniverse]); // eslint-disable-line

  // focus a specific node (from panel/AI/search)
  useEffect(() => {
    if (!fgRef.current || !focusSignal) return;
    const node = (data.nodes || []).find(
      (n) => n.id === focusSignal || n.label === focusSignal || n.slug === focusSignal
    );
    if (node && node.x != null) {
      fgRef.current.centerAt(node.x, node.y, 600);
      fgRef.current.zoom(2.4, 600);
    }
  }, [focusSignal]); // eslint-disable-line

  const matchSearch = useCallback((n) => {
    if (!searchQuery) return true;
    return (n.label || "").toLowerCase().includes(searchQuery.toLowerCase());
  }, [searchQuery]);

  const nodeAlpha = useCallback((n) => {
    // hover takes priority
    if (hoverId) {
      if (n.id === hoverId) return 1;
      return neighbors[hoverId]?.has(n.id) ? 1 : 0.15;
    }
    if (focusSignal) {
      if (n.id === focusSignal || n.label === focusSignal) return 1;
    }
    if (searchQuery) return matchSearch(n) ? 1 : 0.08;
    if (activeUniverse) {
      return (n.universes || []).includes(activeUniverse) ? 1 : 0.05;
    }
    return 1;
  }, [hoverId, neighbors, activeUniverse, searchQuery, matchSearch, focusSignal]);

  const drawNode = useCallback((node, ctx, globalScale) => {
    const x = node.x, y = node.y;
    if (!Number.isFinite(x) || !Number.isFinite(y)) return;
    if (!vt[nodeCat(node)]) return;
    const r = Math.max(2.2, node.size / 2 / 1);
    const a = nodeAlpha(node);
    const isHi = a >= 0.99;

    // glow for providers + aggregators
    if (node.type === "provider" || node.type === "aggregator") {
      const gr = ctx.createRadialGradient(x, y, 0, x, y, r * 2.6);
      gr.addColorStop(0, hexA(node.color, 0.42 * a));
      gr.addColorStop(0.5, hexA(node.color, 0.16 * a));
      gr.addColorStop(1, hexA(node.color, 0));
      ctx.fillStyle = gr;
      ctx.beginPath();
      ctx.arc(x, y, r * 2.6, 0, 2 * Math.PI);
      ctx.fill();
    } else {
      // soft halo for signal/property nodes too (brighter dots)
      const gr = ctx.createRadialGradient(x, y, 0, x, y, r * 1.9);
      gr.addColorStop(0, hexA(node.color, 0.3 * a));
      gr.addColorStop(1, hexA(node.color, 0));
      ctx.fillStyle = gr;
      ctx.beginPath();
      ctx.arc(x, y, r * 1.9, 0, 2 * Math.PI);
      ctx.fill();
    }

    // core
    ctx.beginPath();
    ctx.arc(x, y, r, 0, 2 * Math.PI);
    ctx.fillStyle = hexA(node.color, Math.max(0.18, a));
    ctx.fill();

    // bright inner highlight (gives nodes a luminous, star-like core)
    if (a > 0.3) {
      ctx.beginPath();
      ctx.arc(x - r * 0.22, y - r * 0.22, r * 0.42, 0, 2 * Math.PI);
      ctx.fillStyle = hexA("#FFFFFF", 0.5 * a);
      ctx.fill();
    }

    // aggregator ring
    if (node.type === "aggregator") {
      ctx.lineWidth = 1.2 / globalScale;
      ctx.strokeStyle = hexA("#FFFFFF", 0.5 * a);
      ctx.beginPath();
      ctx.arc(x, y, r + 3 / globalScale, 0, 2 * Math.PI);
      ctx.stroke();
    }
    // selected pulse ring
    if (node.id === selectedId) {
      ctx.lineWidth = 1.6 / globalScale;
      ctx.strokeStyle = hexA(node.color, 0.9);
      ctx.beginPath();
      ctx.arc(x, y, r + 5 / globalScale, 0, 2 * Math.PI);
      ctx.stroke();
    }

    // label
    const showLabel =
      node.type === "provider" || node.type === "aggregator" || isHi || globalScale > 1.5;
    if (showLabel) {
      const fs = 11 / globalScale;
      ctx.font = `500 ${fs}px "Geist Mono", monospace`;
      ctx.textAlign = "center";
      ctx.textBaseline = "top";
      ctx.fillStyle = hexA("#F4F5F7", node.type === "provider" ? 0.92 * a : 0.78 * a);
      const label = (node.label || "").toUpperCase();
      ctx.fillText(label, x, y + r + 2.5 / globalScale);
    }
  }, [nodeAlpha, selectedId, vt, nodeCat]);

  const paintPointerArea = useCallback((node, color, ctx) => {
    if (!Number.isFinite(node.x) || !Number.isFinite(node.y)) return;
    if (!vt[nodeCat(node)]) return;
    const r = Math.max(4, node.size / 2 + 3);
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(node.x, node.y, r, 0, 2 * Math.PI);
    ctx.fill();
  }, [vt, nodeCat]);

  const linkColor = useCallback((link) => {
    const s = typeof link.source === "object" ? link.source.id : link.source;
    const t = typeof link.target === "object" ? link.target.id : link.target;
    if (hoverId && (s === hoverId || t === hoverId)) return "rgba(232,96,10,0.45)";
    if (selectedId && (s === selectedId || t === selectedId)) return "rgba(232,96,10,0.4)";
    if (hoverId || searchQuery || activeUniverse) return "rgba(255,255,255,0.025)";
    return "rgba(255,255,255,0.08)";
  }, [hoverId, selectedId, searchQuery, activeUniverse]);

  const handleClick = useCallback((node) => {
    if (!node) return;
    if (node.type === "provider") onSelectProvider(node);
    else {
      // center on the signal/aggregator
      if (fgRef.current) {
        fgRef.current.centerAt(node.x, node.y, 500);
        fgRef.current.zoom(2.2, 500);
      }
    }
  }, [onSelectProvider]);

  return (
    <div ref={wrapRef} style={{ width: "100%", height: "100%" }}>
      <ForceGraph2D
        ref={fgRef}
        graphData={data}
        width={dims.w}
        height={dims.h}
        backgroundColor="rgba(0,0,0,0)"
        nodeRelSize={4}
        cooldownTicks={120}
        d3VelocityDecay={0.32}
        warmupTicks={20}
        nodeCanvasObject={drawNode}
        nodePointerAreaPaint={paintPointerArea}
        onRenderFramePre={(ctx, globalScale) => drawStars(ctx, globalScale)}
        linkVisibility={(l) => {
          const s = typeof l.source === "object" ? l.source : null;
          const t = typeof l.target === "object" ? l.target : null;
          if (s && !vt[nodeCat(s)]) return false;
          if (t && !vt[nodeCat(t)]) return false;
          return true;
        }}
        linkColor={linkColor}
        linkWidth={(l) => {
          const s = typeof l.source === "object" ? l.source.id : l.source;
          const t = typeof l.target === "object" ? l.target.id : l.target;
          return (hoverId && (s === hoverId || t === hoverId)) ? 1.2 : 0.5;
        }}
        onNodeHover={(n) => setHoverId(n ? n.id : null)}
        onNodeClick={handleClick}
        onEngineStop={fitView}
        onBackgroundClick={() => { onClearFocus && onClearFocus(); }}
        enableNodeDrag={true}
      />
    </div>
  );
}
