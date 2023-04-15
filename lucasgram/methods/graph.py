from telegraph import Telegraph


async def CreateTextGraph(title: str, content: list):
  telegraph = Telegraph()
  telegraph.create_account(short_name='my_account')
  page = telegraph.create_page(title=title, html_content=''.join(content))
  return page['url']
