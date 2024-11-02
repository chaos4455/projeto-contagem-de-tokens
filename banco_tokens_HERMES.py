import sqlite3
import hashlib
import datetime
import json
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch

def create_database(db_name="tokens_database.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            unique_hash TEXT UNIQUE,
            input_text TEXT,
            tokens TEXT,
            embeddings BLOB
        )
    ''')
    conn.commit()
    conn.close()


def generate_unique_hash(input_text):
    return hashlib.sha256(input_text.encode()).hexdigest()


def analyze_bert(text, model_name="bert-base-uncased"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    tokens = tokenizer.tokenize(text)
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).numpy()
    return tokens, embeddings


def insert_data(input_text, tokens, embeddings, db_name="tokens_database.db"):
    timestamp = datetime.datetime.now().isoformat()
    unique_hash = generate_unique_hash(input_text)
    tokens_str = ",".join(tokens)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO tokens (timestamp, unique_hash, input_text, tokens, embeddings) VALUES (?, ?, ?, ?, ?)",
                       (timestamp, unique_hash, input_text, tokens_str, embeddings.tobytes()))
        conn.commit()
        print(f"Dados inseridos com sucesso para o hash: {unique_hash}")
    except sqlite3.IntegrityError:
        print(f"Entrada com hash '{unique_hash}' já existe no banco de dados.")
    finally:
        conn.close()


def main():
    input_text = input("Insira o texto: ")
    tokens, embeddings = analyze_bert(input_text)
    create_database()
    insert_data(input_text, tokens, embeddings)


if __name__ == "__main__":
    import torch
    main()

# ----HERMES----
