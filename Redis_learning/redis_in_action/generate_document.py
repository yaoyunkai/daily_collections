"""


Created at 2023/3/22
"""

import random
from datetime import datetime, timedelta

from faker import Faker
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def generate_docs(numbers=50):
    doc_ids = list(range(10000, 99999))
    random.shuffle(doc_ids)
    fake = Faker()

    docs = []
    for i in range(numbers):
        doc_id = doc_ids[i]
        title = fake.sentence()

        end_time = datetime.now()
        start_time = end_time - timedelta(days=30)
        created = start_time + (end_time - start_time) * random.random()

        doc = {
            'id': doc_id,
            'created': int(created.timestamp()),
            'updated': int(created.timestamp()),
            'title': title,
            'content': fake.text()
        }
        docs.append(doc)

    return docs


def tokenize(content: str):
    content = content.lower()
    words = word_tokenize(content)
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in words if word.casefold() not in stop_words]
    return filtered_words


if __name__ == '__main__':
    for item in generate_docs():
        print(item)
        # print(tokenize(item['content']))
