from config import *
from pyrogram import filters,enums
import os
import sys 
import subprocess
import asyncio 
import traceback 
import io



@bot.on_message(filters.command("sh") & filters.user(own))
@bot.on_edited_message(filters.command("sh",prefix) & filters.user(own))
async def shell(client, m):
    cmd = m.text.split(" ",1)
    if len(m.command) == 1:
        return await m.reply(text="No command to execute was given.",quote=True)
    msg = await m. reply(text="__Processing...__",quote=True)
    shell = (await shell_exec(cmd[1]))[0]
    if len(shell) > 3000:
        with open("shell_asta.txt", "w") as file:
            file.write(shell)
        with open("shell_asta.txt", "rb") as doc:
          if m.chat.is_forum == True:
            await bot.send_document(m.chat.id,
                document=doc,
                file_name=doc.name,message_thread_id=m.topics.id)
          else:
            await bot.send_document(m.chat.id,
                document=doc,
                file_name=doc.name)
          await msg.delete()
          try:
            os.remove("shell_asta.txt")
          except:
            pass
    elif len(shell) != 0:
        await msg.edit(text=shell)
    else:
        await msg.edit("No Reply")

@bot.on_message(filters.command("run",prefix) & filters.user(own))
@bot.on_edited_message(filters.command("run",prefix) & filters.user(own))
async def evaluation_cmd_t(client, m):
  cmd = m.text.split(" ",1)
  if len(m.command) == 1:
    return await m.reply(text="__No evaluate message!__",quote=True)
  status_message = await m.reply(text="__Processing eval pyrogram...__",quote=True)

  old_stderr = sys.stderr
  old_stdout = sys.stdout
  redirected_output = sys.stdout = io.StringIO()
  redirected_error = sys.stderr = io.StringIO()
  stdout, stderr, exc = None, None, None

  try:
    await aexec(cmd[1], client, m)
  except Exception as e:
   # exc = traceback.format_exc(e)
    exc = str(e)
  stdout = redirected_output.getvalue()
  stderr = redirected_error.getvalue()
  sys.stdout = old_stdout
  sys.stderr = old_stderr

  evaluation = ""
  if exc:
    evaluation = exc
  elif stderr:
    evaluation = stderr
  elif stdout:
    evaluation = stdout
  else:
    evaluation = "Success"

  final_output = f"**EVAL**:\n`{cmd[1]}`\n\n**OUTPUT**:\n`{evaluation.strip()}`\n"

  if len(final_output) > 4096:
    with open("AstaEval.txt", "w+", encoding="utf8") as out_file:
      out_file.write(final_output)
    await m.reply_document(document="LucasEval.txt",
                           caption=f"<code>{cmd[1][: 4096 // 4 - 1]}</code>",
                           disable_notification=True)
    await status_message.delete()
    os.remove("AstaEval.txt")
  else:
    await status_message.edit(text=final_output)


async def aexec(code, c, m):
  exec("async def __aexec(c, m): " + "\n p = print" +
       "\n replied = m.reply_to_message" + "".join(f"\n {l_}"
                                                   for l_ in code.split("\n")))
  return await locals()["__aexec"](c, m)

async def shell_exec(code, treat=True):
    process = await asyncio.create_subprocess_shell(code, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)

    stdout = (await process.communicate())[0]
    if treat:
        stdout = stdout.decode().strip()
    return stdout, process
