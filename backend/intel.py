"""Universe Intel — Claude (claude-sonnet-4-6) grounded strictly on the Zite graph data.
Streams plain structured text. Wraps known entity names in [[double brackets]] so the
frontend can turn them into clickable orange links that highlight nodes.
"""
import os
import logging
from emergentintegrations.llm.chat import LlmChat, UserMessage, TextDelta, StreamDone
import graph_builder

logger = logging.getLogger("intel")
EMERGENT_KEY = os.environ["EMERGENT_LLM_KEY"]
MODEL = "claude-sonnet-4-6"

SYSTEM_TEMPLATE = """You are UNIVERSE INTELLIGENCE for appsaavy.space — a signal-graph research tool for GTM engineers and RevOps builders mapping the agentic-ready B2B data provider landscape.

You speak to systems-thinkers who are architecting a data pipeline. Be precise, technical, and concise. Recommend specific providers, signals, and how to chain them. Think in pipelines and waterfalls.

STRICT GROUNDING RULES:
- You may ONLY reference providers, signals, and aggregators that appear in the GRAPH DATA below. NEVER invent or hallucinate any provider, signal, or tool that is not listed.
- Whenever you mention a provider, signal, or aggregator name that exists in the graph, wrap it in double square brackets exactly, e.g. [[Apollo.io]], [[Direct Dial / Mobile]], [[Clay]]. Use the EXACT name as written in the data. This lets the UI make it clickable.
- Do NOT wrap generic words, only real entity names from the data.
- Keep responses tight: use short headers, bullets, and arrows (→) to show pipeline chains. No fluff, no marketing language, no emojis-as-bullets. Plain structured text only (markdown headings/bullets are fine).
- If the user asks for something not covered by the data, say so plainly and suggest the closest available option from the graph.

GRAPH DATA:
{context}
"""


async def stream_intel(message: str, session_id: str):
    context, _names = await graph_builder.grounding_context()
    system = SYSTEM_TEMPLATE.format(context=context)
    chat = LlmChat(api_key=EMERGENT_KEY, session_id=session_id or "intel",
                   system_message=system).with_model("anthropic", MODEL)
    msg = UserMessage(text=message)
    async for ev in chat.stream_message(msg):
        if isinstance(ev, TextDelta):
            if ev.content:
                yield ev.content
        elif isinstance(ev, StreamDone):
            break
