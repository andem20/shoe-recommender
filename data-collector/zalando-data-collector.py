import requests
from bs4 import BeautifulSoup
import multiprocessing
import os
import hashlib
from PIL import Image
import io

DATA_PATH = "./data-collector/data/zalando"

if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

def get_page(index: int):
    URL = "https://www.zalando.dk/herresko/?p="
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    response = requests.get(URL + str(index), headers=headers, timeout=5)
    soup = BeautifulSoup(response.text, 'html.parser')

    container = soup.find("div", {"data-zalon-partner-target": "true"})

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
    content = io.BytesIO(img.content)
    id = calc_md5(img.content)
    image = Image.open(content).convert('RGB')
    image.save(f"{DATA_PATH}/{id}.jpg", "jpeg")

with multiprocessing.Pool(16) as pool:
    result = pool.map(get_page, range(1, 223))