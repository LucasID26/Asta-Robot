from pyrogram import filters 
from config import bot,prefix
import time 
import asyncio 
import json
from pyrogram import enums
import re

from Asta.decorators.cek_admin import bot_admin
from Asta.decorators.pv_or_gc import no_private
from Asta.decorators.info_cmd import info_cmd
from Asta.decorators.error import error

a = open("JSON/afk.json")
afk_ = json.load(a)


TIME_DURATION_UNITS = ( ('minggu', 60 * 60 * 24 * 7), ('hari', 60 * 60 * 24), ('jam', 60 * 60), ('menit', 60), ('detik', 1))
def _human_time_duration(seconds):
  if seconds == 0:
    return 'Baru aja off'
  parts = []
  for unit, div in TIME_DURATION_UNITS:
    amount, seconds = divmod(int(seconds), div)
    if amount > 0:
      parts.append('{} {}{}' .format(amount, unit, "" if amount == 1 else ""))
  return ', '.join(parts) 


@bot.on_message(filters.command("afk",prefix))
@info_cmd
@no_private
@bot_admin
@error
async def bot_afk(client,m):
  userid = str(m.from_user.id)
  if userid in afk_:
    if len(m.command) == 1:
      reason = "Yo ndak tau orang gada ngasi alasan"
      afk_[userid]["reason"] = reason
    elif len(m.command) >= 2:
      start_time = time.time()
      reason = m.text.split(None, 1)[1]
      afk_[userid]["reason"] = reason
    with open("JSON/afk.json","w") as out:
      json.dump(afk_,out, indent=2) 
    await m.reply(f"❏ <b>Update AFK!</b>\n└ <b>Karena:</b> <code>{reason}</code>")
  elif not userid in afk_:
    start_time = time.time() 
    if len(m.command) == 1:
      reason = "Yo ndak tau orang gada ngasi alasan"
      afk_[userid] = {"start_time": start_time,
                         "reason": reason}
    elif len(m.command) >= 2:
      start_time = time.time()
      reason = m.text.split(None, 1)[1]
      afk_[userid] = {"start_time": start_time,
                         "reason": reason}
    with open("JSON/afk.json","w") as out:
      json.dump(afk_,out, indent=2)
    await m.reply(f"❏ <b>Telah AFK!</b>\n└ <b>Karena:</b> <code>{reason}</code>")

@bot.on_message(filters.group & ~filters.private)
async def afk_respon(client,m):
  userid = str(m.from_user.id)
  if userid in afk_:
    reason = afk_[userid]["reason"]
    end_time = time.time()
    start_time = afk_[userid]["start_time"]
    afk_time = end_time - start_time
    uptime = _human_time_duration(int(afk_time))
    await m.reply(f"❏ {m.from_user.mention}\n⌦ <b>STATUS:</b> <code>ONLINE!</code>\n⌦ <b>Selama:</b> <code>{uptime}</code>")
    del afk_[str(m.from_user.id)]
    with open("JSON/afk.json","w") as out:
      json.dump(afk_,out, indent=2)
  if m.reply_to_message:
    user = m.reply_to_message.from_user
    if str(user.id) in afk_: 
      reason = afk_[str(user.id)]["reason"]
      end_time = time.time()
      start_time = afk_[str(user.id)]["start_time"]
      afk_time = end_time - start_time
      uptime = _human_time_duration(int(afk_time))
      await m.reply(f"❏ {user.mention}\n⌦ <b>STATUS:</b> <code>AFK!</code>\n⌦ <b>Karena:</b> <code>{reason}</code>\n⌦ <b>Selama:</b> <code>{uptime}</code>")
    else:
      pass
  elif m.entities:
    entity = m.entities
    j = 0
    for _ in range(len(entity)):
      if (entity[j].type) == enums.MessageEntityType.MENTION:
        found = re.findall("@([_0-9a-zA-Z]+)", m.text)
        get_user = found[j]
        userid = await bot.get_users(get_user) 
        user_id = str(userid.id)
        mention = (await bot.get_users(user_id)).mention
        if user_id in afk_: 
          reason = afk_[user_id]["reason"]
          end_time = time.time()
          start_time = afk_[user_id]["start_time"]
          afk_time = end_time - start_time
          uptime = _human_time_duration(int(afk_time))
          await m.reply(f"❏ {mention}\n⌦ <b>STATUS:</b> <code>AFK!</code>\n⌦ <b>Karena:</b> <code>{reason}</code>\n⌦ <b>Selama:</b> <code>{uptime}</code>")
        else:
          pass
      elif (entity[j].type) == enums.MessageEntityType.TEXT_MENTION:
        userid = entity[j].user 
        user_id = str(userid.id)
        mention = (await bot.get_users(user_id)).mention
        if user_id in afk_: 
          reason = afk_[user_id]["reason"]
          end_time = time.time()
          start_time = afk_[user_id]["start_time"]
          afk_time = end_time - start_time
          uptime = _human_time_duration(int(afk_time))
          await m.reply(f"❏ {mention}\n⌦ <b>STATUS:</b> <code>AFK!</code>\n⌦ <b>Karena:</b> <code>{reason}</code>\n⌦ <b>Selama:</b> <code>{uptime}</code>")
        else:
          pass
                
  
    