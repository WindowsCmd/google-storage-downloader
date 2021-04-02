from bs4 import BeautifulSoup
import os
import urllib.request
import requests
import pathlib

GOOGLE_CLOUD_URL = "https://storage.googleapis.com/curious-sandbox-307908/"

folders = {}


def download_file(file_name):
    folder = file_name.split("/")[0]
    name = file_name.split("/")[1]

    print(f"Downloading {name}")

    if not folders.get(folder):
        os.mkdir(f"./files/{folder}")
        folders[folder] = True

    url = GOOGLE_CLOUD_URL + file_name
    location = f"./files/{folder}/{name}"

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, location)


def parse_xml(filename="storage.xml"):
    fd = open(filename, "r")

    xml_file = fd.read()

    soup = BeautifulSoup(xml_file, features="xml")

    for file_ in soup.findAll("Contents"):
        name = file_.find("Key")
        download_file(name.text)


def main():
    x = requests.get(GOOGLE_CLOUD_URL)
    f = open("storage.xml", "w")
    f.write(x.text)
    f.close()
    parse_xml()


if __name__ == "__main__":
    main()
