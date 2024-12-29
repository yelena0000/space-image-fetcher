import argparse
import random
import time

import telegram
from environs import Env

from utils import get_all_files
from utils import send_photo_to_telegram


def publish_photos(bot, chat_id, folder_name, delay):
    try:
        photos = get_all_files(folder_name)
    except OSError as os_err:
        raise RuntimeError(f"Ошибка при чтении директории "
                           f"{folder_name}: {os_err}")

    if not photos:
        raise ValueError('Нет доступных фото для публикации. '
                         'Добавьте файлы в указанную директорию.')

    published_photos = []

    while True:
        for photo in photos:
            try:
                send_photo_to_telegram(bot, chat_id, photo)
                published_photos.append(photo)
            except telegram.error.TelegramError as tg_err:
                print(f'Ошибка при отправке фото {photo}: {tg_err}')
            except Exception as unexpected_err:
                print(f'Непредвиденная ошибка при отправке фото '
                      f'{photo}: {unexpected_err}')
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
            'Не указан chat_id. '
            'Укажите его через --chat_id или переменную окружения TG_CHAT_ID.'
        )
        return

    try:
        token = env.str('TG_BOT_TOKEN')
        bot = telegram.Bot(token=token)

        publish_photos(bot, args.chat_id, args.directory, args.delay)

    except ValueError as val_err:
        print(f'Ошибка: {val_err}')
    except RuntimeError as runtime_err:
        print(f'Ошибка работы с файловой системой: {runtime_err}')
    except telegram.error.TelegramError as tg_err:
        print(f'Ошибка Telegram API: {tg_err}')
    except Exception as unexpected_err:
        print(f'Неожиданная ошибка: {unexpected_err}')


if __name__ == '__main__':
    main()
