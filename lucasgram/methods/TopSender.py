import itertools
import json

async def GetTopSender(self, chat_id):
  try:
    #members_count = await self.get_chat_members_count(chat_id)
    #all_members = await self.get_chat_members(chat_id, limit=members_count)

    senders = {}
    async for message in self.search_messages(chat_id=chat_id):
      user_id = message.from_user.id
      senders[user_id] = senders.get(user_id, 0) + 1

    top_sender_id = max(senders, key=senders.get)
    top_sender = await self.get_users(top_sender_id)

    result_dict = {
        "top_sender": {
            "first_name": top_sender.first_name,
            "message_count": senders[top_sender_id]
        },
        "all_senders": {
            sender_id: {
                "user": await self.get_users(sender_id),
                "message_count": message_count
            } for sender_id, message_count in senders.items()
        }
    }

    return json.dumps(result_dict, indent=4)

  except Exception as e:
    print(f"Error getting top sender: {e}")

