import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pyrogram import Client, filters
from pyrogram.types import Message
import yt_dlp

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running 24/7!")

def run_web():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_web, daemon=True).start()

API_ID = 2189301
API_HASH = "fbd6c0abb44f8d0f8e531902db22aae2"
BOT_TOKEN = "8982220297:AAFIY-_0iftJ6GMqbOscSdEl1jyAwZCWQ_0"

app = Client("video_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_cmd(client, message: Message):
    await message.reply_text("🎬 أهلاً بك! أرسل لي رابط فيديو من (Instagram, TikTok, YouTube, Facebook) وسأقوم بتحميله لك فوراً.")

@app.on_message(filters.text & ~filters.command(["start"]) & ~filters.me)
async def download_video(client, message: Message):
    if message.from_user and message.from_user.is_self:
        return

    url = message.text.strip()
    if not (url.startswith("http://") or url.startswith("https://")):
        await message.reply_text("⚠️ يرجى إرسال رابط صحيح يبتدأ بـ http أو https")
        return

    msg = await message.reply_text("🔍 جاري معالجة الرابط وتحميل الفيديو...")

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'quiet': True,
        'outtmpl': '%(title)s.%(ext)s',
        'max_filesize': 50 * 1024 * 1024,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_file = ydl.prepare_filename(info)

        await msg.edit_text("⬆️ جاري رفع الفيديو إلى تيليجرام...")
        await message.reply_video(video_file, caption=f"🎥 {info.get('title', 'فيديو')}")
        await msg.delete()

        if os.path.exists(video_file):
            os.remove(video_file)

    except Exception as e:
        await msg.edit_text(f"❌ حدث خطأ أثناء التحميل:\n{e}")

if __name__ == "__main__":
    app.run()
