import argparse
import os
import requests
from environs import Env


def download_nasa_epic_images(api_key, folder_name, count=10):
    os.makedirs(folder_name, exist_ok=True)
    api_url = 'https://api.nasa.gov/EPIC/api/natural/images'

    try:
        params = {'api_key': api_key}
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        images_data = response.json()[:count]

        for index, image_data in enumerate(images_data, start=1):
            image_name = image_data['image']
            image_date = image_data['date']

            date_only = image_date.split(' ')[0]
            year, month, day = date_only.split('-')

            image_url = (
                f'https://api.nasa.gov/EPIC/archive/natural/'
                f'{year}/{month}/{day}/png/{image_name}.png?api_key={api_key}'
            )
            try:
                image_response = requests.get(image_url)
                image_response.raise_for_status()

                filename = f'nasa_epic_{index}.png'
                save_path = os.path.join(folder_name, filename)
                with open(save_path, 'wb') as file:
                    file.write(image_response.content)

            except requests.exceptions.RequestException as e:
                print(f'Ошибка при скачивании изображения {image_url}: {e}')

    except requests.exceptions.RequestException as e:
        print(f'Ошибка при запросе API EPIC: {e}')


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

    download_nasa_epic_images(api_key, args.folder_name, args.count)


if __name__ == '__main__':
    main()
