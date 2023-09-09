import asyncio
import random
import requests
from AnonXMusic import app
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from AnonXMusic.core.call import Anony
from AnonXMusic.utils.database import *
from pytgcalls.exceptions import NoActiveGroupCall, AlreadyJoinedError

chat = []

async def get_prayer_times(address, method, school):
    url = f"http://api.aladhan.com/timingsByAddress?address={address}&method={method}&school={school}"
    response = requests.get(url)
    data = response.json()
    prayer_times = data["data"]["timings"]
    times_message = f"أوقات الصلاة في {address}:\n"
    times_message += f"الفجر: {prayer_times['Fajr']}\n"
    times_message += f"الشروق: {prayer_times['Sunrise']}\n"
    times_message += f"الظهر: {prayer_times['Dhuhr']}\n"
    times_message += f"العصر: {prayer_times['Asr']}\n"
    times_message += f"المغرب: {prayer_times['Maghrib']}\n"
    times_message += f"العشاء: {prayer_times['Isha']}\n"
    return times_message

async def azan2(address, method, school, message):
    url = f"http://api.aladhan.com/timingsByAddress?address={address}&method={method}&school={school}"
    response = requests.get(url)
    data = response.json()
    prayer_times = data["data"]["timings"]
    assistant = await group_assistant(Anony, message.chat.id)
    try:
        await assistant.join_group_call(message.chat.id, AudioPiped("./AnonXMusic/assets/azan.mp3"), stream_type=StreamType().pulse_stream)
        text = "حان الآن موعد الأذان:"
        await message.reply(text)
        await asyncio.sleep(7)
        await assistant.leave_group_call(message.chat.id)
    except NoActiveGroupCall:
        await message.reply("المكالمة الجماعية مغلقة.")
    except AlreadyJoinedError:
        text = "حان الآن موعد الأذان:"
        await message.reply(text)
    await asyncio.sleep(prayer_times['Asr'])
    for i in chat:
        try:
            await app.send_message(i, random.choice(azan2))
        except:
            pass

asyncio.create_task(azan2())