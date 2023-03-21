from config import bot,prefix
import requests,os
import json 
from pyrogram import filters

from Asta.decorators.cek_admin import bot_admin
from Asta.decorators.info_cmd import info_cmd
from Asta.decorators.error import error


@bot.on_message(filters.command("asupan",prefix))
@info_cmd
@bot_admin
@error
async def fyp(client,m):
  msg = await m.reply_text("__Lagi milih yang sedep!__")
  url = "https://apimu.my.id/asupan/tiktok"
  nama_file = os.path.basename(url)
  response = requests.get(url)

  with open(nama_file, "wb") as f:
    f.write(response.content)
  await m.reply_video(nama_file)
  os.remove(nama_file)
  await msg.delete()
