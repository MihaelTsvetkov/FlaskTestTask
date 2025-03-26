import os
import io
import xml.sax as xs
from typing import List
from config import UPLOAD_FOLDER


class UniqueAttributesHandler(xs.ContentHandler):
    def __init__(self, target_tag: str) -> None:
        self.target_tag: str = target_tag
        self.attributes_set: set[str] = set()

    def startElement(self, name: str, attrs: xs.xmlreader.AttributesImpl) -> None:
        if name == self.target_tag:
            self.attributes_set.update(attrs.keys())


def get_unique_attributes_from_tag(file_name: str, tag_name: str) -> List[str]:
    file_path = os.path.join(UPLOAD_FOLDER, file_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f'Файл "{file_path}" не найден в директории xml файлов')

    with open(file_path, "rb") as f:
        xml_content = f.read()

    handler = UniqueAttributesHandler(tag_name)
    parser = xs.make_parser()
    parser.setContentHandler(handler)

    try:
        parser.parse(io.BytesIO(xml_content))
    except Exception as _:
        raise RuntimeError('Ошибка при разборе XML')

    return sorted(handler.attributes_set)
