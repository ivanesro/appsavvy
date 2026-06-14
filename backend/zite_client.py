"""Cached, resilient client for the Zite (ZiteDB) REST API.
Keeps the API key server-side. Caches table payloads in-memory with a short TTL.
"""
import os
import time
import asyncio
import logging
import requests

logger = logging.getLogger("zite")

KEY = os.environ["ZITE_API_KEY"]
BASE_ID = os.environ["ZITE_BASE_ID"]
API = os.environ.get("ZITE_API_URL", "https://tables.zite.com/api/v1")
HEAD = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

TABLES = {
    "providers": "tjynJoa3Z9k",
    "signals": "tfbPMxULzzJ",
    "universes": "tx3ax8wwSnj",
    "provider_universes": "tg3gnEwKv56",
    "provider_signals": "tuDAEwuWL85",
    "aggregators": "toKLFjsZ5hK",
    "aggregator_providers": "tnoaYzkwLBH",
    "connectors": "tfgYfRx6uie",
    "crawl_jobs": "thXWE1Be2Qb",
}

TTL = 600.0  # seconds
_cache = {}  # table -> (timestamp, records)
_lock = asyncio.Lock()


def _fetch_table_sync(table_id):
    out, offset = [], 0
    while True:
        last = None
        for attempt in range(4):
            r = requests.post(
                f"{API}/bases/{BASE_ID}/tables/{table_id}/records/list",
                headers=HEAD, json={"limit": 500, "offset": offset}, timeout=30,
            )
            last = r
            if r.status_code == 429:
                time.sleep(1.0 * (attempt + 1)); continue
            break
        last.raise_for_status()
        d = last.json()
        out.extend(d.get("records", []))
        if not d.get("hasMore"):
            break
        offset += 500
    return out


async def get_table(name, force=False):
    """Return list of records (each: {id, fields, data, createdAt, updatedAt})."""
    tid = TABLES[name]
    now = time.time()
    cached = _cache.get(name)
    if cached and not force and (now - cached[0]) < TTL:
        return cached[1]
    async with _lock:
        cached = _cache.get(name)
        if cached and not force and (time.time() - cached[0]) < TTL:
            return cached[1]
        try:
            records = await asyncio.to_thread(_fetch_table_sync, tid)
            _cache[name] = (time.time(), records)
            return records
        except Exception as e:
            logger.error(f"Zite fetch failed for {name}: {e}")
            if cached:
                return cached[1]  # serve stale on error
            raise


async def get_all_tables(force=False):
    names = list(TABLES.keys())
    results = await asyncio.gather(*[get_table(n, force=force) for n in names])
    return dict(zip(names, results))


def invalidate():
    _cache.clear()
