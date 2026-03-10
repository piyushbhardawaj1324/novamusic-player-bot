import os
from pyrogram import Client, filters
from yt_dlp import YoutubeDL

OWNER_ID = int(os.getenv("OWNER_ID"))
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("musicbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("🎵 Nova Melody Music Bot Online\nUse /play songname")

@app.on_message(filters.command("play"))
async def play(client, message):
    if len(message.command) < 2:
        return await message.reply("❌ Song name do")

    song = " ".join(message.command[1:])
    await message.reply(f"🔎 Searching: {song}")

    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": "song.%(ext)s"
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{song}", download=True)['entries'][0]
        file = ydl.prepare_filename(info)

    await message.reply_document(file, caption=f"🎧 {info['title']}")
app.run()