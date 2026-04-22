import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "stellar.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS sessoes (
            id        TEXT PRIMARY KEY,
            criada_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS historico (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            sessao_id TEXT NOT NULL,
            autor     TEXT NOT NULL CHECK(autor IN ('user', 'bot')),
            mensagem  TEXT NOT NULL,
            tag       TEXT,
            criada_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sessao_id) REFERENCES sessoes(id)
        );
    """)
    conn.commit()
    conn.close()
