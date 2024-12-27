# Космический Телеграм

Проект состоит из нескольких Python-скриптов, которые выполняют различные задачи:

- Скачивает изображения NASA APOD (Astronomy Picture of the Day) и NASA EPIC (Earth Polychromatic Imaging Camera).
- Скачивает изображения с запусков SpaceX.
- Публикует фотографии в Telegram-канал с использованием Telegram-бота.
- Поддерживает публикацию всех фотографий из указанной директории или одной случайной фотографии.

### Как установить

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```


Перейдите на сайт [NASA API](https://api.nasa.gov/), создайте учетную запись и получите API ключ. 
Сохраните его в переменной окружения `NASA_API_KEY` или передайте через аргумент `--api_key`.
Для работы с SpaceX не требуется получать API ключ.



Для работы с Telegram-ботом создайте бота через [BotFather](https://core.telegram.org/bots#botfather) и получите токен. 
Укажите этот токен в переменной окружения `TG_BOT_TOKEN`. 
Также укажите `TG_CHAT_ID`, который можно получить из Telegram (например, через `@userinfobot`).


#### Перед запуском скриптов убедитесь, что:

У вас создан файл `.env`, в котором указаны следующие переменные окружения:
```commandline
NASA_API_KEY='your_nasa_api_key'
TG_BOT_TOKEN='your_telegram_bot_token'
TG_CHAT_ID='@example'
DELAY=12345
```
***
### Скрипты
`download_nasa_apod_images.py`

Скрипт для скачивания изображений из **NASA APOD (Astronomy Picture of the Day)**.

Пример использования:

```bash
python download_nasa_apod_images.py --api_key <your_api_key> <folder_name> --count 30
```
Аргументы:

`--api_key`: ваш API ключ NASA.

`<folder_name>`: папка, в которую будут сохранены изображения.

`--count`: количество изображений для скачивания (по умолчанию 30).
***
`download_nasa_epic_images.py`
Скрипт для скачивания изображений из **NASA EPIC (Earth Polychromatic Imaging Camera)**.

Пример использования:

```bash
python download_nasa_epic_images.py --api_key <your_api_key> <folder_name> --count 10
```
Аргументы:

`--api_key`: ваш API ключ NASA.

`<folder_name>`: папка для сохранения изображений.

`--count`: количество изображений (по умолчанию 10).
***
`fetch_spacex_images.py`

Скрипт для скачивания изображений с запуска **SpaceX**. 
Поддерживает указание ID запуска или автоматическое скачивание изображений с последнего запуска.

Пример использования:
```bash
python fetch_spacex_images.py <folder_name> --launch_id <launch_id>
```
Аргументы:

`<folder_name>`: папка для сохранения фотографий.

`--launch_id`: ID запуска SpaceX (если не указан, будет использован последний запуск).
***
```telegram_photo_publisher.py```

Скрипт для публикации всех фотографий из указанной папки в Telegram-канал с заданной задержкой между публикациями.

Пример использования:

```bash
python telegram_photo_publisher.py --chat_id <your_chat_id> --directory <folder_name> --delay 14400
```
Аргументы:

`--chat_id`: ID или username Telegram-канала.

`--directory`: путь к папке с фотографиями.

`--delay`: задержка между публикациями в секундах (по умолчанию 14400 секунд, или 4 часа).
***
`telegram_single_photo_publisher.py`
Скрипт для публикации одной фотографии в Telegram-канал. Если не указано имя фотографии, будет выбрана случайная.

Пример использования:

```bash
python telegram_single_photo_publisher.py --chat_id <your_chat_id> --directory <folder_name> --photo_name <photo_name>
```
Аргументы:

`--chat_id`: ID или username Telegram-канала.
`--directory`: путь к папке с фотографиями.
`--photo_name`: имя фотографии для публикации (если не указано, выберется случайная).
***
#### Вспомогательные скрипты:

`create_folder(folder_name)` - функция для создания папки, если она не существует.

`get_file_extension(url)` - функция для получения расширения файла по URL.

`get_all_files(directory)` - функция для получения всех файлов из указанной директории.
***
### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).