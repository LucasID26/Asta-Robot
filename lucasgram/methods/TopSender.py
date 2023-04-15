import itertools

async def GetTopSender(self, chat_id, max_senders=10):
  try:
    senders = {}
    async for message in self.search_messages(chat_id=chat_id):
      user_id = message.from_user.id
      senders[user_id] = senders.get(user_id, 0) + 1

    top_senders = dict(sorted(senders.items(), key=lambda x: x[1], reverse=True)[:max_senders])

    top_senders_info = {await self.get_users(sender_id): senders[sender_id] for sender_id in top_senders.keys()}

    return top_senders_info

  except Exception as e:
    print(f"Error getting top senders: {e}")

