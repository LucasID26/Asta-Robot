from pyrogram import filters
from config import bot,prefix

from database.filters_db import del_filter, get_filter, get_filters_names, save_filter

from Asta.decorators.info_cmd import info_cmd
from Asta.decorators.cek_admin import admins_only,bot_admin
from Asta.decorators.pv_or_gc import no_private
from Asta.decorators.error import error

@bot.on_message(filters.command('filter',prefix), group=1)
@info_cmd
@no_private
@bot_admin
@admins_only
@error
async def filter(client, m):
  _key = m.text.split(" ",1)
  chatid = m.chat.id
  if len(m.command) == 1:
    return await m.reply_text("Silahkan masukan kata kunci dan kata respon/reply sticker!")
  if m.reply_to_message is not None:
    key = _key[1].lower()
    if m.reply_to_message.sticker:
      respon = m.reply_to_message.sticker.file_id
      type = "sticker"
    if m.reply_to_message.text:
      respon = m.reply_to_messags.text
      type = "text"
    _filter = {
        "type": type,
        "data": respon,
    }
    await save_filter(chatid, key, _filter)
    await m.reply_text(f"**Save text filter di `{m.chat.title}` :**\n`~ {key}`")
  elif len(m.command) == 2:
    return await m.reply_text("Silahkan masukan respon/reply sticker")
  key_ = m.text.split(" ",2)
  key = key_[1].lower()
  respon = m.text.split(" ",maxsplit=2)[2]
  type = "text"
  _filter = {
        "type": type,
        "data": respon,
    }
  await save_filter(chatid, key, _filter)
  await m.reply_text(f"**Save text filter di `{m.chat.title}` :**\n`~ {key}`")
    

@bot.on_message(filters.command('filters',prefix), group=1)
@info_cmd
@no_private
@bot_admin
@admins_only 
@error
async def filterss(client, m):
  _filters = await get_filters_names(m.chat.id)
  msg = f"**List filters di** {m.chat.title}:\n"
  if not _filters:
    msg += "**-** `[kosong]`"
    return await m.reply_text(msg)
  _filters.sort() 
  for _filter in _filters:
      msg += f"**-** `{_filter}`\n"
  await m.reply_text(msg)
