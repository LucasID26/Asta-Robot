

async def get_top_sender(self, chat_id):
  try:
    members_count = await self.get_chat_members_count(chat_id)
    all_members = await self.get_chat_members(chat_id, limit=members_count)

    senders = {}
    for member in all_members:
      user_id = member.user.id
      messages = await self.search_messages(chat_id=chat_id, from_user=user_id)
      senders[user_id] = messages.total

    top_sender_id = max(senders, key=senders.get)
    top_sender = await self.get_users(top_sender_id)

    return top_sender.first_name, senders[top_sender_id]
  except Exception as e:
    print(f"Error getting top sender: {e}")
