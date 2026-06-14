import { useEffect, useState, useCallback, useMemo } from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route, useSearchParams } from "react-router-dom";
import { fetchGraph } from "@/lib/api";
import GraphCanvas from "@/components/GraphCanvas";
import TopBar from "@/components/TopBar";
import Legend from "@/components/Legend";
import GalaxyPanel from "@/components/GalaxyPanel";
import IntelSidebar from "@/components/IntelSidebar";
import CommandPalette from "@/components/CommandPalette";
import NodePage from "@/pages/NodePage";

function GraphHome() {
  const [graph, setGraph] = useState({ nodes: [], links: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeUniverse, setActiveUniverse] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedProvider, setSelectedProvider] = useState(null); // node
  const [focusSignal, setFocusSignal] = useState(null);
  const [intelOpen, setIntelOpen] = useState(false);
  const [paletteOpen, setPaletteOpen] = useState(false);
  const [params, setParams] = useSearchParams();

  useEffect(() => {
    fetchGraph()
      .then((d) => { setGraph(d); setLoading(false); })
      .catch((e) => { setError(e.message); setLoading(false); });
  }, []);

  // deep link: /?node=slug pre-selects a provider
  useEffect(() => {
    const node = params.get("node");
    if (node && graph.nodes.length) {
      const n = graph.nodes.find((x) => x.slug === node && x.type === "provider");
      if (n) { setSelectedProvider(n); setFocusSignal(n.id); }
    }
  }, [graph, params]); // eslint-disable-line

  // CMD+K
  useEffect(() => {
    const onKey = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setPaletteOpen((p) => !p);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  const nameToNode = useMemo(() => {
    const m = {};
    graph.nodes.forEach((n) => { m[n.label] = n; });
    return m;
  }, [graph]);

  const knownNames = useMemo(() => graph.nodes.map((n) => n.label), [graph]);

  const handleSelectProvider = useCallback((node) => {
    setSelectedProvider(node);
    setFocusSignal(node.id);
  }, []);

  const handleEntityClick = useCallback((name) => {
    const node = nameToNode[name];
    if (!node) return;
    if (node.type === "provider") handleSelectProvider(node);
    else setFocusSignal(node.id);
  }, [nameToNode, handleSelectProvider]);

  const handlePalettePick = useCallback((node) => {
    setPaletteOpen(false);
    if (node.type === "provider") handleSelectProvider(node);
    else setFocusSignal(node.id);
  }, [handleSelectProvider]);

  const closePanel = useCallback(() => {
    setSelectedProvider(null);
    if (params.get("node")) { params.delete("node"); setParams(params, { replace: true }); }
  }, [params, setParams]);

  return (
    <div className="graph-shell app-fade-in">
      <div className={`graph-canvas-wrap ${selectedProvider ? "dimmed" : ""}`}>
        {!loading && !error && (
          <GraphCanvas
            data={graph}
            activeUniverse={activeUniverse}
            searchQuery={searchQuery}
            selectedId={selectedProvider?.id}
            focusSignal={focusSignal}
            onSelectProvider={handleSelectProvider}
            onClearFocus={() => { setFocusSignal(null); }}
          />
        )}
      </div>

      {loading && (
        <div style={{ position: "absolute", inset: 0, display: "grid", placeItems: "center", color: "var(--faint)", fontFamily: "var(--mono)", letterSpacing: "0.2em", fontSize: 12 }}>
          MAPPING THE SIGNAL UNIVERSE…
        </div>
      )}
      {error && (
        <div style={{ position: "absolute", inset: 0, display: "grid", placeItems: "center", color: "#E8600A", fontFamily: "var(--mono)", fontSize: 13 }}>
          Failed to load graph: {error}
        </div>
      )}

      <TopBar
        activeUniverse={activeUniverse}
        onTab={(t) => { setActiveUniverse(t); setSearchQuery(""); }}
        onOpenSearch={() => setPaletteOpen(true)}
      />
      <Legend />

      {!intelOpen && (
        <div className="intel-pill" data-testid="intel-pill" onClick={() => setIntelOpen(true)}>
          <span className="pulse-dot" /> Universe Intel
        </div>
      )}
      <IntelSidebar
        open={intelOpen}
        onClose={() => setIntelOpen(false)}
        knownNames={knownNames}
        onEntityClick={handleEntityClick}
      />

      {selectedProvider && (
        <GalaxyPanel
          slug={selectedProvider.slug}
          onClose={closePanel}
          onHighlightSignal={(name) => setFocusSignal(nameToNode[name]?.id || name)}
        />
      )}

      <CommandPalette
        open={paletteOpen}
        onClose={() => setPaletteOpen(false)}
        nodes={graph.nodes}
        onPick={handlePalettePick}
      />
    </div>
  );
}

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<GraphHome />} />
          <Route path="/node/:slug" element={<NodePage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
