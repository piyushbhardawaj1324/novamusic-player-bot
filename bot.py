import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputStream, InputAudioStream
from pytgcalls.types.input_stream.quality import HighQualityAudio
from yt_dlp import YoutubeDL
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID

app = Client(
    "NovaMusicBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

pytgcalls = PyTgCalls(app)

queues = {}

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply(
        "🎧 **Nova VC Music Bot**\n\n"
        "Commands:\n"
        "/play song\n"
        "/skip\n"
        "/pause\n"
        "/resume\n"
        "/stop"
    )

@app.on_message(filters.command("play"))
async def play(_, message):

    if len(message.command) < 2:
        return await message.reply("❌ Song name do")

    query = " ".join(message.command[1:])
    await message.reply(f"🔎 Searching: {query}")

    ydl_opts = {
    "format": "bestaudio/best",
    "quiet": True,
    "noplaylist": True
}

with YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
    file = info["url"]
    chat_id = message.chat.id

    if chat_id not in queues:
        queues[chat_id] = []

    queues[chat_id].append(file)

    if len(queues[chat_id]) == 1:

        await pytgcalls.join_group_call(
            chat_id,
            InputStream(
                InputAudioStream(
                    file,
                    HighQualityAudio()
                )
            )
        )

        await message.reply(f"🎵 Playing: {info['title']}")

    else:
        await message.reply(f"➕ Added to Queue: {info['title']}")

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

@app.on_message(filters.command("pause"))
async def pause(_, message):
    await pytgcalls.pause_stream(message.chat.id)
    await message.reply("⏸ Paused")

@app.on_message(filters.command("resume"))
async def resume(_, message):
    await pytgcalls.resume_stream(message.chat.id)
    await message.reply("▶ Resumed")

@app.on_message(filters.command("stop"))
async def stop(_, message):

    chat_id = message.chat.id

    queues[chat_id] = []

    await pytgcalls.leave_group_call(chat_id)

    await message.reply("⏹ Stopped")

@app.on_message(filters.command("restart") & filters.user(OWNER_ID))
async def restart(_, message):
    await message.reply("♻ Restarting bot")
    quit()

async def main():

    await app.start()
    await pytgcalls.start()

    print("🎧 Nova VC Music Bot Started")

    await asyncio.Event().wait()

asyncio.run(main())