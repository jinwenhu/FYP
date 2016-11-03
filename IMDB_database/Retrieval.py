import requests
import random
from bs4 import BeautifulSoup
import urllib
import os

def get_content(url , data = None):
    header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
    }
    #timeout = random.choice(range(80, 180))
    rep = requests.get(url,headers = header)
    rep.encoding = 'utf-8'
    return rep.text

def download(url, title, grene):
    print title
    #create folder if necessary
    image_folder_path = "movie_image/" + grene
    description_folder_path = "movie_description/" + grene
    try:
        os.makedirs(image_folder_path)
    except OSError:
        if not os.path.isdir(image_folder_path):
            raise
    try:
        os.makedirs(description_folder_path)
    except OSError:
        if not os.path.isdir(description_folder_path):
            raise

    #get the html content, image and description from IMDB server
    html = get_content(url)
    soup = BeautifulSoup(html, 'html.parser')
    url_image = soup.find("meta", {"property":"og:image"})['content']
    description = soup.find("meta", {"name": "description"})['content']

    #retrieve image content
    urllib.urlretrieve(url_image, image_folder_path + "/" + title + ".jpg")

    with open(description_folder_path + "/" + title + ".txt", "wb") as output1:
        description = description.encode('ascii','ignore')
        output1.write(description)
    output1.close()

if __name__ == '__main__':
    url = 'http://www.imdb.com/title/tt0499549/?ref_=fn_tt_tt_1'
    download(url, "test", "test")