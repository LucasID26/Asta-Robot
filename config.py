import os 
from pyrogram import Client 
import pymongo 
import pyromod.listen
#from motor.motor_asyncio import AsyncIOMotorClient as MongoClient



ID = os.environ['API_ID']
HASH = os.environ['API_HASH']
TOKEN = os.environ['BOT_TOKEN']
ASISSTANT_STR = os.environ['ASISSTANT_STRING']
DATABASE = os.environ["DB"]
DB = pymongo.MongoClient(str(DATABASE),connectTimeoutMS=5000)

dbname = DB["Asta-Robot"]


prefix = ['/','!','.','*'] 
own = [1928677026]
bot = Client('Asta-Robot',
             api_id=ID,
             api_hash=HASH,
             bot_token=TOKEN,
             in_memory=True
            )
asisstant = Client('Asta-Asisstant',
             api_id=ID,
             api_hash=HASH,
             session_string=ASISSTANT_STR,
             in_memory=True
            )
