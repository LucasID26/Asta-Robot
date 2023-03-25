from requests import get
from bs4 import BeautifulSoup as BF

def translate(kode,query):
  url = f"https://translate.glosbe.com/id-{kode}/{query}"
  res = get(url)
  bf = BF(res.content,'html.parser')
  hasil = bf.find("div",class_="w-full h-full bg-gray-100 h-full border p-2 min-h-25vh sm:min-h-50vh whitespace-pre-wrap break-words")
  if len(hasil) == 0:
    return "Ahh Kode bahasa itu tidak ada bre"
  else:
    return hasil
