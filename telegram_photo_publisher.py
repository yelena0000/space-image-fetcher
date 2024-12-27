import argparse
import random
import time

import telegram
from environs import Env

from utils import get_all_files


def publish_photos(bot, chat_id, folder_name, delay):
    photos = get_all_files(folder_name)

    while True:
        if not photos:
            print('Нет доступных фото для публикации.'
                  'Ожидание новых файлов...')
            time.sleep(delay)
            photos = get_all_files(folder_name)
            continue

        published_photos = []

        for photo in photos:
            try:
                with open(photo, 'rb') as file:
                    bot.send_photo(chat_id=chat_id, photo=file)
                published_photos.append(photo)
            except Exception as e:
                print(f'Ошибка при публикации {photo}: {e}')

            time.sleep(delay)

        photos = published_photos.copy()
        random.shuffle(photos)
        published_photos.clear()


def main():
    env = Env()
    env.read_env()

    parser = argparse.ArgumentParser(
        description='Скрипт для публикации фото в Telegram-канал.'
    )
    parser.add_argument(
        '--chat_id',
        type=str,
        default=env.str('TG_CHAT_ID', None),
        help=('ID или username Telegram-канала (например, @my_channel). '
              'Если не указан, используется TG_CHAT_ID из переменных окружения.')
    )
    parser.add_argument(
        '--directory',
        type=str,
        required=True,
        help='Путь к директории с фотографиями.'
    )
    parser.add_argument(
        '--delay',
        type=int,
        default=env.int('DELAY', 14400),
        help='Задержка между публикациями в секундах (по умолчанию 4 часа).'
    )

    args = parser.parse_args()

    if not args.chat_id:
        print(
            'Не указан chat_id.'
            'Укажите его через --chat_id или переменную окружения TG_CHAT_ID.'
        )
        return

    token = env.str('TG_BOT_TOKEN')
    bot = telegram.Bot(token=token)

    publish_photos(bot, args.chat_id, args.directory, args.delay)


if __name__ == '__main__':
    main()
