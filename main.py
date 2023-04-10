from flask import Flask
from threading import Thread 
import subprocess
import sys
import os

app = Flask(__name__)

@app.route('/')
def flask_run():
  return "BOT RUN"


def install_requirements():
  requirements_file = "requirements.txt"
  if os.path.exists(requirements_file):
    print("Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
    print("Requirements installed.")
    subprocess.check_call([sys.executable, "clear"])
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
  
  from pyrogram import idle
  from config import bot,asisstant
  import Asta
  
  bot.run()
  bot.start()
  asisstant.start()
  idle()
  bot.stop()
  asisstant.stop()

run_all()
