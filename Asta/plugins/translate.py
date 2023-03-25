from config import bot,prefix
from pyrogram import filters

from Asta.func.translate import translate
from Asta.decorators.info_cmd import info_cmd
from Asta.decorators.cek_admin import bot_admin
from Asta.decorators.error import error


@bot.on_message(filters.command(['tr','trans','translate'],prefix))
async def trans(client,m):
  if len(m.command) == 1:
    return await m.reply_text("Google Translate,/tr [kode bhs] [text]")
  try:
    if m.reply_to_message is not None:
      text = m.reply_to_message.text 
    else:
      text = m.text.split(" ",2)[2]
    code = m.text.split(" ",1)[1]
    tr = translate(code,text)
    hasil = f"**Hasil translate ke {code}\n`{tr}`"
    await m.reply_text(hasil)
  except:
    await m.reply_text("Terjadi kesalahan")
