# Voorivex-Academy-Downloader

A Python script to download videos from the voorivex.academy website. Due to limitations on the website, it is not possible to download multiple videos simultaneously. This script allows you to download the videos one by one using the site's API and Internet Download Manager for faster and easier downloads.Also you can you can download movies without IDM.

## Prerequisites

- Python 3.x
- Internet Download Manager (IDM)

## Installation

1. Clone the repository:

`git clone https://github.com/maverick0o0/Voorivex-Academy-Downloader.git`


2. Navigate to the project directory:

`cd Voorivex-Academy-Downloader`


3. Install the required dependencies:

`pip3 install -r requirements.txt`


4. Login to your voorivex.academy account using your credentials.

5. Open the website and press F12 to open the developer console.

6. Go to the "Storage" tab and copy the value of the dl-token from the "Cookies" section.
<div align='left'>
<img src="/images/TokenPlace.png" height="200px">

7. Open the `.env` file and replace `bearer_token` with your actual token.

## Usage

Run the script:
`python3 voorivex-downloader.py`


The script will read the video keys from the `keys.txt` file and start downloading the videos one by one using IDM.

## Guide

### What is keys.txt file?
All videos are associated with a unique key that is used for creation or deletion. This key essentially represents the video's name. The program iterates through this file and generates the download for each video.
By editing this file you can choose what video you want to download. (for now just TA lives and Hunt lives)

### What are create-keys.py & html-data.txt files?
In this section, we parse the HTML page and extract all the keys (video names) using regular expressions (regex). These keys are then saved inside the keys.txt file.



## Unreliable Network Connection

In IDM open **Scheduler** and in **Main download queue** set **Number of retries for each file if downloading failed** to 10. 
<div align='left'>
<img src="/images/IDM.png" height="200px">
</div>

## Contributing

Contributions are welcome! If you have any improvements or new features to add, please follow these steps:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Commit and push your changes.
5. Submit a pull request.

Please make sure to follow the code style and provide a clear description of your changes.

Thank you for your contributions!




