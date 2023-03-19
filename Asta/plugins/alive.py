from pyrogram import filters 
fron config import bot 
import time 



@bot.on_message(filters.command("ping",prefix))
#@info_cmd
async def ping(client, m):
  uptime = duration((datetime.utcnow() - starttime).total_seconds())
  start = time.time() 
  msg = await m.reply_text("**0% ▒▒▒▒▒▒▒▒▒▒**")
  end = time.time()
  durasi = round(end - start,3)
  await msg.edit("**20% ██▒▒▒▒▒▒▒▒**")
  await msg.edit("**40% ████▒▒▒▒▒▒**")
  await msg.edit("**60% ██████▒▒▒▒**")
  await msg.edit("**80% ████████▒▒**")
  await msg.edit("**100% ██████████**")
  owner = (await bot.get_users(own[0])).mention
  await msg.edit(f"""
❏ **PONG!!🏓**
├• **Pinger** - `{durasi} detik`
├• **Uptime -** `{uptime}`
└• **Owner :** {owner} <a href='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTz5q_KcP8RQbDQPciRoBSlwKMyBHAKMNN-pg&amp;usqp=CAU'>⁠</a>""")
