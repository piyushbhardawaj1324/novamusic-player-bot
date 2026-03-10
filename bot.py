import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputStream, InputAudioStream
from pytgcalls.types.input_stream.quality import HighQualityAudio
from yt_dlp import YoutubeDL

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("musicbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
pytgcalls = PyTgCalls(app)

queues = {}

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply("🎧 VC Music Bot Online\nUse /play songname")

@app.on_message(filters.command("play"))
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply("❌ Song name do")

    query = " ".join(message.command[1:])
    await message.reply(f"🔎 Searching: {query}")

    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": "%(title)s.%(ext)s",
        "quiet": True
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
        file = ydl.prepare_filename(info)

    chat_id = message.chat.id

    if chat_id in queues:
        queues[chat_id].append(file)
        return await message.reply(f"➕ Added to queue\n🎵 {info['title']}")

    queues[chat_id] = [file]

    await pytgcalls.join_group_call(
        chat_id,
        InputStream(
            InputAudioStream(
                file,
                HighQualityAudio()
            )
        )
    )

    await message.reply(f"🎶 Playing: {info['title']}")

@app.on_message(filters.command("skip"))
async def skip(_, message):
    chat_id = message.chat.id

    if chat_id not in queues or len(queues[chat_id]) == 0:
        return await message.reply("❌ Queue empty")

    queues[chat_id].pop(0)

    if len(queues[chat_id]) == 0:
        await pytgcalls.leave_group_call(chat_id)
        return await message.reply("⏹ Queue finished")

    next_song = queues[chat_id][0]

    await pytgcalls.change_stream(
        chat_id,
        InputStream(
            InputAudioStream(
                next_song,
                HighQualityAudio()
            )
        )
    )

    await message.reply("⏭ Skipped")

@app.on_message(filters.command("stop"))
async def stop(_, message):
    chat_id = message.chat.id

    queues.pop(chat_id, None)
    await pytgcalls.leave_group_call(chat_id)

    await message.reply("⏹ Music stopped")

app.start()
pytgcalls.start()
app.idle()