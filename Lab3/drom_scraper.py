import requests as rq
import os
from bs4 import BeautifulSoup as bs
import base64
import zipfile
import uuid
from datetime import datetime

def GetWebPageByLink(url: str, folder_name = datetime.now().strftime("%Y-%m-%d - %H-%M")):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    response = rq.get(url=url)
    if not response.ok:
        return None
    soup = bs(response.text, features="html.parser")
    with zipfile.ZipFile('images.zip', 'w') as zpf:
        for link in soup.find_all('img'):
            img_link = link.get('src')
            if(img_link[-3::] == "jpg"):
                img = rq.get(img_link)
                rng_name = str(uuid.uuid4())
                if img.ok:
                    with open(f"./{folder_name}/{rng_name}.png", "wb+") as fh:
                        fh.write(base64.decodebytes(base64.b64encode(img.content)))
                zpf.write(f"./{folder_name}/{rng_name}.png")

def main():
    GetWebPageByLink("https://auto.drom.ru/toyota/all/?maxprice=350000")

if __name__ == "__main__":
    main()
