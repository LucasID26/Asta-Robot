from pyrogram import filters, enums
from pyrogram.errors import FloodWait 
from config import bot,prefix
import asyncio 

from Asta.decorators.cek_admin import admins_only,bot_admin
from Asta.decorators.pv_or_gc import no_private
from Asta.decorators.error import error


@bot.on_message(filters.command("bots",prefix) & ~filters.private) 
@no_private 
@bot_admin
@admins_only 
@error
async def list_bots(client, message):  
  try:
    botList = []
    async for bots in bot.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BOTS):
      botList.append(bots.user)
    lenBotList = len(botList) 
    text3  = f"**BOT LIST - {message.chat.title}**\n\n🤖 Bots\n"
    while len(botList) > 1:
      bots = botList.pop(0)
      text3 += f"├ {bots.mention}\n"    
    else:    
      bots = botList.pop(0)
      text3 += f"└ {bots.mention}\n\n"
      text3 += f"✅ | **Total jumlah bot**: {lenBotList}"
      await message.reply(text=text3) 
  except Exception as e:
    await message.reply(e,quote=True)


