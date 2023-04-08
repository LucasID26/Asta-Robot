from config import bot,asisstant
from flask import Flask
from threading import Thread 
from pyrogram import idle
import random
import Asta

app = Flask(__name__)

@app.route('/')
def flask_run():
  return "BOT RUN"


def run_flask():
  app.run(
    host="0.0.0.0",
    port=8080)

def run_thread():
  Thread(target=run_flask).start()

def run_all():
  run_thread()
  #bot.run()
  bot.start()
  asisstant.start()
  idle()
  bot.stop()
  asisstant.stop()

run_all()