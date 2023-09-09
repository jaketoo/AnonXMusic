import requests
import asyncio
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.exceptions import NoActiveGroupCall, TelegramServerError, AlreadyJoinedError

from AnonXMusic import app

active_groups = []

def get_prayer_times(address, method, school):
    url = f"http://api.aladhan.com/timingsByAddress?address={address}&method={method}&school={school}"
    response = requests.get(url)
    data = response.json()
    prayer_times = data.get("data", {}).get("timings", {})
    return prayer_times

async def play_prayer_times():
    while True:
        current_time = datetime.now()
        address = "Cairo"
        method = 4
        school = 0
        prayer_times = get_prayer_times(address, method, school)
        for prayer_name, prayer_time in prayer_times.items():
            if prayer_name.lower() in ["fajr", "dhuhr", "asr", "maghrib", "isha"]:
                prayer_time_obj = datetime.strptime(prayer_time, "%H:%M")
                time_difference = prayer_time_obj - current_time
                if timedelta(minutes=0) <= time_difference <= timedelta(minutes=5):
                    for chat_id in active_groups:
                        try:
                            await app.join_group_call(chat_id, AudioPiped("AnonXMusic/azan.mp3"), stream_type=StreamType().pulse_stream)
                            await app.send_message(chat_id, f"حان وقت صلاة {prayer_name} 🕌")
                        except (NoActiveGroupCall, TelegramServerError, AlreadyJoinedError):
                            pass
        await asyncio.sleep(300)

@app.on_message(filters.command("تفعيل الاذان", "") & filters.group)
async def enable_prayer_times_command(client, message):
    chat_id = message.chat.id
    if chat_id not in active_groups:
        active_groups.append(chat_id)
        await message.reply("تم تفعيل الأذان لهذه المجموعة.")
    else:
        await message.reply("الأذان مفعل بالفعل لهذه المجموعة.")

@app.on_message(filters.command("تعطيل الاذان", "") & filters.group)
async def disable_prayer_times_command(client, message):
    chat_id = message.chat.id
    if chat_id in active_groups:
        active_groups.remove(chat_id)
        await message.reply("تم تعطيل الأذان لهذه المجموعة.")
    else:
        await message.reply("الأذان معطل بالفعل لهذه المجموعة.")

asyncio.create_task(play_prayer_times())