from config import bot,own,prefix 
from pyrogram import filters 
import asyncio
from pyrogram.errors import UserNotParticipant 
from pyrogram.types import ChatPermissions

from Asta.decorators.permission import izin,list_admin
from Asta.decorators.cek_admin import admins_only,bot_admin
from Asta.decorators.pv_or_gc import no_private
from Asta.decorators.info_cmd import info_cmd
from Asta.decorators.error import error


#KICK MEMBER
@bot.on_message(filters.command(['kick','dkick'],prefix))
@info_cmd
@no_private 
@bot_admin
@admins_only
@izin("can_restrict_members")
@error
async def kicked(client,m):
  if m.reply_to_message is not None:
    users = m.reply_to_message.from_user.id
  elif len(m.command) == 1:
    return await m.reply_text("Silahkan reply user/cantumkan username pengguna!")
  else:
    users = m.text.split(" ",1)[1]
  try:
    user = await bot.get_chat_member(m.chat.id,users)
  except UserNotParticipant:
    return await m.reply_text("User bukan anggota dari group ini!")
  except :
    return await m.reply_text("Username tidak valid!")
  if user.user.id == client.me.id:
    return await m.reply_text("Anda mau kick saya?,saya bisa keluar sendiri bung!")
  elif user.user.id in own:
    return await m.reply_text("Oops tidak bisa karena beliau owner saya!")
  
  elif user.status.value in ['owner','administrator']:
    return await m.reply_text("Oops tidak bisa karena dia admin!")  
  mention = user.user.mention
  text = f"""
**Banned User:** {mention}
**By: {m.from_user.mention if m.from_user else 'Anon'}
"""
  if m.command[0][0] == "d":
    try:
      await m.reply_to_message.delete()
    except:
      pass
  await m.chat.ban_member(user.user.id)
  await m.reply_text(text)
  await asyncio.sleep(1)
  await m.chat.unban_member(user.user.id) 


@bot.on_message(filters.command(['ban','dban'],prefix))
@info_cmd
@no_private 
@bot_admin
@admins_only
@izin("can_restrict_members")
@error
async def banned(client,m):
  if m.reply_to_message is not None:
    users = m.reply_to_message.from_user.id
  elif len(m.command) == 1:
    return await m.reply_text("Silahkan reply user/cantumkan username pengguna!")
  else:
    users = m.text.split(" ",1)[1]
  try:
    user = await bot.get_chat_member(m.chat.id,users) 
    if user.status.value == 'banned':
      return await m.reply_text("User sudah ada dalam daftar banned group ini!")
  except UserNotParticipant:
    return await m.reply_text("User bukan anggota dari group ini!")
  except :
    return await m.reply_text("Username tidak valid!")
  if user.user.id == client.me.id:
    return await m.reply_text("Anda mau ban saya?,saya bisa keluar sendiri bung!")
  elif user.user.id in own:
    return await m.reply_text("Oops tidak bisa karena beliau owner saya!")
  
  elif user.status.value in ['owner','administrator']:
    return await m.reply_text("Oops tidak bisa karena dia admin!")  
  mention = user.user.mention
  text = f"""
**Banned User:** {mention}
**By: {m.from_user.mention if m.from_user else 'Anon'}
"""
  if m.command[0][0] == "d":
    try:
      await m.reply_to_message.delete()
    except:
      pass
  await m.chat.ban_member(user.user.id)
  await m.reply_text(text)


@bot.on_message(filters.command(['unban'],prefix))
@info_cmd
@no_private 
@bot_admin
@admins_only
@izin("can_restrict_members")
@error
async def unbanned(client,m):
  if m.reply_to_message is not None:
    users = m.reply_to_message.from_user.id
  elif len(m.command) == 1:
    return await m.reply_text("Silahkan reply user/cantumkan username pengguna!")
  else:
    users = m.text.split(" ",1)[1]
  try:
    user = await bot.get_chat_member(m.chat.id,users) 
  except UserNotParticipant:
    return await m.reply_text("User bukan anggota dari group ini!")
  except :
    return await m.reply_text("Username tidak valid!") 
  if user.status.value == 'banned':
    mention = user.user.mention
    text = f"""
**Unbanned User:** {mention}
**By: {m.from_user.mention if m.from_user else 'Anon'}
"""
    await m.chat.unban_member(user.user.id)
    return await m.reply_text(text) 
  elif user.status.value != 'banned':
    return await m.reply_text("User tidak ada dalam daftar banned group ini!")


#MUTE MEMBER 
@bot.on_message(filters.command(['mute','dmute'],prefix))
@info_cmd
@no_private 
@bot_admin
@admins_only
@izin("can_restrict_members")
@error
async def muted(client,m):
  if m.reply_to_message is not None:
    users = m.reply_to_message.from_user.id
  elif len(m.command) == 1:
    return await m.reply_text("Silahkan reply user/cantumkan username pengguna!")
  else:
    users = m.text.split(" ",1)[1]
  try:
    user = await bot.get_chat_member(m.chat.id,users) 
    if user.status.value == 'restricted':
      return await m.reply_text("User sudah ada dalam daftar muted group ini!")
  except UserNotParticipant:
    return await m.reply_text("User bukan anggota dari group ini!")
  except :
    return await m.reply_text("Username tidak valid!")
  if user.user.id == client.me.id:
    return await m.reply_text("Anda mau mute saya?")
  elif user.user.id in own:
    return await m.reply_text("Oops tidak bisa karena beliau owner saya!")
  
  elif user.status.value in ['owner','administrator']:
    return await m.reply_text("Oops tidak bisa karena dia admin!")  
  mention = user.user.mention
  text = f"""
**Muted User:** {mention}
**By: {m.from_user.mention if m.from_user else 'Anon'}
"""
  if m.command[0][0] == "d":
    try:
      await m.reply_to_message.delete()
    except:
      pass
  await bot.restrict_chat_member(m.chat.id, user.user.id, ChatPermissions())
  await m.reply_text(text) 


@bot.on_message(filters.command(['unmute'],prefix))
@info_cmd
@no_private 
@bot_admin
@admins_only
@izin("can_restrict_members")
@error
async def unmute(client,m):
  if m.reply_to_message is not None:
    users = m.reply_to_message.from_user.id
  elif len(m.command) == 1:
    return await m.reply_text("Silahkan reply user/cantumkan username pengguna!")
  else:
    users = m.text.split(" ",1)[1]
  try:
    user = await bot.get_chat_member(m.chat.id,users) 
  except UserNotParticipant:
    return await m.reply_text("User bukan anggota dari group ini!")
  except :
    return await m.reply_text("Username tidak valid!") 
  if user.status.value == 'restricted':
    mention = user.user.mention
    text = f"""
**Unmute User:** {mention}
**By: {m.from_user.mention if m.from_user else 'Anon'}
"""
    await m.chat.unban_member(user.user.id)
    return await m.reply_text(text) 
  elif user.status.value != 'restricted':
    return await m.reply_text("User tidak ada dalam daftar muted group ini!")

