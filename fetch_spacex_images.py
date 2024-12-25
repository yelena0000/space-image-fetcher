import argparse
import os
import requests


def fetch_spacex_launch(launch_id, folder_name):
    os.makedirs(folder_name, exist_ok=True)

    try:
        url = f'https://api.spacexdata.com/v5/launches/{launch_id}'
        response = requests.get(url)
        response.raise_for_status()

        response_data = response.json()
        photos_url = response_data.get('links', {}).get(
            'flickr', {}).get('original', [])

        if not photos_url:
            print('Фотографий для данного запуска нет.')
            return

        for index, photo_url in enumerate(photos_url, start=1):
            try:
                photo_response = requests.get(photo_url)
                photo_response.raise_for_status()

                filename = f'spacex_{index}.jpg'
                save_path = os.path.join(folder_name, filename)

                with open(save_path, 'wb') as file:
                    file.write(photo_response.content)

            except requests.exceptions.RequestException as e:
                print(f'Ошибка при скачивании {photo_url}: {e}')

    except requests.exceptions.RequestException as e:
        print(f'Ошибка при запросе API или обработке данных: {e}')


def get_latest_spacex_launch_id():
    try:
        url = 'https://api.spacexdata.com/v5/launches/latest'
        response = requests.get(url)
        response.raise_for_status()

        response_data = response.json()
        return response_data['id']

    except requests.exceptions.RequestException as e:
        print(f'Ошибка при запросе последнего запуска: {e}')
        return None


def main():
    parser = argparse.ArgumentParser(
        description='Скачивает фото от SpaceX по указанному ID запуска.')

    parser.add_argument(
        'folder_name',
        type=str,
        help='Имя папки, куда будут сохранены фотографии.'
    )

    parser.add_argument(
        '--launch_id',
        type=str,
        help=('ID запуска SpaceX. '
              'Если не указан, будет использоваться последний запуск.'),
        default=None
    )

    args = parser.parse_args()

    if args.launch_id is None:
        args.launch_id = get_latest_spacex_launch_id()
        if not args.launch_id:
            print('Не удалось получить ID последнего запуска.')
            return

    fetch_spacex_launch(args.launch_id, args.folder_name)


if __name__ == '__main__':
    main()
