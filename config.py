import os 
from pyrogram import Client 
import pymongo 
import pyromod.listen
#from motor.motor_asyncio import AsyncIOMotorClient as MongoClient



ID = os.environ['API_ID']
HASH = os.environ['API_HASH']
TOKEN = os.environ['BOT_TOKEN']
ASUPAN_TOKEN = os.environ['ASUPAN_TOKEN']
ASISSTANT_STR = os.environ['ASISSTANT_STRING']
DATABASE = os.environ["DB"] 

CH_DB = int(os.environ['CH_DB'])
CH_SHARE = int(os.environ['CH_SHARE'])
SUBS_ID = os.environ['SUBS_ID'] 


DB = pymongo.MongoClient(str(DATABASE),connectTimeoutMS=5000)

dbname = DB["Asta-Robot"]


prefix = ['/','!','*'] 
own = [1928677026,5039288972]
bot = Client('Asta_Robot',
             api_id=ID,
             api_hash=HASH,
             bot_token=TOKEN,
             in_memory=True
            )
botasupan = Client('ASUPAN',
             api_id=ID,
             api_hash=HASH,
             bot_token=ASUPAN_TOKEN,
             in_memory=True
            )

asisstant = Client('AstaAsisstant',
             api_id=ID,
             api_hash=HASH,
             session_string=ASISSTANT_STR,
             in_memory=True
            )