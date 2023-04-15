import itertools

async def GetTopSender(self, chat_id):
  try:
    senders = {}
    async for message in self.search_messages(chat_id=chat_id):
      user_id = message.from_user.id
      senders[user_id] = senders.get(user_id, 0) + 1

    sorted_senders = sorted(senders.items(), key=lambda x: x[1], reverse=True)
    top_senders = itertools.islice(sorted_senders, 10)

    top_senders_info = {await self.get_users(sender[0]): sender[1] for sender in top_senders}

    return top_senders_info

  except Exception as e:
    print(f"Error getting top senders: {e}")
