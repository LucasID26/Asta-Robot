from config import *
from pyrogram import filters,enums
import os
import sys 
import subprocess
import asyncio 
import traceback 
import io
from pykeyboard import InlineKeyboard,InlineButton


@bot.on_message(filters.command("sh") & filters.user(own))
@bot.on_edited_message(filters.command("sh",prefix) & filters.user(own))
async def shell(client, m):
    cmd = m.text.split(" ",1)
    if len(m.command) == 1:
        return await m.reply(text="No command to execute was given.",quote=True)
    msg = await m. reply(text="__Processing...__",quote=True)
    shell = (await shell_exec(cmd[1]))[0]
    button = InlineKeyboard()
    button.add(InlineButton("DELETE",callback_data=f"delete#{m.from_user.id}"))
    if len(shell) > 3000:
        with open("shell_asta.txt", "w") as file:
            file.write(shell)
        with open("shell_asta.txt", "rb") as doc:
          if m.chat.is_forum == True:
            await bot.send_document(m.chat.id,
                document=doc,
                file_name=doc.name,message_thread_id=m.topics.id,reply_markup=button)
          else:
            await bot.send_document(m.chat.id,
                document=doc,
                file_name=doc.name,reply_markup=button)
          await msg.delete()
          try:
            os.remove("shell_asta.txt")
          except:
            pass
    elif len(shell) != 0:
        await msg.edit(text=shell,reply_markup=button)
    else:
        await msg.edit("No Reply")

@bot.on_message(filters.command("run",prefix) & filters.user(own))
@bot.on_edited_message(filters.command("run",prefix) & filters.user(own))
async def evaluation_cmd_t(client, m):
  cmd = m.text.split(" ",1)
  if len(m.command) == 1:
    return await m.reply_text(text="__No evaluate message!__")
  status = await m.reply_text(text="__Processing eval pyrogram...__")

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
  button = InlineKeyboard()
  button.add(InlineButton("DELETE",callback_data=f"delete#{m.from_user.id}"))
  if len(final_output) > 4096:
    with open("AstaEval.txt", "w+", encoding="utf8") as out_file:
      out_file.write(final_output)
    await m.reply_document(document="AstaEval.txt",
                           caption=f"<code>{cmd[1][: 4096 // 4 - 1]}</code>",
                           disable_notification=True,reply_markup=button)
    await status.delete()
    os.remove("AstaEval.txt")
  else:
    await status.edit_text(text=final_output,reply_markup=button)


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

@bot.on_callback_query(filters.create(lambda _, __, query: "delete#" in query.data))
async def eval_call(client,call):
  try:
    if call.from_user.id != int(call.data.split("#")[1]):
      return await call.answer("Bukan buat lu..!",True) 
    return await call.message.delete()
  except:
    return await call.answer("Callback timeout")

