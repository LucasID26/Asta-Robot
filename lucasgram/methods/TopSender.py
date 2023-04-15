import itertools
import json

async def GetTopSender(self, chat_id, limit=10):
  try:
    senders = {}
    async for message in self.search_messages(chat_id=chat_id):
      user_id = message.from_user.id
      senders[user_id] = senders.get(user_id, 0) + 1

    sorted_senders = sorted(senders.items(), key=lambda x: x[1], reverse=True)[:limit]

    top_senders = []
    for sender_id, message_count in sorted_senders:
      user = await self.get_users(sender_id)
      user_dict = {
          "id": user.id,
          "first_name": user.first_name,
          "last_name": user.last_name,
          "username": user.username,
          "message_count": message_count
      }
      top_senders.append({
          "user": user_dict
      })

    result_dict = {
        "top_senders": top_senders
    }

    return json.dumps(result_dict, indent=2)

  except Exception as e:
    print(f"Error getting top senders: {e}")
