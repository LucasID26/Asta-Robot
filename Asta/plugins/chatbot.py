from config import bot,asisstant,asisstant2 
from requests import get 
import json 
from pyrogram import filters 
from deep_translator import GoogleTranslator


@bot.on_message(filters.group & ~filters.private) 
#@asisstant.on_message(filters.group & ~filters.private) 
#@asisstant2.on_message(filters.group & ~filters.private) 
async def chatbott(client,m):
  if m.reply_to_message:
    if m.reply_to_message.from_user.id == (await bot.get_me()).id:
      teks = m.text
      if teks == None:
        return
      nama = "Asta"
      respone = get_respone(teks,nama)
      await bot.send_message(chat_id=m.chat.id,text=respone,reply_to_message_id=m.id)
    elif m.reply_to_message.from_user.id == (await asisstant.get_me()).id:
      teks = m.text
      if teks == None:
        return
      nama = "Melinda"
      respone = get_respone(teks,nama)
      await asisstant.send_message(chat_id=m.chat.id,text=respone,reply_to_message_id=m.id)
    elif m.reply_to_message.from_user.id == (await asisstant2.get_me()).id:
      teks = m.text
      if teks == None:
        return
      nama = "Ayinaa"
      respone = get_respone(teks,nama)
      await asisstant2.send_message(chat_id=m.chat.id,text=respone,reply_to_message_id=m.id)
  else:
    pass



def get_tr(code, tr_text):
  return GoogleTranslator(source="auto",target=code).translate(tr_text)

def get_respone(text, nama):
  req = get(f"http://api.safone.me/chatbot?query={get_tr('en', text)}&user_id=1928677026&bot_name={nama}&bot_master=Lucas").json()
  if req['status'] == 200:
    return get_tr('id',req['response'])
  else:
    return "Lagi males ngomong humm"