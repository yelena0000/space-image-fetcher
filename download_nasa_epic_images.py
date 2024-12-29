import argparse
import requests
from environs import Env

from utils import create_folder
from utils import download_and_save_image


def download_nasa_epic_images(api_key, folder_name, count=10):
    create_folder(folder_name)

    api_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    params = {'api_key': api_key}
    response = requests.get(api_url, params=params)
    response.raise_for_status()

    images_data = response.json()[:count]

    for index, image_data in enumerate(images_data, start=1):
        image_name = image_data['image']
        image_date = image_data['date']

        date_only = image_date.split(' ')[0]
        year, month, day = date_only.split('-')

        params = {'api_key': api_key}
        image_url = (
            f'https://api.nasa.gov/EPIC/archive/natural/'
            f'{year}/{month}/{day}/png/{image_name}.png'
        )
        image_url = requests.Request(
            'GET', image_url, params=params
        ).prepare().url
        download_and_save_image('nasa_epic', image_url, folder_name, index)


def main():
    parser = argparse.ArgumentParser(
        description='Скачивает изображения NASA EPIC.'
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
        help='Количество изображений для скачивания (по умолчанию 10).',
        default=10
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
        download_nasa_epic_images(api_key, args.folder_name, args.count)
    except requests.exceptions.RequestException as req_err:
        print(f"Ошибка при работе с API или сетью: {req_err}")
    except (ValueError, KeyError) as json_err:
        print(f"Ошибка обработки данных: {json_err}")
    except OSError as file_err:
        print(f"Ошибка при работе с файловой системой: {file_err}")
    except Exception as unexpected_err:
        print(f'Непредвиденная ошибка: {unexpected_err}')


if __name__ == '__main__':
    main()
