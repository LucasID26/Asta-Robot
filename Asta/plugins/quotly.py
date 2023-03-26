import asyncio
from config import bot,asisstant,prefix
from pyrogram import filters

from Asta.decorators.info_cmd import info_cmd
from Asta.decorators.cek_admin import bot_admin
from Asta.decorators.error import error
from Asta.func.tools import get_arg

@bot.on_message(filters.command(["q", "quotly"],prefix))
@info_cmd
@bot_admin
@error
async def quotly(client,m):
  args = get_arg(m)
  if not m.reply_to_message and not args:
    return await m.reply_text("**Mohon Balas ke Pesan**")
  Bot = "QuotLyBot"
  if m.reply_to_message:
    msg = await m.reply_text("`Membuat sticker . . .`")
    await asisstant.unblock_user(Bot)
    if args:
      await asisstant.send_message(Bot, f"/qcolor {args}")
      await asyncio.sleep(1)
    else:
      pass
    await asisstant.forward_messages(chat_id=Bot,from_chat_id=m.chat.id,message_ids=m.reply_to_message.id) 
    #await m.reply_to_message.forward(Bot)
    await asyncio.sleep(5)
    async for quotly in asisstant.search_messages(Bot, limit=1):
      if quotly:
        await msg.delete()
        rep = m.id if m.reply_to_message.from_user.is_bot == True else m.reply_to_message.id
        await m.reply_sticker(
                    sticker=quotly.sticker.file_id,
                    reply_to_message_id=rep)
      else:
        return await m.edit("**Gagal Membuat Sticker Quotly**")

