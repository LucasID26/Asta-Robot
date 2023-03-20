from requests import get 
from bs4 import BeautifulSoup as BF 

def get_donghua(m,query):
  results_all = {}
  results = {}
  msgid = str(m.id)
  #res = get(f"https://kazefuri.net/?s={query}")
  res = get(f"https://donghua.web.id/?s={query}")
  bf = BF(res.content,'html.parser')
  for sc in bf.findAll(class_="bsx"):
    judul = sc.find("a").get("title")
    link = sc.find("a").get("href")
    img = sc.find(class_="ts-post-image wp-post-image attachment-medium_large size-medium_large").get("src") 
    
    req = get(link).content
    soup = BF(req,'html.parser')  
    desc = soup.find(class_="mindesc").text
    for info_content in soup.findAll(class_="info-content"):
      content = info_content.findAll("span")

    info = ""
    for detail in content:
      #detail = detail
      info += f" • {detail}\n"
    result = {'judul': judul, 
              'link': link,
              'img': img,
              'desc': desc, 
              'info': info
               }
    results[msgid] = result
    if not msgid in results_all:
      results_all[msgid]  = [result]
    elif msgid in results_all:
      results_all[msgid].append(result)    

  return results_all

def get_kazefuri(m,query):
  results_all = {}
  results = {}
  msgid = str(m.id)
  res = get(f"https://kazefuri.net/?s={query}")
  #res = get(f"https://donghua.web.id/?s={query}")
  bf = BF(res.content,'html.parser')
  for sc in bf.findAll(class_="bsx"):
    judul = sc.find("a").get("title")
    link = sc.find("a").get("href")
    img = sc.find(class_="ts-post-image wp-post-image attachment-medium_large size-medium_large").get("src") 
    
    req = get(link).content
    soup = BF(req,'html.parser')  
    desc = soup.find(class_="mindesc").text
    for info_content in soup.findAll(class_="info-content"):
      content = info_content.findAll("span")

    info = ""
    for detail in content:
      #detail = detail
      info += f" • {detail}\n"
    result = {'judul': judul, 
              'link': link,
              'img': img,
              'desc': desc, 
              'info': info
               }
    results[msgid] = result
    if not msgid in results_all:
      results_all[msgid]  = [result]
    elif msgid in results_all:
      results_all[msgid].append(result)    

  return results_all

                                     
def eps(url):
  results = []
  result = []
  res = get(url) 
  bf = BF(res.content,'html.parser')
  scp = bf.find(class_="eplister")
  for sc in scp.findAll("li"):
    link = sc.find("a").get("href")  
    results.append(link)
  return results

