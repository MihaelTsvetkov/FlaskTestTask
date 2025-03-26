# XML Parser Microservice

Микросервис на Flask, предназначенный для загрузки, парсинга и анализа XML-файлов с сохранением данных в SQLite. Реализован на основе `xml.sax`.

## Технологии
- Python 3.10+
- Flask
- SQLite
- XML SAX Parser

---

## База данных

Создаётся автоматически при запуске.

## Запуск проекта

1. Клонируйте репозиторий:

```
git clone https://github.com/MihaelTsvetkov/FlaskTestTask.git
cd FlaskTestTask
```

2. Создайте и активируйте виртуальное окружение

```
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate  # Linux/macOS
```

3. Установите зависимости:

```
pip install -r requirements.txt
```

4. Запустите проект:

```
python main.py
```


Доступные API

1. POST /api/file/read

```
Загрузка и парсинг XML-файла.
Параметры: form-data
file — XML-файл 
```

2. POST /api/tags/get-count
```
Подсчёт количества определённых тегов в XML-файле.
Параметры: JSON

{
  "file_path": "путь до xml файла",
  "tag_name": "Tag"
}
```

3. POST /api/tags/attributes/get

```
Получение уникальных атрибутов у тега.
Параметры: JSON

{
  "file_name": "название xml файла",
  "tag_name": "Attribute"
}
```
