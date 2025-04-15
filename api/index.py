# api/index.py
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from concurrent.futures import ThreadPoolExecutor
from cachetools import TTLCache
from cachetools.keys import hashkey
import subprocess
import asyncio
import logging

app = FastAPI(
    title="YouTube Audio URL Extractor",
    description="Use /get_audio_url?url=YOUR_YOUTUBE_URL to extract direct audio stream URL.",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Thread pool
executor = ThreadPoolExecutor(max_workers=20)

# Cache
audio_cache = TTLCache(maxsize=1000, ttl=3600)

def get_cache_key(url: str):
    return hashkey(url)

# Subprocess wrapper
async def run_yt_dlp_cached(yt_url: str) -> str:
    key = get_cache_key(yt_url)
    if key in audio_cache:
        logger.info(f"Cache hit for: {yt_url}")
        return audio_cache[key]

    logger.info(f"Cache miss. Running yt-dlp for: {yt_url}")
    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(
            executor,
            lambda: subprocess.check_output(['yt-dlp', '-g', '-f', 'bestaudio', yt_url])
        )
        audio_url = result.decode().strip()
        audio_cache[key] = audio_url
        return audio_url
    except subprocess.CalledProcessError as e:
        logger.error(f"yt-dlp error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch audio URL from yt-dlp.")
    except Exception as e:
        logger.exception("Unexpected error while running yt-dlp")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/")
def root():
    return {
        "message": "Welcome to the YouTube Audio API!",
        "usage": "/get_audio_url?url=https://youtu.be/kKZCjHz2yEU"
    }

@app.get("/get_audio_url")
async def get_audio_url(url: str = Query(None, description="YouTube video URL")):
    if not url:
        raise HTTPException(status_code=400, detail="Missing YouTube video URL in 'url' query parameter.")
    
    logger.info(f"Fetching audio URL for: {url}")
    audio_url = await run_yt_dlp_cached(url)
    return JSONResponse(content={"audio_url": audio_url})
