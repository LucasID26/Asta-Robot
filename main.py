from flask import Flask
from threading import Thread 
from config import bot,prefix,own,asisstant 
from pyrogram import filters
import subprocess
import sys
import os
import re

app = Flask(__name__)

@app.route('/')
def flask_run():
  return "BOT RUN"

@bot.on_message(filters.command('restart'))
async def restart_plugins(client,m):
  msg = await m.reply_text("__Restarting BOT__. . .")
  for file in os.listdir('Asta/plugins'):
    with open('Asta/plugins/__init__.py', 'r') as f:
      init_lines = f.readlines()
    if file.endswith('.py') and not file.startswith('__'):
      module_name = file[:-3]
      import_line = f"from . import {module_name}"
      if not re.search(fr"\b{re.escape(import_line)}\b", str(init_lines)):
        with open('Asta/plugins/__init__.py', 'a') as f:
          f.write("\n"+import_line)
  import Asta    
  await msg.edit("__**Restarting berhasil✅**__")


def install_requirements():
  requirements_file = "requirements.txt"
  if os.path.exists(requirements_file):
    print("Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
    print("Requirements installed.")
    subprocess.call("clear")
  else:
    print("Requirements file not found.")


def run_flask():
  app.run(
    host="0.0.0.0",
    port=8080)

def run_thread():
  Thread(target=run_flask).start()

def run_all():
  install_requirements()
  run_thread()

  import Asta
  
  bot.run()
  bot.start()
  asisstant.start()
  idle()
  bot.stop()
  asisstant.stop()

run_all()
