from flask import Flask
from threading import Thread
from config import bot,asisstant 
import importlib
from pyrogram import idle
import random
import os
import asyncio 
import pickle
import traceback

app = Flask(__name__)

@app.route('/')
def flask_run():
  return "ASTA-ROBOT RUN"


def run_flask():
  app.run(
    host="0.0.0.0",
    port=random.randint(5000, 9999))

def run_thread():
  Thread(target=run_flask).start()


async def run_all():
  from Asta.__init__ import install_requirements,git
  git_pull = git()
  importlib.import_module("Asta")
  install_requirements()
  
  await bot.start()
  await asisstant.start()
  run_thread()
  if os.path.exists("restart.pickle"):
    with open('restart.pickle', 'rb') as status:
      chat_id, message_id = pickle.load(status)
      os.remove("restart.pickle")
      await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"{git_pull}\n\n__**Restarting berhasil✅**__")
  await idle()
  await bot.stop()
  await asisstant.stop()

loop = asyncio.get_event_loop()
if __name__ == "__main__":
  try:
    loop.run_until_complete(run_all())
  except KeyboardInterrupt:
    pass 
  except Exception:
    err = traceback.format_exc()
    print(err)
  finally:
    loop.stop()
    print("STOPED")
