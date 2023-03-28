from config import bot,prefix
from pyrogram import filters

from Asta.func.translate import trbali
from Asta.decorators.info_cmd import info_cmd
from Asta.decorators.cek_admin import bot_admin
from Asta.decorators.error import error


@bot.on_message(filters.command('trbali',prefix))
@info_cmd
@bot_admin
@error
async def trans(client,m):
  if len(m.command) == 1:
    return await m.reply_text("Google Translate Bhs Bali, /bali [text]")
  try:
    if m.reply_to_message is not None:
      if not m.reply_to_message.text:
        return await m.reply_text("Reply pesan bukan media")
      text = m.reply_to_message.text 
    else:
      text = m.text.split(" ",1)[1]
    tr = trbali(text)
    hasil = f"**Hasil translate ke Bhs Bali**\n\n`{tr}`"
    await m.reply_text(hasil)
  except:
    await m.reply_text("Pastikan format sudah benar")
