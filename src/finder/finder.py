import os
import json
from fastapi import FastAPI
# import magic

from .models import FileEvent


"""
Компонент «Ищейка»
Ожидает появления файлов в папке и обрабатывает их:
при нахождении текстового файла (подразумеваются обычные файлы формата txt –
с указанием формата или без указания) - перекладывает его в volume
«Анализатора» и передает json сообщение посредством очереди: «Parsing»,
в сообщении указывает путь до найденного файла после его перемещения.
Если тип файла не текстовый, тогда переложить файл в volume «Ошибочников»
и отправить сообщение в «Errors»;
В сообщении указывает путь до найденного файла после его
перемещения.
"""


app = FastAPI(
    title="Isheyka"
)


@app.post("/handle_file_event/")
async def handle_file_event(file_event: FileEvent):
    """
    Была попытка реализовать через модуль Magic, но программа крашилась.
    Из за чего это, разобраться не успел, поэтому сделал через
    указание формата. Не совсем корректно, так как по ТЗ сказано,
    что формат не всегда может быть указан.
    """
    file_path = file_event.path

    # Определение типа файла
    # file_type = get_file_type(file_path)

    if file_path.endswith('.txt'):
        # Если файл текстовый, переместить и отправить сообщение в "Parsing"
        move_file_to_analyzer(file_path)
        send_message_to_queue("Parsing", file_path)
    else:
        # Если файл не текстовый, переместить и отправить сообщение в "Errors"
        move_file_to_errors(file_path)
        send_message_to_queue("Errors", file_path)

    return {"message": "File event processed successfully"}


# def get_file_type(file_path):
#     mime = magic.Magic()
#     return mime.from_file(file_path)


def move_file_to_analyzer(file_path):
    """Перемещает файл в Анализатор."""
    os.replace(file_path, f"/path/to/analyzer/{os.path.basename(file_path)}")


def move_file_to_errors(file_path):
    """Перемещает файл в Errors."""
    os.replace(file_path, f"/path/to/errors/{os.path.basename(file_path)}")


def send_message_to_queue(queue_name, file_path):
    """Отправит сообщение с указанием пути до файла в очередь."""
    message = json.dumps({"file_path": file_path})
    print(f"Message sent to queue '{queue_name}': {message}")