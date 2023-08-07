from config import bot,asisstant
from requests import get 
import json 
from pyrogram import filters 
from deep_translator import GoogleTranslator


@bot.on_message(filters.group & ~filters.private,group=2) 
async def chatbott(client,m):
  if m.reply_to_message:
    if m.reply_to_message.from_user.id == (await bot.get_me()).id:
      teks = m.text
      if teks == None:
        return
      nama = "Asta"
      return
      #respone = await get_respone(teks,nama)
      #await bot.send_message(chat_id=m.chat.id,text=respone,reply_to_message_id=m.id)
    elif m.reply_to_message.from_user.id == (await asisstant.get_me()).id:
      teks = m.text
      if teks == None:
        return
      nama = "Melinda"
      respone = await get_respone(teks,nama)
      await asisstant.send_message(chat_id=m.chat.id,text=respone,reply_to_message_id=m.id)
    else:
      pass
  else:
    pass



async def get_tr(code, tr_text):
  return GoogleTranslator(source="auto",target=code).translate(tr_text)

async def get_respone(text, nama):
  if text.startswith('/'):
    return
  req = get(f"http://api.safone.me/chatbot?query={await get_tr('en', text)}&user_id=1928677026&bot_name={nama}&bot_master=Lucas").json()
  if req['status'] == 200:
    return await get_tr('id',req['response'])
  else:
    return "Lagi males ngomong humm"