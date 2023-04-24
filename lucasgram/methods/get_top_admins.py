import json
import heapq

async def GetTopAdmins(self, chat_id, n=3):
  members = self.get_chat_members(chat_id)
  message_count = {}
  for member in members:
    if member.status == 'administrator':
      message_count[member.user.username] = 0
  count = self.get_chat_members_count(chat_id)
  offset = 0
  limit = 100
  while offset < count:
    members = self.get_chat_members(chat_id, offset=offset, limit=limit)
    for member in members:
      if member.user.username in message_count:
        message_count[member.user.username] += member.user.messages_count
    offset += limit
  top_admins = heapq.nlargest(n, message_count.items(), key=lambda x: x[1])
  result = {}
  for i, (admin, count) in enumerate(top_admins):
    result[f"admin_{i+1}"] = {"username": admin, "message_count": count}
  return json.dumps(result)



