import argparse
import os
import random

import telegram
from environs import Env

from utils import get_all_files
from utils import send_photo_to_telegram


def publish_photo(bot, chat_id, folder_name, photo_name=None):
    photos = get_all_files(folder_name)

    if not photos:
        raise ValueError(
            'Нет доступных фото для публикации в указанной директории.'
        )

    if photo_name:
        photo_path = os.path.join(folder_name, photo_name)
        if photo_path not in photos:
            raise FileNotFoundError(
                f'Фото {photo_name} не найдено в указанной директории.'
            )
    else:
        photo_path = random.choice(photos)

    send_photo_to_telegram(bot, chat_id, photo_path)


def main():
    env = Env()
    env.read_env()

    parser = argparse.ArgumentParser(
        description='Скрипт для публикации фотографии в Telegram-канал.'
    )
    parser.add_argument(
        '--chat_id',
        type=str,
        required=True,
        help='ID или username Telegram-канала (например, @my_channel).'
    )
    parser.add_argument(
        '--directory',
        type=str,
        required=True,
        help='Путь к директории с фотографиями.'
    )
    parser.add_argument(
        '--photo_name',
        type=str,
        help=('Имя фотографии для публикации '
              '(если не указано, выбирается случайная).')
    )

    args = parser.parse_args()

    try:
        token = env.str('TG_BOT_TOKEN')
        bot = telegram.Bot(token=token)

        publish_photo(bot, args.chat_id, args.directory, args.photo_name)

    except ValueError as e:
        print(f'Ошибка: {e}')
    except FileNotFoundError as e:
        print(f'Ошибка: {e}')
    except telegram.error.TelegramError as e:
        print(f'Ошибка при работе с Telegram API: {e}')
    except Exception as e:
        print(f'Неожиданная ошибка: {e}')


if __name__ == '__main__':
    main()
