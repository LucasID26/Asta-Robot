from config import asisstant,asisstant2
import asyncio


async def share_link():
  while True:
    await asisstant.send_message('chatbot','/next')
    await asisstant2.send_message('chatbot','/next')
    await asyncio.sleep(5)
    await asisstant.send_message('chatbot', 'ᴍᴜᴛᴜᴀʟᴀɴ ᴄʜᴀᴛ ɢʀᴏᴜᴘ 🔞\n𝗚𝗔𝗥𝗜𝗦 𝗞𝗘𝗥𝗔𝗦 𝗨𝗡𝗧𝗨𝗞 𝗢𝗥𝗔𝗡𝗚-𝗢𝗥𝗔𝗡𝗚 𝗦𝗢𝗞 𝗞𝗘𝗥𝗔𝗦 !!!\nINFO/LINK GC:\n https://t.me/mischief54')
    await asisstant2.send_message('chatbot', 'ᴍᴜᴛᴜᴀʟᴀɴ ᴄʜᴀᴛ ɢʀᴏᴜᴘ 🔞\n𝗚𝗔𝗥𝗜𝗦 𝗞𝗘𝗥𝗔𝗦 𝗨𝗡𝗧𝗨𝗞 𝗢𝗥𝗔𝗡𝗚-𝗢𝗥𝗔𝗡𝗚 𝗦𝗢𝗞 𝗞𝗘𝗥𝗔𝗦 !!!\nINFO/LINK GC:\n https://t.me/mischief54')
    await asisstant.send_message('chatbot','/stop')
    await asisstant2.send_message('chatbot','/stop')
    await asyncio.sleep(59)