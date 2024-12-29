# Космический Телеграм

Проект состоит из нескольких Python-скриптов, которые выполняют различные задачи:

- Скачивает изображения NASA APOD (Astronomy Picture of the Day) и NASA EPIC (Earth Polychromatic Imaging Camera).
- Скачивает изображения с запусков SpaceX.
- Публикует фотографии в Telegram-канал с использованием Telegram-бота.
- Поддерживает публикацию всех фотографий из указанной директории или одной случайной фотографии.

## Как установить

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```


Перейдите на сайт [NASA API](https://api.nasa.gov/), создайте учетную запись и получите API ключ. 
Сохраните его в переменной окружения `NASA_API_KEY` или передайте через аргумент `--api_key`.
Для работы с SpaceX не требуется получать API ключ.



Для работы с Telegram-ботом создайте бота через [BotFather](https://telegram.me/BotFather) и получите токен. 
Укажите этот токен в переменной окружения `TG_BOT_TOKEN`. 
Также укажите `TG_CHAT_ID`, который можно получить из Telegram (например, через `@userinfobot`).


### Переменные окружения:

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `manage.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`:

```
NASA_API_KEY='your_nasa_api_key'
TG_BOT_TOKEN='your_telegram_bot_token'
TG_CHAT_ID='@example'
DELAY=12345
```
***
## Описание скриптов
### download_nasa_apod_images.py

Скрипт для скачивания изображений из **NASA APOD (Astronomy Picture of the Day)**.

```bash
python download_nasa_apod_images.py --api_key <your_api_key> <folder_name> --count 12
```

В приведённом выше примере: `<your_api_key>` - ваш API ключ NASA, `<folder_name>` - папка, в которую будут сохранены изображения, `12` - количество изображений для скачивания (по умолчанию 30).
***
### download_nasa_epic_images.py

Скрипт для скачивания изображений из **NASA EPIC (Earth Polychromatic Imaging Camera)**.


```bash
python download_nasa_epic_images.py --api_key <your_api_key> <folder_name> --count 12
```
В приведённом выше примере:  `<your_api_key>` - ваш API ключ NASA,  `<folder_name>` - папка для сохранения изображений, `12` - количество изображений (по умолчанию 10).
***
### fetch_spacex_images.py

Скрипт для скачивания изображений с запуска **SpaceX**. 
Поддерживает указание ID запуска или автоматическое скачивание изображений с последнего запуска.

```bash
python fetch_spacex_images.py <folder_name> --launch_id <launch_id>
```
В приведённом выше примере:  `<folder_name>` - папка для сохранения фотографий, `<launch_id>` - ID запуска SpaceX (если не указан, будет использован последний запуск).
***
### telegram_photo_publisher.py

Скрипт для публикации всех фотографий из указанной папки в Telegram-канал с заданной задержкой между публикациями.

```bash
python telegram_photo_publisher.py --chat_id <your_chat_id> --directory <folder_name> --delay 12345
```
В приведённом выше примере: `<your_chat_id>` - ID или username Telegram-канала, `<folder_name>` - путь к папке с фотографиями, `12345` - задержка между публикациями в секундах (по умолчанию 14400 секунд, или 4 часа).
***
### telegram_single_photo_publisher.py

Скрипт для публикации одной фотографии в Telegram-канал. Если не указано имя фотографии, будет выбрана случайная.

```bash
python telegram_single_photo_publisher.py --chat_id <your_chat_id> --directory <folder_name> --photo_name <photo_name>
```
В приведённом выше примере: `<your_chat_id>` - ID или username Telegram-канала,`<folder_name>` - путь к папке с фотографиями, `<photo_name>` - имя фотографии для публикации (если не указано, выберется случайная).
***
### Вспомогательные скрипты:

`create_folder(folder_name)` - функция для создания папки, если она не существует.

`get_file_extension(url)` - функция для получения расширения файла по URL.

`get_all_files(directory)` - функция для получения всех файлов из указанной директории.

`download_and_save_image(image_name, image_url, folder_name, index)` -функция для скачивания изображения
из указанного URL и сохранения его в указанной папке.

`send_photo_to_telegram(bot, chat_id, photo_path)` - функция для отправки изображения в Telegram-канал или чат.

`fetch_spacex_launch_data(launch_id=None)` - функция для получения данных о запуске SpaceX по указанному ID 
или о последнем запуске, если ID не задан.
***
## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
