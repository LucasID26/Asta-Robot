import json
import heapq
from config import bot


async def GetTopAdmins(chat_id, n=3): 
  admins = {}
  async for member in bot.get_chat_members(chat_id, filter="administrators"):
    admins[member.user.id] = member.user.username
        
  messages = await bot.get_messages(chat_id)
  message_count = {}
  for message in messages:
    if message.from_user.id in admins:
      message_count[message.from_user.username] = message_count.get(message.from_user.username, 0) + 1
                
  top_admins = sorted(message_count.items(), key=lambda x: x[1], reverse=True)[:n]
        
  result = {}
  for i, (admin, count) in enumerate(top_admins):
    result[f"admin_{i+1}"] = {"username": admin, "message_count": count}
        
  return json.dumps(result)



