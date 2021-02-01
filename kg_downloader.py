from bs4 import BeautifulSoup
import requests
import os

# Global Constants
OUTPUT_PATH = "./output/"

HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-HEADERS': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}


def main():

    # Grab kg-url input from user

    # acc_url = input("Enter K歌 Account URL: ")
    acc_url = "https://node.kg.qq.com/personal?uid=6b9c9c83202d308b35"
    req = requests.get(acc_url, HEADERS)

    provision(BeautifulSoup(req.content, 'html.parser'))


def provision(soup):
    acc_name = soup.find("span", {"class": "my_show__name"}).next

    # Remove account files if exists and re-create
    acc_file_path = OUTPUT_PATH + acc_name

    if os.path.exists(acc_file_path):
        os.rmdir(acc_file_path)
    os.mkdir(acc_file_path)

    album_divs = soup.find_all("div", {"class": "mod_playlist__cd"})
    print(album_divs)

    # for link in album_links:
    #     song_extract(link)


def song_extract(link):
    req= requests.get(link, HEADERS)
    BeautifulSoup(req.content, 'html.parser')


if __name__ == "__main__":
    main()
