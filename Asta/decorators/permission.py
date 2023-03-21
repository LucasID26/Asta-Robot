from config import bot,own
from functools import wraps
from pyrogram import enums
from time import time


admins_in_chat = {}

async def list_admin(chat_id: int):
  global admins_in_chat
  if chat_id in admins_in_chat:
    interval = time() - admins_in_chat[chat_id]["last_updated_at"]
    if interval < 3600:
      return admins_in_chat[chat_id]["data"]

    admins_in_chat[chat_id] = {
        "last_updated_at": time(),
        "data": [member.user.id async for member in bot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS)],
    }
    return admins_in_chat[chat_id]["data"]




async def member_permissions(chat_id: int, user_id: int):
  perms = []
  try:
    member = await bot.get_chat_member(chat_id, user_id)
    perijinan = member.privileges
  except Exception:
    return []
  if member.status != enums.ChatMemberStatus.MEMBER:
    if perijinan.can_post_messages:
      perms.append("can_post_messages")
    if perijinan.can_edit_messages:
      perms.append("can_edit_messages")
    if perijinan.can_delete_messages:
      perms.append("can_delete_messages")
    if perijinan.can_restrict_members:
      perms.append("can_restrict_members")
    if perijinan.can_promote_members:
      perms.append("can_promote_members")
    if perijinan.can_change_info:
      perms.append("can_change_info")
    if perijinan.can_invite_users:
      perms.append("can_invite_users")
    if perijinan.can_pin_messages:
      perms.append("can_pin_messages")
    if perijinan.can_manage_video_chats:
      perms.append("can_manage_video_chats")
  return perms 


def izin(permission):
  def subFunc(func):
    @wraps(func)
    async def subFunc2(client, message, *args, **kwargs):
      chatID = message.chat.id
      if not message.from_user:
        # For anonymous admins
        if message.sender_chat and message.sender_chat.id == message.chat.id:
            return await message.reply_text(f"Anda tidak memiliki izin yang diperlukan untuk melakukan tindakan ini.\n**Izin:** {permission}")
      # For admins and sudo users
      userID = message.from_user.id
      permissions = await member_permissions(chatID, userID)
      if userID not in own and permission not in permissions:
        return await message.reply_text(f"Anda tidak memiliki izin yang diperlukan untuk melakukan tindakan ini.\n**Izin:** {permission}")
  
      return await func(client, message, *args, **kwargs)
    return subFunc2

  return subFunc
