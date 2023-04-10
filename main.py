from flask import Flask
from threading import Thread 
from pyrogram import idle
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
  else:
    print("Requirements file not found.")

from config import bot,asisstant
import Asta


def run_flask():
  app.run(
    host="0.0.0.0",
    port=8080)

def run_thread():
  Thread(target=run_flask).start()

def run_all():
  install_requirements()
  run_thread()
  bot.run()
  bot.start()
  asisstant.start()
  idle()
  bot.stop()
  asisstant.stop()

run_all()
