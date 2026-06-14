from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import json
import logging
import uuid
from pathlib import Path
from datetime import datetime, timezone
from pydantic import BaseModel

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

import zite_client
import graph_builder
import intel

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI(title="appsaavy.space API")
api_router = APIRouter(prefix="/api")

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class IntelRequest(BaseModel):
    message: str
    session_id: str | None = None


@api_router.get("/")
async def root():
    return {"service": "appsaavy.space", "status": "ok"}


@api_router.get("/graph")
async def get_graph():
    try:
        return await graph_builder.build_graph()
    except Exception as e:
        logger.exception("graph build failed")
        raise HTTPException(status_code=502, detail=f"Zite graph build failed: {e}")


@api_router.get("/universes")
async def get_universes():
    return await graph_builder.list_universes()


@api_router.get("/providers")
async def get_providers():
    return await graph_builder.list_providers()


@api_router.get("/provider/{slug}")
async def get_provider(slug: str):
    detail = await graph_builder.provider_detail(slug)
    if not detail:
        raise HTTPException(status_code=404, detail="Provider not found")
    return detail


@api_router.get("/signals")
async def get_signals():
    return await graph_builder.list_signals()


@api_router.get("/crawl-jobs")
async def get_crawl_jobs():
    return await graph_builder.list_crawl_jobs()


@api_router.post("/refresh")
async def refresh_cache():
    zite_client.invalidate()
    await zite_client.get_all_tables(force=True)
    return {"status": "refreshed"}


@api_router.post("/intel/chat")
async def intel_chat(req: IntelRequest):
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="message is required")
    session_id = req.session_id or str(uuid.uuid4())

    async def event_gen():
        full = ""
        # signal session id first
        yield f"data: {json.dumps({'type': 'session', 'session_id': session_id})}\n\n"
        try:
            async for chunk in intel.stream_intel(req.message, session_id):
                full += chunk
                yield f"data: {json.dumps({'type': 'delta', 'content': chunk})}\n\n"
        except Exception as e:
            logger.exception("intel stream failed")
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"
        else:
            try:
                await db.intel_messages.insert_one({
                    "id": str(uuid.uuid4()), "session_id": session_id,
                    "question": req.message, "answer": full,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                })
            except Exception:
                logger.warning("failed to persist intel message")
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(event_gen(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no",
                                      "Connection": "keep-alive"})


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def warm_cache():
    try:
        await zite_client.get_all_tables(force=True)
        logger.info("Zite cache warmed on startup")
    except Exception as e:
        logger.warning(f"cache warm failed: {e}")


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
