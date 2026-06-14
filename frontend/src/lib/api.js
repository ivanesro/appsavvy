const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

export async function fetchGraph() {
  const r = await fetch(`${API}/graph`);
  if (!r.ok) throw new Error(`graph ${r.status}`);
  return r.json();
}

export async function fetchProvider(slug) {
  const r = await fetch(`${API}/provider/${slug}`);
  if (!r.ok) throw new Error(`provider ${r.status}`);
  return r.json();
}

export async function fetchUniverses() {
  const r = await fetch(`${API}/universes`);
  if (!r.ok) throw new Error(`universes ${r.status}`);
  return r.json();
}

export async function fetchSignals() {
  const r = await fetch(`${API}/signals`);
  if (!r.ok) throw new Error(`signals ${r.status}`);
  return r.json();
}

// Stream the Universe Intel response over SSE-style fetch.
export async function streamIntel(message, sessionId, handlers) {
  const { onSession, onDelta, onDone, onError } = handlers;
  try {
    const res = await fetch(`${API}/intel/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, session_id: sessionId || null }),
    });
    if (!res.ok || !res.body) throw new Error(`intel ${res.status}`);
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const parts = buffer.split("\n\n");
      buffer = parts.pop() || "";
      for (const part of parts) {
        const line = part.trim();
        if (!line.startsWith("data:")) continue;
        const payload = line.slice(5).trim();
        if (!payload) continue;
        let evt;
        try { evt = JSON.parse(payload); } catch { continue; }
        if (evt.type === "session") onSession && onSession(evt.session_id);
        else if (evt.type === "delta") onDelta && onDelta(evt.content);
        else if (evt.type === "error") onError && onError(evt.content);
        else if (evt.type === "done") onDone && onDone();
      }
    }
    onDone && onDone();
  } catch (e) {
    onError && onError(e.message || "stream failed");
  }
}
