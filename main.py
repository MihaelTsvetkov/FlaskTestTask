import sqlite3
from flask import Flask
from api.endpoints import api
from config import DB_PATH

app = Flask(__name__)
app.register_blueprint(api)


def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Files (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tags (
            id INTEGER PRIMARY KEY,
            name TEXT,
            file_id INTEGER,
            FOREIGN KEY (file_id) REFERENCES Files(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Attributes (
            id INTEGER PRIMARY KEY,
            name TEXT,
            value TEXT,
            tag_id INTEGER,
            FOREIGN KEY (tag_id) REFERENCES Tags(id)
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def main() -> str:
    return (
        "<h2>API для работы с XML</h2>"
        "<ul>"
        "<li><b>POST /api/file/read</b> — Загрузка XML-файла. Передаётся файл через <i>form-data</i>, параметр: <code>file</code> (.xml)</li>"
        "<li><b>POST /api/tags/get-count</b> — Получить количество заданных тегов в XML-файле. "
        "Передаётся JSON: <code>{ \"file_path\": \"путь до файла\", \"tag_name\": \"Tag\" }</code></li>"
        "<li><b>POST /api/tags/attributes/get</b> — Получить список уникальных атрибутов заданного тега. "
        "Передаётся JSON: <code>{ \"file_name\": \"data.xml\", \"tag_name\": \"Attribute\" }</code></li>"
        "</ul>"
    )



if __name__ == "__main__":
    init_db()
    app.run(debug=True)
