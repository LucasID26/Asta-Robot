from config import prefix,bot,asisstant
import asyncio
from pyrogram import filters
from Asta.decorators.cek_admin import bot_admin
from Asta.decorators.info_cmd import info_cmd
from Asta.decorators.error import error 

gadmin =  [1928677026,5039288972,1868402575,2003697760]
@bot.on_message(filters.command('gcast',prefix) & filters.user(gadmin))
@info_cmd
@bot_admin
@error
async def broadcast(client,m):
  if m.reply_to_message:
    if m.reply_to_message.text:
      gcs = m.reply_to_message.text
      await gas_gcast(m,gcs)
    else:
      return await m.reply('<code>Silahkah balas pesan untuk disiarkan!</code>')
  else:
    if len(m.command) == 1 :
      return await m.reply('<code>Silahkah masukan pesan atau balas pesan untuk disiarkan!</code>')
    else:
      gcs = m.text.split(" ",1)[1]
      await gas_gcast(m,gcs)

  

async def gas_gcast(m, gcs):
  sent = await m.reply("<code>Sedang menyiarkan pesan...</code>")
  pesan = "<b>Data Broadcast :</b>\n\n"
  for akun in [asisstant]:
    nama = (await akun.get_me()).first_name
    sukses = 0
    gagal = 0
    async for dialog in akun.get_dialogs():
      chat_type = dialog.chat.type
      if chat_type.value in ["supergroup","group"]:
        try:
          await akun.send_message(dialog.chat.id,gcs)
          sukses += 1
        except:
          gagal += 1
        #await asyncio.sleep(1)
    pesan += f"{nama} :\nBerhasil :{sukses}\nGagal : {gagal}\n\n"
  await sent.edit(pesan)  