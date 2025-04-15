# 🎵 YouTube Audio URL Extractor API

A blazing-fast ⚡️ FastAPI-based backend that extracts **direct audio stream URLs** from YouTube videos using `yt-dlp`. Perfect for use in your custom music apps, bots, or media streamers.

---

## 🌍 Live Usage

> Paste your YouTube video URL like this:

```
http://localhost:5000/get_audio_url?url=https://youtu.be/kKZCjHz2yEU
```

**Response Example**:

```json
{
  "audio_url": "https://rr3---sn-h5q7dn7d.googlevideo.com/..."
}
```

---

## ✨ Features

- ✅ Extract direct MP4/AAC audio stream links from YouTube
- ⚡️ Fast responses with built-in in-memory **TTL caching**
- 🔒 CORS-enabled (for browser or cross-domain requests)
- 🧠 Caches results for **1 hour** using `cachetools`
- 🛠️ Uses `yt-dlp` under the hood (powerful YouTube downloader)
- 🏗️ Built with **FastAPI** – async, modern, and production-ready

---

## 📆 Installation

### Clone this repo:

```bash
git clone https://github.com/yourusername/youtube-audio-api.git
cd youtube-audio-api
```

### Create virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 📜 `requirements.txt`

```txt
fastapi
uvicorn[standard]
yt-dlp
cachetools==5.3.2
```

---

## 🧪 Running Locally

```bash
uvicorn test:app --reload --port 5000
```

Visit:

```
http://127.0.0.1:5000/
```

And test audio extraction:

```
http://127.0.0.1:5000/get_audio_url?url=https://youtu.be/kKZCjHz2yEU
```

---

## 🧠 Caching Mechanism

This project uses `cachetools.TTLCache` to store recently processed YouTube links.

- 🛠️ **Cache Size**: 1000 entries
- ⏳ **TTL (Time-to-Live)**: 1 hour per entry

This drastically reduces response time for repeated requests and avoids redundant processing via `yt-dlp`.

---

## 🛠 File Structure

```
.
├── test.py                # Main FastAPI application
├── requirements.txt       # Required Python packages
└── README.md              # You're reading it!
```

---

## 📱 Deploy on Vercel (Optional)

You can deploy this API on [Vercel](https://vercel.com/) using their Python runtime.

### Create a `vercel.json` file:

```json
{
  "builds": [
    { "src": "test.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "test.py" }
  ]
}
```

### Deploy using Vercel CLI:

```bash
npm install -g vercel
vercel
```

✅ Done! You'll get a public URL to use.

---

## 📘 API Reference

### `GET /`

```json
{
  "message": "Welcome to the YouTube Audio API!",
  "usage": "/get_audio_url?url=https://youtu.be/kKZCjHz2yEU"
}
```

### `GET /get_audio_url`

#### Parameters:

| Name  | Type     | Description                  |
| ----- | -------- | ---------------------------- |
| `url` | `string` | (required) YouTube video URL |

#### Response:

```json
{
  "audio_url": "https://audio-stream-url"
}
```

---

## 💬 Troubleshooting

- ❌ If a video doesn't return a link, it may be region-restricted, DRM-locked, or blocked from extraction.
- ❌ Ensure `yt-dlp` is installed and available in your environment.
- ✅ You can test `yt-dlp` manually with:
  ```bash
  yt-dlp -g -f bestaudio https://youtu.be/kKZCjHz2yEU
  ```

---

## 👨‍💼 Author

**Harsh Vishwakarma**\
Built with ❤️ using Python, FastAPI, and yt-dlp.



---

## 📄 License

This project is licensed under the MIT License.\
Feel free to fork, build, and improve!

MIT License

Copyright (c) 2025 Harsh Vishwakarma

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
