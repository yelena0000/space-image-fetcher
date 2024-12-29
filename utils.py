import os
import requests
from urllib.parse import urlparse


def create_folder(folder_name):
    os.makedirs(folder_name, exist_ok=True)


def get_file_extension(url):
    parsed_url = urlparse(url)
    file_name = os.path.basename(parsed_url.path)
    file_extension = os.path.splitext(file_name)[1]
    return file_extension


def get_all_files(directory):
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            all_files.append(full_path)
    return all_files


def download_and_save_image(image_name, image_url, folder_name, index):

    image_response = requests.get(image_url)
    image_response.raise_for_status()

    file_extension = get_file_extension(image_url)
    filename = f'{image_name}_{index}{file_extension}'

    save_path = os.path.join(folder_name, filename)

    with open(save_path, 'wb') as file:
        file.write(image_response.content)


def send_photo_to_telegram(bot, chat_id, photo_path):
    with open(photo_path, 'rb') as file:
        bot.send_photo(chat_id=chat_id, photo=file)


def fetch_spacex_launch_data(launch_id=None):

    base_url = 'https://api.spacexdata.com/v5/launches'
    url = f'{base_url}/{launch_id}' if launch_id else f'{base_url}/latest'

    response = requests.get(url)
    response.raise_for_status()
    return response.json()
