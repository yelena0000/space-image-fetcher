import argparse
import os
import requests
from environs import Env

from main import get_file_extension


def download_nasa_apod_images(api_key, folder_name, count=30):
    os.makedirs(folder_name, exist_ok=True)

    url = 'https://api.nasa.gov/planetary/apod'

    try:
        params = {'api_key': api_key, 'count': count}
        response = requests.get(url, params=params)
        response.raise_for_status()
        images_data = response.json()

        for index, image_data in enumerate(images_data, start=1):
            image_url = image_data.get('url')

            if not image_url or image_data.get('media_type') != 'image':
                continue

            try:
                image_response = requests.get(image_url)
                image_response.raise_for_status()

                file_extension = get_file_extension(image_url)

                filename = f'nasa_apod_{index}{file_extension}'
                save_path = os.path.join(folder_name, filename)

                with open(save_path, 'wb') as file:
                    file.write(image_response.content)

            except requests.exceptions.RequestException as e:
                print(f'Ошибка при скачивании изображения {image_url}: {e}')

    except requests.exceptions.RequestException as e:
        print(f'Ошибка при запросе API NASA: {e}')


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

    download_nasa_apod_images(api_key, args.folder_name, args.count)


if __name__ == '__main__':
    main()
