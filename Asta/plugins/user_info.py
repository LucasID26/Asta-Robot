from config import bot, prefix
from pyrogram import filters,enums
import os
from html import escape

from Asta.func.cek_admin import bot_admin,admins_only
fron Asta.func.info_cmd import info_cmd
from Asta.func.error import error

async def get_user_info(m,user):
    try:
      member = await bot.get_chat_member(m.chat.id,user)
      status_in_group = member.status.value
    except:
      status_in_group = "❓"
    base_user_info = await bot.get_users(user)
    get_user = await bot.get_chat(user) 
    photo_count = await bot.get_chat_photos_count(user)
    user_id = base_user_info.id
    first_name = base_user_info.first_name
    last_name = base_user_info.last_name 
    username = base_user_info.username
    user_info = {
        "id": user_id,
        "dc": base_user_info.dc_id,
        "photo_id": base_user_info.photo.big_file_id if base_user_info.photo else None,
        "first_name": escape(first_name) if first_name else "None",
        "last_name": last_name if last_name else "None",
        "user_name": username if username else "None",
        "user_mension": base_user_info.mention,
        "is_contact": "Yes" if base_user_info.is_contact else "No",
        "is_bot": "Yes" if base_user_info.is_bot else "No",
        "is_scam": "Yes" if base_user_info.is_scam else "No",
        "status": base_user_info.status.value if base_user_info.is_bot == False else "None",
        "bio": get_user.bio, 
        "user?": "USER" if base_user_info.is_bot == False else "BOT", 
        "photo_count": photo_count, 
        "status_in_group": status_in_group, 
        "premium": "Yes" if base_user_info.is_premium else "No",
        "lang_code": base_user_info.language_code if base_user_info.language_code else "❓"
    }
    return user_info 

@bot.on_message(filters.command("info",prefix))
@info_cmd
@bot_admin
@error
async def info(client, m):
  if m.reply_to_message:
    userid = m.reply_to_message.from_user.id
  elif len(m.command) == 1:
    userid = m.from_user.id
  else:
    userid = m.text.split(" ",1)[1] 
  try:
    get = await bot.get_chat(userid)
  except:
    return await m.reply_text("Masukan username/user_id yang valid!")
  if get.type.value in ['supergroup','channel']:
    g_title = get.title
    g_id = get.id 
    g_type = get.type.value 
    g_username = "@"+get.username if get.username else None 
    msg = await m.reply_text(f"__Get {g_type.upper()} info...__")
    g_text = f"""
__**{g_type.upper()} INFO**__

**• Title:** {g_title}
**• Username:** {g_username} 
**• Type:** {g_type}
**• ID:** `{g_id}`
"""
    return await msg.edit(g_text)

  chatid = m.chat.id
  usr_info = await get_user_info(m,userid)
  has_photo = usr_info['photo_id']
  msg = await m.reply_text(f"__Get {usr_info['user?']} info...__")
  user_info_text = f"""
<i><b>{usr_info['user?']} INFO</b></i>

<b>• First Name:</b> {usr_info["first_name"]}
<b>• Last Name:</b> {usr_info["last_name"]}
<b>• User Name:</b> @{usr_info["user_name"]}
<b>• Mention:</b> {usr_info["user_mension"]}
<b>• User ID:</b> <code>{usr_info["id"]}</code>
<b>• Status User:</b> {usr_info['status'].upper()}
<b>• Status in Group:</b> {usr_info["status_in_group"]}
<b>• Bio:</b> {usr_info['bio']}
<b>• Photo Count:</b> {usr_info["photo_count"]}
<b>• DC ID:</b> {usr_info["dc"]}
<b>• Is Bot?:</b> {usr_info["is_bot"]}
<b>• Is Premium?:</b> {usr_info["premium"]}
<b>• Lang Code:</b> {usr_info["lang_code"]}

"""
  if m.chat.type.value != 'private' and m.chat.permissions.can_send_media_messages:    
    if has_photo:
      usr_dp = await bot.download_media(has_photo)
      await bot.send_photo(chat_id=m.chat.id,photo=usr_dp, caption=user_info_text, reply_to_message_id=m.id,parse_mode=enums.ParseMode.HTML)
      await msg.delete()
      os.remove(usr_dp)
    else:
      await msg.edit(user_info_text,parse_mode=enums.ParseMode.HTML)
  else:
    await msg.edit(user_info_text,parse_mode=enums.ParseMode.HTML) 

@bot.on_message(filters.command("id",prefix))
@info_cmd
@bot_admin
@error
async def iid(client, m):
  await m.reply_text(f"**Chat ID:** `{m.chat.id}`")
