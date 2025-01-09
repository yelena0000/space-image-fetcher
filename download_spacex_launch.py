import argparse
import requests

from utils import create_folder
from utils import download_and_save_image
from utils import fetch_spacex_launch_data


def download_spacex_launch(launch_id, folder_name):
    create_folder(folder_name)

    photo_urls = (
        fetch_spacex_launch_data(launch_id)
        .get('links', {})
        .get('flickr', {})
        .get('original', [])
    )

    if not photo_urls:
        raise ValueError(f'Фотографий для запуска {launch_id} нет.')

    for index, photo_url in enumerate(photo_urls, start=1):
        download_and_save_image('spacex', photo_url, folder_name, index)


def get_latest_spacex_launch_id():
    launch_data = fetch_spacex_launch_data()
    return launch_data.get('id')


def main():
    parser = argparse.ArgumentParser(
        description='Скачивает фото от SpaceX по указанному ID запуска.'
    )

    parser.add_argument(
        '--folder_name',
        type=str,
        default='images',
        help='Имя папки, куда будут сохранены фотографии (по умолчанию "images").'
    )

    parser.add_argument(
        '--launch_id',
        type=str,
        help=('ID запуска SpaceX. '
              'Если не указан, будет использоваться последний запуск.'),
        default=None
    )

    args = parser.parse_args()

    try:
        if args.launch_id is None:
            args.launch_id = get_latest_spacex_launch_id()

        download_spacex_launch(args.launch_id, args.folder_name)
    except requests.exceptions.RequestException as req_err:
        print(f'Ошибка сети или запроса к API: {req_err}')
    except ValueError as value_err:
        print(f'Ошибка данных: {value_err}')
    except OSError as os_err:
        print(f'Ошибка файловой системы: {os_err}')
    except Exception as unexpected_err:
        print(f'Непредвиденная ошибка: {unexpected_err}')


if __name__ == '__main__':
    main()
