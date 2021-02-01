from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import os
import shutil

# Global Constants
OUTPUT_PATH = "./output/"

HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-HEADERS': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

# Webdriver setup
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(
    "/usr/lib/chromium-browser/chromedriver", options=options)


def main():
    """Initialization of program"""

    # Grab kg-url input from user

    # acc_url = input("Enter K歌 Account URL: ")
    acc_url = "https://node.kg.qq.com/personal?uid=6b9c9c83202d308b35"

    # Use Selenium to allow full loading of page
    driver.get(acc_url)
    album_btn = driver.find_element_by_id("album")
    driver.execute_script("arguments[0].click();", album_btn)
    time.sleep(1)

    # Progress
    print("URL parsed...")

    # Provision file structure
    provision(BeautifulSoup(driver.page_source, 'lxml'))


def provision(soup):
    """Provision folder structure for album downloads"""
    acc_name = soup.find("span", {"class": "my_show__name"}).next

    # Progress update
    print("Current Account: " + acc_name)

    # Remove account files if exists and re-create
    acc_file_path = os.path.join(OUTPUT_PATH, acc_name)

    if os.path.exists(acc_file_path):
        shutil.rmtree(acc_file_path, ignore_errors=True)
    os.mkdir(acc_file_path)

    # Extract songs from albums
    album_links = [link['href']
                   for link in soup.findAll("a", {"class": "mod_playlist__cover"}) if 'album' in link['href']]

    for link in album_links:
        # Create soup for album page
        req = requests.get(link, HEADERS)
        album_soup = BeautifulSoup(req.content, 'lxml')

        # path for album
        album_name = album_soup.find("h2", {"class": "play_name"}).next

        print("---Album Name: {}---".format(album_name))

        song_extract(album_soup, acc_file_path)


def song_extract(album_soup, acc_file_path):
    """Extracts songs and downloads in correct folders"""
    song_links = [link['href'] for link in album_soup.findAll(
        "a", {"class": "mod_song_list__body"})]

    for link in song_links:
        # Create soup for song page w/ Selenium
        driver.get(link)
        time.sleep(1)
        song_soup = BeautifulSoup(driver.page_source, "lxml")

        audio_elem = song_soup.find("audio")
        audio_src = audio_elem['src']
        audio_name = "{0}.mp3".format(audio_elem['meta'])

        print("Song: {}".format(audio_name))

        mp3_file = requests.get(audio_src, allow_redirects=True)
        
        with open(os.path.join(acc_file_path, audio_name), 'wb') as f:
            f.write(mp3_file.content)

        # urllib.request.urlretrieve(
        #     audio_src, os.path.join(album_file_path, audio_name))


if __name__ == "__main__":
    # Test
    links = ['https://node.kg.qq.com/album?s=6b9c9c83202d308b352176d9b3c8cfcf6fb1f69cd8b9efa698bf4a8b1281848c36d2d13c81e170d691&g_f=personal&appsource=', 'https://node.kg.qq.com/album?s=6b9c9c83202d308b352176d9b3c8cfcf6cb8f799d8bbeaa09cbe408e128e828c36d2d13c81e170d691&g_f=personal&appsource=', 'https://node.kg.qq.com/album?s=6b9c9c83202d308b352176d9b3c8cfcf6cb9f39ed8beeca39bbf4e821281ec800ad1d212acef67ce&g_f=personal&appsource=', 'https://node.kg.qq.com/album?s=6b9c9c83202d308b352176d9b3c8cfcf6cb4fa9fd8bdeea198b94d8b1686ec800ad1d212acef67ce&g_f=personal&appsource=',
             'https://node.kg.qq.com/album?s=6b9c9c83202d308b352176d9b3c8cfcf6cb3fb9fd8b9e4ad9cbc4b8b1585878c36d2d13c81e170d691&g_f=personal&appsource=', 'https://node.kg.qq.com/album?s=6b9c9c83202d308b352176d9b3c8cfcf68b8f495d8bfe4a39dbe488f1687ec800ad1d212acef67ce&g_f=personal&appsource=', 'https://node.kg.qq.com/album?s=6b9c9c83202d308b352176dabbcec2cb6cb2f49dd8beeca39eb041831780878c36d2d13c81e170d691&g_f=personal&appsource=', 'https://node.kg.qq.com/album?s=6b9c9c83202d308b352176dab5c9cfce6db4f599d8bbeca69eb8408d118e848c36d2d13c81e170d691&g_f=personal&appsource=']

    for link in links:
        req = requests.get(link, HEADERS)
        album_soup = BeautifulSoup(req.content, 'lxml')

        song_extract(album_soup, OUTPUT_PATH)

    # main()
