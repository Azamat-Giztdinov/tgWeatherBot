# Telegram Weather Bot



### Создайте файл .env и добавьте параметры подключения к OpenWeatherMapApi и TelegramApiToken
``` bash
cp .env.example .env
```

#### Запуск через docker-docker-compose
``` bash
docker-compose up --build -d
```

#### Запуск через виртуальное окружение

Создать виртуальное окружение venv и установить все зависимости:
```bash
python3 -m venv .venv
source venv/bin/activate
pip install -r requirements.txt
```

Запуск:
```bash
python3 bot.py
```