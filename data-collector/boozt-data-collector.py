import requests
import re
from bs4 import BeautifulSoup
import uuid
import multiprocessing
import os

DATA_PATH = "./data-collector/data"


if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)

def get_page(index: int):
    URL = "https://www.boozt.com/dk/da/toej-til-maend/sko?grid=small&limit=120&page="
    response = requests.get(URL + str(index))
    soup = BeautifulSoup(response.text, 'html.parser')

    container = soup.find("div", "product-listing__wrapper-column product-listing__wrapper-column--main")

    imgs = container.find_all("img")
    urls = [img["src"] for img in imgs]

    for url in urls:
        download_image(url)

def download_image(url: str):
    img = requests.get(url)
    filetype = img.headers['content-type'].split("/")[-1]
    id = uuid.uuid4()
    with open(f"{DATA_PATH}/{id}.{filetype}", "wb") as file:
        file.write(img.content)

with multiprocessing.Pool(16) as pool:
    result = pool.map(get_page, range(1, 25))