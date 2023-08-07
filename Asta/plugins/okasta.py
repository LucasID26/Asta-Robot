from config import bot 
from requests import get 
import json
import os

from pyrogram import filters 
from Asta.decorators.error import error

@bot.on_message(filters.text,group=3)
@error
async def ok_asta(client,m):
  teks = m.text
  if not m.text:
    return 
  cmd = teks.upper()
  if cmd.startswith('OK ASTA'):
    teks2 = teks.split(" ",2)   
    if len(teks2) == 2:
      return await m.reply("Ada yang bisa saya bantu?")
    sent = await m.reply("<code>Mencari informasi yang terkait...</code>")
    req = get(f"https://yasirapi.eu.org/bard?input={teks2[2]}").json()
    try:
      content = req['content']
      link = req['links']
      if len(link) != 0:
        try:
          await m.reply_photo(photo=link[0],caption=content)
        except:
          await m.reply_video(video=link[0],caption=content)
        await sent.delete()
      else:
        await sent.edit(content)
    except:
      await sent.edit("Sedang mengalami gangguan silahkan coba lain kali!")
  