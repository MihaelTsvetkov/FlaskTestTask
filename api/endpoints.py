import os
import xml.sax as xs
from typing import Any, Dict
from flask import Blueprint, jsonify, request, Response
from utils.xml_to_db_handler import XMLToDBHandler
from utils.tag_counter_handler import TagCounterHandler
from utils.get_unique_attributes_from_tag import get_unique_attributes_from_tag
from config import UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

api = Blueprint("api", __name__)


@api.route('/api/tags/get-count', methods=['POST'])
def get_count() -> Response:
    data: Dict[str, Any] = request.get_json()

    if not data:
        return jsonify({'Ошибка': 'Ожидается JSON тело запроса'}), 400

    tag_name: str = data.get('tag_name')
    file_path: str = data.get('file_path')

    if not tag_name or not file_path:
        return jsonify({'error': 'Параметры "tag_name" и "file_path" обязательны'}), 400

    if not os.path.exists(file_path):
        return jsonify({'error': f'Файл не найден: {file_path}'}), 404

    handler = TagCounterHandler(tag_name)
    parser = xs.make_parser()
    parser.setContentHandler(handler)

    try:
        parser.parse(file_path)
    except FileNotFoundError:
        return jsonify({'error': f'Файл не найден: {file_path}'}), 404
    except Exception:
        return jsonify({'error': 'Ошибка при разборе XML'}), 500

    if handler.count == 0:
        return jsonify({'error': 'В файле отсутствует тег с данным названием'}), 404

    return jsonify({'tag': tag_name, 'count': handler.count})


@api.route('/api/file/read', methods=['POST'])
def read_file() -> Response:
    if 'file' not in request.files:
        return jsonify({'result': False}), 400

    file = request.files['file']

    if file.filename == '' or not file.filename.endswith('.xml'):
        return jsonify({'result': False}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        handler = XMLToDBHandler(file.filename)
        parser = xs.make_parser()
        parser.setContentHandler(handler)
        parser.parse(filepath)

        return jsonify({"result": handler.success}), 200 if handler.success else 400

    except Exception:
        return jsonify({"result": False}), 500


@api.route('/api/tags/attributes/get', methods=['POST'])
def get_attributes() -> Response:
    data: Dict[str, Any] = request.get_json()

    if not data:
        return jsonify({'Ошибка': 'Ожидается JSON тело запроса'}), 400

    tag_name: str = data.get('tag_name')
    file_name: str = data.get('file_name')

    if not tag_name or not file_name:
        return jsonify({'Ошибка': 'Параметры "tag_name" и "file_name" обязательны'}), 400

    try:
        attrs = get_unique_attributes_from_tag(file_name, tag_name)
        return jsonify({'attributes': attrs})

    except FileNotFoundError:
        return jsonify({'Ошибка': 'Файл не найден'}), 404
    except RuntimeError:
        return jsonify({'Ошибка': 'Ошибка во время парсинга'}), 400
    except Exception as e:
        return jsonify({'Ошибка': 'Внутренняя ошибка'}), 500
