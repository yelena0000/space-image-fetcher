import argparse
import os
import random

import telegram
from environs import Env

from utils import get_all_files


def publish_photo(bot, chat_id, folder_name, photo_name=None):
    photos = get_all_files(folder_name)

    if not photos:
        print('Нет доступных фото для публикации.')
        return

    if photo_name:
        photo_path = os.path.join(folder_name, photo_name)
        if photo_path not in photos:
            print(f'Фото {photo_name} не найдено в указанной директории.')
            return
    else:
        photo_path = random.choice(photos)

    try:
        with open(photo_path, 'rb') as file:
            bot.send_photo(chat_id=chat_id, photo=file)
    except Exception as e:
        print(f"Ошибка при публикации {photo_path}: {e}")


def main():
    env = Env()
    env.read_env()

    parser = argparse.ArgumentParser(
        description='Скрипт для публикации фотографии в Telegram-канал.'
    )
    parser.add_argument(
        '--chat_id',
        type=str,
        help='ID или username Telegram-канала (например, @my_channel).'
    )
    parser.add_argument(
        '--directory',
        type=str,
        help='Путь к директории с фотографиями.'
    )
    parser.add_argument(
        '--photo_name',
        type=str,
        help=('Имя фотографии для публикации '
              '(если не указано, выбирается случайная).')
    )

    args = parser.parse_args()

    token = env.str('TG_BOT_TOKEN')
    bot = telegram.Bot(token=token)

    publish_photo(bot, args.chat_id, args.directory, args.photo_name)


if __name__ == '__main__':
    main()
