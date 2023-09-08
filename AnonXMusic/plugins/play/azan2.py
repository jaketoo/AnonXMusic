import time
import requests 
from pyrogram import Client, filters

async def get_prayer_times(address, method, school):
    url = f"http://api.aladhan.com/timingsByAddress?address={address}&method={method}&school={school}"
    response = requests.get(url)
    data = response.json()
    return data["data"]["timings"]

        address = "Cairo"
        method = 4  
        school = 0  
        prayer_times = await get_prayer_times(address, method, school)
        times_message = f"أوقات الصلاة في {address}:\n"
        times_message += f"الفجر: {prayer_times['Fajr']}\n"
        times_message += f"الشروق: {prayer_times['Sunrise']}\n"
        times_message += f"الظهر: {prayer_times['Dhuhr']}\n"
        times_message += f"العصر: {prayer_times['Asr']}\n"
        times_message += f"المغرب: {prayer_times['Maghrib']}\n"
        times_message += f"العشاء: {prayer_times['Isha']}\n"
        await message.reply_text(times_message)
active = True 

async def azan2():
    assistant = await group_assistant(Anon,message.chat.id)<
    tryp
        await assistant.join_group_call(message.chat.id, AudioPiped("./AnonX/assets/azan.mp3"), stream_type=StreamType().pulse_stream)
        text="حان الان موعد الاذان :"
        await message.reply(f"{text}")
        await asyncio.sleep(7)
        await assistant.leave_group_call(message.chat.id)
    except NoActiveGroupCall:
        await message.reply(f"الكول مقفول اصلا يصاحبي")
    except AlreadyJoinedError:
        text="حان الان موعد الاذان :"
        participants = await assistant.get_participants(message.chat.id)
        await message.reply(f"{text}")
        get_prayer_times(address, method, school)
    while not await asyncio.sleep(prayer_times['Asr']):
    for i in chat:
       try:
         await app.send_message(i, random.choice(azan2))
       except:
         pass

asyncio.create_task(azan2())

