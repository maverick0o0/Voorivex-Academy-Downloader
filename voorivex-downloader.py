import time

import requests
import os
from dotenv import dotenv_values


import platform

if platform.system() == 'Windows':
    from idm import IDMan


# TODO
# Set connection speed
# Create a folder for each live ?
# User can change time.sleep for each process



# User Part
def GetFileSizeByUrl(url):
    response = requests.head(url)
    content_length = response.headers.get('Content-Length')
    if content_length:
        size_in_bytes = int(content_length)
        print(f"Url file size : {size_in_bytes} bytes")
        return size_in_bytes
    else:
        print("File size could not be determined.")
        return 0


def GetFileSizeByPath(file_path):
    if os.path.isfile(file_path):
        file_size = os.path.getsize(file_path)
        size_in_bytes = file_size
        return size_in_bytes
    else:
        print("Checking for downloaded file...")
        time.sleep(45)
        return 0


def WaitForDownload(url):
    urlFileSize = GetFileSizeByUrl(url)
    global pathFileSize
    pathFileSize = GetFileSizeByPath(file_path)

    if (urlFileSize == 0):
        WaitForDownload()

    while True:
        if (urlFileSize != 0 and pathFileSize != 0):
            print("Download completed.")
            time.sleep(5)
            break
        else:
            pathFileSize = GetFileSizeByPath(file_path)
            continue


def Download_With_IDM(url):
    time.sleep(5)
    downloader = IDMan()
    print(f"Saving in {file_path}")
    downloader.download(url, rf"{file_path_to_save}", f'{filename}', referrer=None, cookie=None,
                        postData=None, user=None, password=None, confirm=False, lflag='Test', clip=False)
    if (WaitForDownload(url)):
        print("Download finished starting new download ...")
        time.sleep(10)
    # else:
    #     time.sleep(5)
    #     WaitForDownload(url)


def Download_With_Request(url):
    chunk_size = 8192  # Adjust the chunk size as per your requirements
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    file.write(chunk)

            print("File downloaded successfully!")
            break  # Exit the loop if the download is successful
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            if attempt < max_retries:
                print(f"Retrying download... (Attempt {attempt + 1})")
                time.sleep(1)  # Pause for 1 second before the next attempt
        except IOError as e:
            print(f"IOError: {e}")
            break  # Exit the loop if there's an IOError


# Server Part
def RemoveVideo(key):
    url = 'https://dl-api.voorivex.academy/video/remove'

    payload = {
        'key': f'{key}'
    }

    response = requests.post(url, headers=headers, json=payload)

    if (response.status_code == 201):
        print("Removing previous video...")
        time.sleep(5)
        # print(response.text)
    else:
        print("Something went wrong !")


def CreateVideo(key):

    url = 'https://dl-api.voorivex.academy/video/ganerate'

    payload = {
        'key': f'{key}'
    }

    response = requests.post(url, headers=headers, json=payload)

    if (response.status_code == 201):
        print(f"Creating {key} video ...")
        time.sleep(5)
        return True
        # print(response.text)
    elif (response.status_code == 400):
        print("You have another video!")
        return False
        # DownloadVideo(key)
        # CreateVideo()


def GetVideoLink():
    url = 'https://dl-api.voorivex.academy/video/getActiveLink'

    response = requests.get(url, headers=headers)

    if (response.status_code == 200):
        result = response.json()
        if (result['type'] == 'pending'):
            print("Waiting for video link...")
            time.sleep(10)
            return None, None
        elif (result['type'] == 'active'):
            if (len(result['videos']) != 0):
                videoUrl = result['videos'][0]['url']
                key = result['videos'][0]['key']
                return videoUrl, key
            else:
                print("There is no video!")
                return None, None


def DownloadVideo(key):
    print("Start...")
    videoLink, fileToRemove = GetVideoLink()
    if (videoLink != None):
        RemoveVideo(fileToRemove)
    time.sleep(7)
    result = CreateVideo(key)
    if (result):
        while True:
            download_link, key = GetVideoLink()
            if (download_link != None):
                print('Download link is ', download_link)
                if (download_method == 'idm'):
                    Download_With_IDM(download_link)
                elif (download_method == 'default'):
                    Download_With_Request(download_link)
                break
            else:
                continue
    # else:
    #     DownloadVideo(key)


# User input
def select_folder():
    folder_path = input("Please enter the folder path: ")

    # Validate the folder path
    while not os.path.isdir(folder_path):
        print("Invalid folder path. Please try again.")
        folder_path = input("Please enter the folder path: ")

    # print("Selected folder path:", folder_path)
    return folder_path


def select_bearer():
    config = dotenv_values(".env")
    bearer_token = config["bearer_token"]
    if (bearer_token == ''):
        print("Please add your bearer token in .env")
        exit(1)
    return bearer_token


def select_download_method():
    method = input(
        "Choose the download method:\n1. Default method\n2. Use IDM\nEnter your choice (1 or 2): ")
    if method == "1":
        # use constants here
        return 'default'
    elif method == "2":
        # use constants here
        return 'idm'
    else:
        print("Invalid input. Please choose 1 or 2.")
        select_download_method()


def main():
    global file_path
    global filename
    global headers
    global file_path_to_save
    global download_method

    file_path_to_save = select_folder()
    bearer_token = select_bearer()
    download_method = select_download_method()

    headers = {
        'Host': 'dl-api.voorivex.academy',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {bearer_token}'
    }

    with open('keys.txt', '+r') as file:
        lines = file.readlines()
        for key in lines:
            filename = key.strip().split('/')[-1]
            file_path = file_path_to_save + '/' + filename
            if (os.path.exists(file_path)):
                print("This file exist ", file_path)
                continue
            else:
                print("Downloading new file ", key)
                DownloadVideo(key.strip())


# The download process has completed at this point
if __name__ == "__main__":
    main()
