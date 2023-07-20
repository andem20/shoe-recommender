import requests
import re
from bs4 import BeautifulSoup
import uuid
import multiprocessing
import os
import hashlib
from PIL import Image
import io

DATA_PATH = "./data-collector/data/boozt"

if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

def get_page(index: int):
    URL = "https://www.boozt.com/dk/da/toej-til-maend/sko?grid=small&limit=120&page="
    response = requests.get(URL + str(index))
    soup = BeautifulSoup(response.text, 'html.parser')

    container = soup.find("div", "product-listing__wrapper-column product-listing__wrapper-column--main")

    if container is None:
        return

    imgs = container.find_all("img")
    urls = [img["src"] for img in imgs]

    for url in urls:
        download_image(url)

def calc_md5(img):
    return hashlib.md5(img).hexdigest()

def download_image(url: str):
    img = requests.get(url)
    # filetype = img.headers['content-type'].split("/")[-1]
    content = io.BytesIO(img.content)
    id = calc_md5(img.content)
    image = Image.open(content).convert('RGB')
    image.save(f"{DATA_PATH}/{id}.jpg", "jpeg")
    # with open(f"{DATA_PATH}/{id}.{filetype}", "wb") as file:
    #     file.write(img.content)

with multiprocessing.Pool(16) as pool:
    result = pool.map(get_page, range(1, 25))