import os
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
