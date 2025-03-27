import sqlite3
import xml.sax as xs
from typing import Optional
from xml.sax.xmlreader import AttributesImpl
from config import DB_PATH


class XMLToDBHandler(xs.ContentHandler):
    def __init__(self, xml_filename: str) -> None:
        self.conn: sqlite3.Connection = sqlite3.connect(DB_PATH)
        self.cursor: sqlite3.Cursor = self.conn.cursor()
        self.conn.execute("BEGIN")
        self.current_file_id: Optional[int] = None
        self.current_tag_id: Optional[int] = None
        self.success: bool = True
        self.xml_filename: str = xml_filename

    def startElement(self, name: str, attrs: AttributesImpl) -> None:
        try:
            if name == "File":
                if "id" not in attrs or "name" not in attrs:
                    self.success = False
                    return

                file_id = int(attrs["id"])
                self.current_file_id = file_id

                self.cursor.execute(
                    "INSERT OR IGNORE INTO Files (id, name) VALUES (?, ?)",
                    (file_id, self.xml_filename)
                )

            elif name == "Tag":
                if self.current_file_id is None:
                    self.success = False
                    return

                tag_id = int(attrs["id"])
                tag_name = attrs["name"]
                self.current_tag_id = tag_id

                self.cursor.execute(
                    "INSERT OR IGNORE INTO Tags (id, name, file_id) VALUES (?, ?, ?)",
                    (tag_id, tag_name, self.current_file_id)
                )

            elif name == "Attribute":
                if self.current_tag_id is None:
                    self.success = False
                    return

                attr_id = int(attrs["id"])
                attr_name = attrs["name"]
                attr_value = attrs["value"]

                self.cursor.execute(
                    "INSERT OR IGNORE INTO Attributes (id, name, value, tag_id) VALUES (?, ?, ?, ?)",
                    (attr_id, attr_name, attr_value, self.current_tag_id)
                )

        except Exception:
            self.success = False

    def endDocument(self) -> None:
        self.conn.commit()
        self.conn.close()
