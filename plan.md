# appsaavy.space — Interactive Signal Graph (Plan)

## 1) Objectives
- Deliver a **graph-first research tool** (no marketing UI) that lets GTM engineers explore **real providers + real signals + real integrations** from **Zite DB**.
- Provide a stable core data flow: **Zite → FastAPI graph builder (cached) → React force-graph**.
- Populate Zite with a **focused, high-quality v1 dataset** (≈28–32 providers, ≈45–60 signals, connectors + junctions) with **no fake entries**.
- Ship Universe Intel: **SSE streaming Claude** grounded strictly on the Zite dataset, with clickable entity references that highlight nodes.

---

## 2) Implementation Steps

### Phase 1 — Core POC (Isolation) ✅ (already proven)

### ENHANCEMENTS ROUND 1 (user-requested) ✅ ALL DONE & TESTED 100%
1. Legend toggles — bottom-left legend rows toggle node categories (galaxy/sun/property) on the canvas.
2. Space-universe styling — in-canvas parallax starfield (320 stars) + luminous brighter node cores.
3. Properties Catalog view — new /catalog route: browsable grid of all 52 data points with type/universe/search filters + clickable provider chips that jump into the graph.
4. More spacing — stronger physics (charge -620, distanceMax 1100, collide +22, link distance 98).
5. Data crawl — added 24 NEW real Crustdata-based properties/signals (now 52 signals, 212 graph links).
- ✅ Zite DB connectivity + schema verified (tables.zite.com).
- ✅ Create/read/delete records; junction link resolution proven.
- ✅ Claude grounding proven (claude-sonnet-4-6 via EMERGENT_LLM_KEY).
- ✅ Connectors table created (`connectors`, id `tfgYfRx6uie`).

**User stories (POC validation)**
1. As a user, I want the app to load real providers from Zite so the graph is never empty.
2. As a user, I want provider↔signal edges to reflect true backend relationships.
3. As a user, I want AI answers to reference only real nodes that exist in the graph.
4. As a user, I want connector badges to come from real backend rows, not UI constants.
5. As a builder, I want a repeatable script to validate Zite write + link behavior.

---

### Phase 2 — V1 App Development (build around proven core)

#### 2.1 Data population (real research → Zite)
- Implement **idempotent seed script** `/app/backend/seed_zite.py`:
  - slug-based upsert for: `providers`, `signals`, `provider_signals`, `aggregator_providers`, `provider_universes`, `connectors`.
  - only create/update when changed; log counts + diffs.
- Web research pass (best practices + accuracy checks):
  - verify each provider’s **docs_url**, core coverage, pricing tier, API availability.
  - map each signal to the correct **universe + type + field_type + cadence**.
- Target v1 data:
  - Providers: expand from 10 → **~28–32** (focused, high-signal set).
  - Signals: **~45–60**.
  - provider_signals edges: **2–8 signals/provider**.
  - connectors: **REST/MCP/Clay/N8N/Snowflake/etc.** with real URLs.
  - aggregator_providers: add Clay/N8N/Relay/Make/Zapier/Bardeen integration coverage.

#### 2.2 FastAPI backend (graph builder + detail + AI)
- Create Zite client module with:
  - `list_records(tableId, limit/offset/filter)`
  - retry/backoff for 429/5xx
  - in-memory cache (TTL ~60s) for table payloads + derived graph.
- Implement routes:
  - `GET /api/graph` → `{ nodes, links }` built from Zite tables.
  - `GET /api/providers` + `GET /api/provider/{slug}` (details: connectors, signals, aggregators).
  - `GET /api/signals`, `GET /api/universes`, `GET /api/aggregators`.
  - `GET /api/crawl-jobs` (read-only).
  - `POST /api/intel/chat` (SSE streaming): Claude Sonnet grounded on **current graph snapshot**; persist chat turns in Mongo.
- Node/edge building rules:
  - Providers = galaxies, signals/entities = planets, properties = stars (by `signal_type`).
  - Links from junction tables primarily via **linked IDs**; fallback to **denormalized name matching**.
  - Include `kind` on links (`provider_signal`, `aggregator_provider`, `provider_universe`).

#### 2.3 React frontend (CRA) — 5 screens, locked identity
- Install + wire: `react-force-graph-2d`, Tailwind, fonts (Inter + Geist Mono).
- Screen 1: The Graph (home)
  - full-viewport canvas bg `#08090E`, no scroll.
  - top bar (logo, universe tabs, search + CMD+K).
  - hover highlight + fade others; select pulses; edges thin rgba white.
- Screen 2: Universe filter
  - tab click filters in-place (fade to 5% + recenter cluster) with no reload.
- Screen 3: Galaxy Details panel
  - right slide-in, ~360px, mono headers; pricing/coverage; connectors badge chips; signals list → click highlights node.
- Screen 4: Universe Intel sidebar
  - bottom-right expandable; SSE streaming; plain structured text; entity mentions become clickable links.
- Screen 5: Node detail page `/node/:slug`
  - provider detail + `react-helmet` meta; “View in Graph” deep-link with preselect.

**User stories (V1)**
1. As a user, I want to land on the site and see a living graph instantly with real nodes.
2. As a user, I want universe tabs to isolate the relevant cluster without losing context.
3. As a user, I want clicking a provider to reveal connectors + signals so I can design my pipeline.
4. As a user, I want AI to recommend providers/signals and let me click results to highlight them.
5. As a user, I want `/node/{slug}` to summarize a provider and let me jump into the graph view.

#### 2.4 Phase-2 checkpoint: end-to-end test pass
- Run one E2E test round (backend routes + graph render + panel + AI streaming + node page).
- Fix any broken flows before moving on.

---

### Phase 3 — Testing, polish, and resilience
- Backend hardening:
  - stricter schema validation, safer datetime serialization, better cache invalidation.
  - guardrails for empty tables (graceful empty states) + partial data.
- Frontend polish:
  - performance (canvas tuning), stable node positioning, smooth fade transitions.
  - command palette quality (fast fuzzy search, keyboard navigation).
- Add minimal analytics-style logging (server-side) for: graph build time, Zite latency, Claude latency.

**User stories (polish)**
1. As a user, I want the graph interactions to stay smooth even as data grows.
2. As a user, I want loading/error states to be quiet and non-SaaS-like but informative.
3. As a user, I want search (CMD+K) to find nodes instantly by name/alias.
4. As a user, I want AI responses to be consistent and never hallucinate providers.
5. As a maintainer, I want seed + graph build to be repeatable and debuggable via logs.

---

## 3) Next Actions (immediate)
1. Build `/app/backend/seed_zite.py` (slug upsert) and run once to populate: signals + junctions + connectors.
2. Implement FastAPI endpoints: `/api/graph`, `/api/provider/{slug}`, `/api/intel/chat` (SSE).
3. Implement React Graph screen + selection/hover + details panel.
4. Add Universe Intel UI with streaming + clickable entity linking.
5. Run testing agent for an end-to-end validation pass and fix regressions.

---

## 4) Success Criteria
- Data: Zite contains **~28–32 providers**, **~45–60 signals**, and populated junction tables (provider_signals, aggregator_providers, provider_universes, connectors).
- Graph: `GET /api/graph` returns a valid node/link set; React renders it with locked identity; hover/select/filter all work.
- Details: Provider panel shows pricing/coverage/connectors/signals sourced from Zite.
- AI: `/api/intel/chat` streams responses and references only real providers/signals; clicking references highlights nodes.
- Stability: one full E2E test pass without broken core flows (load → explore → details → AI → node page).