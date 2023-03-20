import config
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
  app.run(host="0.0.0.0",port=random.randint(2000,9000))

def run_thread():
  Thread(target=run_bot).start()

def run_all():
  run_thread()
  bot.start()
  idle()
  bot.stop()

run_all()
