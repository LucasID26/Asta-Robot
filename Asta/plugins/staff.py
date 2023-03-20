from pyrogram import enums, filters 
from pyrogram.errors import FloodWait
from pyrogram.enums import ChatMemberStatus
from config import *

from Asta.decorators.cek_bot import admins_only,bot_admin
from Asta.decorators.pv_or_gc import no_private
from Asta.decorators.info_cmd import info_cmd
from Asta.decorators.error import error


#ADMIN/STAFF GROUP 
@bot.on_message(filters.command("staff",prefix))
@info_cmd
@no_private
@bot_admin
@admins_only
@error
async def admins(client, message):
  try: 
    adminList = []
    ownerList = []
    async for admin in bot.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
      if admin.privileges.is_anonymous == False:
        if admin.user.is_bot == True:
          pass
        elif admin.status == ChatMemberStatus.OWNER:
          ownerList.append(admin.user)
        else:  
          adminList.append(admin.user)
      else:
        pass   
    lenAdminList= len(ownerList) + len(adminList)  
    text2 = f"**GROUP STAFF - {message.chat.title}**\n\n"
    try:
      owner = ownerList[0]
      if owner.username == None:
        text2 += f"👑 Owner\n└ {owner.mention}\n\n👮🏻 Admins\n"
      else:
        text2 += f"👑 Owner\n└ @{owner.username}\n\n👮🏻 Admins\n"
    except:
      text2 += f"👑 Owner\n└ <i>Hidden</i>\n\n👮🏻 Admins\n"
    if len(adminList) == 0:
      text2 += "└ <i>Admins are hidden</i>"
      await message.reply_text(text2) 
    else:  
      while len(adminList) > 1:
        admin = adminList.pop(0)
        if admin.username == None:
          text2 += f"├ {admin.mention}\n"
        else:
          text2 += f"├ @{admin.username}\n"    
      else:    
        admin = adminList.pop(0)
        if admin.username == None:
          text2 += f"└ {admin.mention}\n\n"
        else:
          text2 += f"└ @{admin.username}\n\n"
      text2 += f"✅ | **Total number of admins**: {lenAdminList}\n❌ | Bots and hidden admins were rejected." 
      await message.reply_text(text2) 
  except FloodWait as e:
    await asyncio.sleep(e.value) 
