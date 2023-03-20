import requests 
from bs4 import BeautifulSoup


def google(keywords,limit = 20):
    query  = keywords.replace(' ','+')
    start = 0
    hasil = []
    num = min(limit + 1,100)
    headers = {
        'User-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    
    params = {
      'q': query, 
      'gl': 'id', 
      'hl': 'id',
      'num' : num
    }
    
    html = requests.get("https://www.google.com/search", headers=headers, params=params,timeout=10)
    soup = BeautifulSoup(html.text, 'html.parser')
    element = soup.select(".tF2Cxc")
    if not element:
        return hasil
    for result in element:
        title = result.select_one(".DKV0Md").text
        link = result.select_one(".yuRUbf a")["href"]
        try:
            snippet = result.select_one("#rso .lyLwlc").text
        except:
            snippet = "KOSONG"
        result_s = {'judul': title,
                           'link': link,
                           'deskripsi': snippet}
        hasil.append(result_s)
    if len(hasil) >= limit or abs(limit - len(hasil)) <= 10:
        return hasil
    start += num 


def Gimages(query):
    google_images = []
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"
}
    params = {
    "q": query,
    "tbm": "isch",
    "hl": "id",
    "gl": "id",
    "ijn": "0"
}

    html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
    soup = BeautifulSoup(html.text, "lxml")
    if html.status_code == 400:
        return google_images

    all_script_tags = soup.select("script")
    
    matched_images_data = "".join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags)))

    matched_images_data_fix = json.dumps(matched_images_data)
    matched_images_data_json = json.loads(matched_images_data_fix)

    matched_google_image_data = re.findall(r'\"b-GRID_STATE0\"(.*)sideChannel:\s?{}}', matched_images_data_json)

    matched_google_images_thumbnails = ", ".join(
        re.findall(r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]',
                   str(matched_google_image_data))).split(", ")

    thumbnails = [
        bytes(bytes(thumbnail, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for thumbnail in matched_google_images_thumbnails
    ]
    removed_matched_google_images_thumbnails = re.sub(
        r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', "", str(matched_google_image_data))

    matched_google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]", removed_matched_google_images_thumbnails)

    full_res_images = [
        bytes(bytes(img, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for img in matched_google_full_resolution_images
    ]

    for index, (metadata, thumbnail, original) in enumerate(zip(soup.select('.isv-r.PNCib.MSM1fd.BUooTd'), thumbnails, full_res_images), start=1):
        google_images.append({
            "title": metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")["title"],
            "link": metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")["href"],
            "source": metadata.select_one(".fxgdke").text,
            "thumbnail": thumbnail,
            "original": original
        })
        if index == 20:
            break


    return google_images
