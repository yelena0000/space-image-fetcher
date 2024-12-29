import argparse
import requests
from environs import Env

from utils import download_and_save_image
from utils import create_folder


def download_nasa_apod_images(api_key, folder_name, count=30):
    create_folder(folder_name)
    url = 'https://api.nasa.gov/planetary/apod'

    params = {'api_key': api_key, 'count': count}
    response = requests.get(url, params=params)
    response.raise_for_status()
    images_data = response.json()

    for index, image_data in enumerate(images_data, start=1):
        image_url = image_data.get('url')

        if not image_url or image_data.get('media_type') != 'image':
            continue

        download_and_save_image('nasa_apod', image_url, folder_name, index)


def main():
    parser = argparse.ArgumentParser(
        description='Скачивает изображения NASA APOD.'
    )
    parser.add_argument(
        '--api_key',
        type=str,
        help='Ваш API ключ NASA. '
             'Если не указан, используется ключ из переменных окружения.',
        default=None
    )
    parser.add_argument(
        'folder_name',
        type=str,
        help='Имя папки, куда будут сохранены изображения.'
    )
    parser.add_argument(
        '--count',
        type=int,
        help='Количество изображений для скачивания (по умолчанию 30).',
        default=30
    )

    args = parser.parse_args()

    env = Env()
    env.read_env()
    api_key = args.api_key or env.str('NASA_API_KEY', default=None)

    if not api_key:
        print('API ключ не найден. Укажите его через --api_key '
              'или переменную окружения NASA_API_KEY.')
        return

    try:
        download_nasa_apod_images(api_key, args.folder_name, args.count)
    except requests.exceptions.RequestException as req_err:
        print(f"Ошибка сети или API: {req_err}")
    except OSError as file_err:
        print(f"Ошибка при работе с файлами: {file_err}")
    except Exception as unexpected_err:
        print(f'Непредвиденная ошибка: {unexpected_err}')


if __name__ == '__main__':
    main()
