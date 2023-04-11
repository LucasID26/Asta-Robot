from . import plugins

from config import bot,prefix,own 
from pyrogram import filters
import subprocess
import sys
import os
import re 
import pickle

@bot.on_message(filters.command('restart',prefix) & filters.user(own[0]))
async def restart_plugins(client,m):
  msg = await m.reply_text("__Restarting BOT__. . .")
  with open("restart.pickle", "wb") as status:
    pickle.dump([m.chat.id, msg.id], status)
  for file in os.listdir('Asta/plugins'):
    with open('Asta/plugins/__init__.py', 'r') as f:
      init_lines = f.readlines()
    if file.endswith('.py') and not file.startswith('__'):
      module_name = file[:-3]
      import_line = f"from . import {module_name}"
      if not re.search(fr"\b{re.escape(import_line)}\b", str(init_lines)):
        with open('Asta/plugins/__init__.py', 'a') as f:
          f.write("\n"+import_line)
  #await msg.edit("__**Restarting berhasil✅**__")
  restart_program() 

def restart_program():
  #os.kill(os.getpid(), signal.SIGTERM)
  os.execvp(sys.executable, [sys.executable, "main.py"]) 

def install_requirements():
  requirements_file = "requirements.txt"
  if os.path.exists(requirements_file):
    print("Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
    print("Requirements installed.")
    subprocess.call("clear")
  else:
    print("Requirements file not found.")