from flask import Flask
from threading import Thread
from config import bot, asisstant
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
  app.run(host="0.0.0.0", port=random.randint(5000, 9999))


def run_thread():
  Thread(target=run_flask).start()


async def run_all():
  from Asta.__main__ import restarting, restart
  restart()
  importlib.import_module("Asta")
  await bot.start()
  await asisstant.start()
  run_thread()
  await restarting()
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
    from Asta.func.sendGmail import sendgmail
    sendgmail("LAPORAN KONSOL",err)
  finally:
    loop.stop()
    print("STOPED")
