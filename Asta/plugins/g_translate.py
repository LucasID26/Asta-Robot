from pyrogram import filters 
from config import bot,prefix 

from requests import get 
from bs4 import BeautifulSoup as BF 
from deep_translator import GoogleTranslator  

from Asta.decorators.info_cmd import info_cmd 
from Asta.decorators.cek_admin import bot_admin 
from Asta.decorators.error import error 
from Asta.func.tools import HTTP


async def tr_bali(query):
  req = get(f"https://translate.glosbe.com/id-ban/{query}") 
  bf = BF(req.content,'html.parser') 
  hasil = bf.find('div',class_='w-full h-full bg-gray-100 h-full border p-2 min-h-25vh sm:min-h-50vh whitespace-pre-wrap break-words')
  try:
    return hasil 
  except Exception as e:
    return f"<b>ERROR :</b>\n<code>{e}</code>"

@bot.on_message(filters.command(['tr','trans','translate'],prefix))
@info_cmd
@bot_admin
@error 
async def translate(client,m):
  if m.reply_to_message:
    if not m.reply_to_message.text:
      return await m.reply("Silahkan reply pesan!!")
    text = m.reply_to_message.text
  elif len(m.command) == 1:
    return await m.reply("Silahkan masukan kode bahasa dan text/reply pesan!!")
  elif not m.reply_to_message:
    text = m.text.split(" ",2)[2]
  lang = m.text.split(" ",2)
  if lang[1] == "bl":
    tr = await tr_bali(text) 
  elif lang[1] != "bl":
    try:
      tr = GoogleTranslator(source="auto",target=lang[1]).translate(text)
    except:
      return await m.reply("Silahkan masukan format dengan benar\nContoh : /tr en hallo")
  pesan = f"<b>Hasil Translate ke {lang[1]}:</b>\n\n<code>{tr}</code>"
  await m.reply(pesan)



