from pyrogram import Client, filters
from yt_dlp import YoutubeDL

OWNER_ID = 6317313711
API_ID = 36845222
API_HASH = "YOUR_API_HASH"
BOT_TOKEN = "YOUR_BOT_TOKEN"

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

    ydl_opts = {"format": "bestaudio"}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{song}", download=False)['entries'][0]
        url = info['url']

    await message.reply(f"🎧 Playing: {info['title']}")
    
app.run()