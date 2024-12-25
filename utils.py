import os
from urllib.parse import urlparse


def get_file_extension(url):
    parsed_url = urlparse(url)
    file_name = os.path.basename(parsed_url.path)
    file_extension = os.path.splitext(file_name)[1]
    return file_extension