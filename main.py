import os
import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
from yt_dlp import YoutubeDL

# Railway Variables से डेटा उठाना
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
SESSION = os.environ.get("SESSION_STRING")

# Bot और Assistant को सेटअप करना
bot = Client("MusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
assistant = Client("Assistant", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)
call_py = PyTgCalls(assistant)

@bot.on_message(filters.command("play") & filters.group)
async def play(client, message):
    if len(message.command) < 2:
        return await message.reply("गाने का नाम लिखें! उदाहरण: /play fitoor")
    
    query = " ".join(message.command[1:])
    m = await message.reply("🔎 गाना खोज रहा हूँ...")

    try:
        with YoutubeDL({"format": "bestaudio", "quiet": True}) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            url = info['url']
            title = info['title']

        await call_py.start()
        # नए वर्ज़न के लिए MediaStream का उपयोग
        await call_py.play(message.chat.id, MediaStream(url))
        await m.edit(f"🎵 **बज रहा है:** {title}")
    except Exception as e:
        await m.edit(f"❌ एरर आया: {str(e)}")

@bot.on_message(filters.command("stop") & filters.group)
async def stop(client, message):
    try:
        await call_py.leave_call(message.chat.id)
        await message.reply("⏹ गाना बंद कर दिया गया है।")
    except:
        await message.reply("❌ अभी कोई गाना नहीं चल रहा है।")

# बॉट चालू करना
async def main():
    await bot.start()
    await assistant.start()
    print("बॉट चालू हो गया है!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
