import os
from config import bot,own,prefix
from pyrogram import filters

from Asta.decorators.info_cmd import info_cmd
from Asta.decorators.cek_admin import bot_admin
from Asta.decorators.error import error



@bot.on_message(filters.command('debug',prefix))
@info_cmd
@bot_admin
@error
async def debug_cmd(client,m):
  if m.reply_to_message is not None:
    debug = m.reply_to_message
  else:
    debug = m
  hasil = f"<b>HASIL-DEBUG:</b>\n<code>{debug}</code>"
  if len(hasil) >= 4096:
    with open("Asta_Debug.txt","w+",encoding="utf8") as dbg:
      dbg.write(hasil)
    return await m.reply_document("Asta_Debug.txt",caption="<b>HASIL-DEBUG</b>")
  else:
    return await m.reply_text(hasil)
