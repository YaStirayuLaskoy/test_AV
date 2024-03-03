import re
from typing import Dict
from fastapi import FastAPI


app = FastAPI(
    title="Analyz"
)


@app.post("/analyze_message/")
async def analyze_message(message: Dict):
    file_path = message.get("file_path", "")

    if file_path:
        text = get_text_from_file(file_path)
        if text:
            words_count = extract_and_store_words(text)
            return {"message": f"Words extracted and stored for file: {file_path}"}

    return {"message": "Error analyzing message"}


def get_text_from_file(file_path):
    # Чтение
    with open(file_path, "r") as file:
        text = file.read()
    return text


def extract_and_store_words(text):
    # Извлекает слово из текста
    words = re.findall(r'\b\w+\b', text)
    words_count = {}

    for word in words:
        if word in words_count:
            words_count[word] += 1
        else:
            words_count[word] = 1

    for word, count in words_count.items():
        insert_word_count_to_db(word, count)

    return words_count


def insert_word_count_to_db(word, count):
    # Вставка слова и количества вхождений в базу данных
    sql = "INSERT INTO word_counts (word, count) VALUES (%s, %s)"
    val = (word, count)
