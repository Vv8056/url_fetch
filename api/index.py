# api/index.py
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from concurrent.futures import ThreadPoolExecutor
from cachetools import TTLCache
from cachetools.keys import hashkey
from yt_dlp import YoutubeDL
import asyncio
import logging
import uvicorn

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

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Thread pool
executor = ThreadPoolExecutor(max_workers=20)

# Cache
audio_cache = TTLCache(maxsize=1000, ttl=3600)

def get_cache_key(url: str):
    return hashkey(url)


# YT-DLP Python Module Wrapper
# async def extract_audio_url(yt_url: str) -> str:
#     key = get_cache_key(yt_url)
#     if key in audio_cache:
#         logger.info(f"Cache hit for: {yt_url}")
#         return audio_cache[key]

#     logger.info(f"Cache miss. Extracting audio for: {yt_url}")
#     loop = asyncio.get_event_loop()

#     try:
#         def run():
#             ydl_opts = {
#                 'quiet': True,
#                 'skip_download': True,
#                 'format': 'bestaudio/best',
#             }
#             with YoutubeDL(ydl_opts) as ydl:
#                 info = ydl.extract_info(yt_url, download=False)
#                 return info['url']

#         audio_url = await loop.run_in_executor(executor, run)
#         audio_cache[key] = audio_url
#         return audio_url

#     except Exception as e:
#         logger.exception("yt-dlp module failed")
#         raise HTTPException(status_code=500, detail="Failed to extract audio URL.")

async def extract_audio_url(url: str) -> str:
    key = keys.hashkey(url)
    if key in cache:
        logger.info(f"Cache hit: {url}")
        return cache[key]

    logger.info(f"Cache miss: {url}. Extracting with yt_dlp...")
    ydl_opts = {
        "quiet": True,
        "format": "bestaudio",
        "skip_download": True
    }

    def run_ytdlp():
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info["url"] if "url" in info else None

    loop = asyncio.get_event_loop()
    audio_url = await loop.run_in_executor(executor, run_ytdlp)

    if not audio_url:
        raise HTTPException(status_code=500, detail="Audio URL not found.")

    cache[key] = audio_url
    return audio_url

@app.get("/")
def root():
    return {
        "message": "Welcome to the YouTube Audio API!",
        "usage": "/get_audio_url?url=https://youtu.be/kKZCjHz2yEU"
    }

# Serve favicon
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

# Audio URL extractor endpoint
# @app.get("/get_audio_url")
# async def get_audio_url(url: str = Query(None, description="YouTube video URL")):
#     if not url:
#         raise HTTPException(status_code=400, detail="Missing YouTube video URL in 'url' query parameter.")
    
#     logger.info(f"Fetching audio URL for: {url}")
#     audio_url = await extract_audio_url(url)
#     return JSONResponse(content={"audio_url": audio_url})

@app.get("/get_audio_url")
async def get_audio_url(url: str = Query(..., description="YouTube video URL")):
    try:
        audio_url = await extract_audio_url(url)
        return JSONResponse(content={"audio_url": audio_url})
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get audio URL.")

# Run the app
if __name__ == "__main__":
    uvicorn.run("index:app")
