import itertools
import json

async def GetTopSender(self, chat_id):
  try:
    senders = {}
    async for message in self.search_messages(chat_id=chat_id):
      user_id = message.from_user.id
      senders[user_id] = senders.get(user_id, 0) + 1

    top_sender_id = max(senders, key=senders.get)
    top_sender = await self.get_users(top_sender_id)

    all_senders = []
    for sender_id, message_count in senders.items():
      user = await self.get_users(sender_id)
      if len(all_senders) >= 10:
        break
      user_dict = {
          "id": user.id,
          "first_name": user.first_name,
          "last_name": user.last_name,
          "username": user.username,
          "message_count": message_count
      }
      all_senders.append({
          "user": user_dict
      })

    result_dict = {
        "top_sender": {
            "user": {
                "id": top_sender.id,
                "first_name": top_sender.first_name,
                "last_name": top_sender.last_name,
                "username": top_sender.username,
                "message_count": senders[top_sender_id]
            }
        },
        "all_senders": all_senders
    }

    return json.dumps(result_dict, indent=4)

  except Exception as e:
    print(f"Error getting top sender: {e}")
