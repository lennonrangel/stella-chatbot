import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "stellar.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    _create_tables(conn)
    _seed_curiosidades(conn)
    conn.close()


def _create_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS sessoes (
            id          TEXT PRIMARY KEY,
            criada_em   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS historico (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            sessao_id   TEXT NOT NULL,
            autor       TEXT NOT NULL CHECK(autor IN ('user', 'bot')),
            mensagem    TEXT NOT NULL,
            tag         TEXT,
            criada_em   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sessao_id) REFERENCES sessoes(id)
        );

        CREATE TABLE IF NOT EXISTS curiosidades (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            tema        TEXT NOT NULL,
            texto       TEXT NOT NULL
        );
    """)
    conn.commit()


def _seed_curiosidades(conn):
    cursor = conn.execute("SELECT COUNT(*) FROM curiosidades")
    total = cursor.fetchone()[0]

    # Só insere se o banco estiver vazio (evita duplicatas)
    if total > 0:
        return

    curiosidades = [
        ("geral", "A luz do Sol que vemos é do passado: ela leva pouco mais de 8 minutos para chegar até nós."),
        ("geral", "O universo tem cerca de 13,8 bilhões de anos e continua em expansão desde o Big Bang."),
        ("geral", "O universo é composto por aproximadamente 68% de energia escura, 27% de matéria escura e apenas 5% de matéria comum."),
        ("geral", "A cada segundo, aproximadamente 275 milhões de estrelas surgem em todo o universo observável."),
        ("estrelas", "Você é literalmente feito de poeira de estrelas — os átomos do seu corpo foram forjados em supernovas."),
        ("estrelas", "Existem mais estrelas no universo do que grãos de areia em todas as praias da Terra."),
        ("planetas", "Um dia em Vênus é mais longo que um ano em Vênus — ele gira mais devagar do que orbita o Sol."),
        ("planetas", "Saturno tem densidade tão baixa que flutuaria na água, se houvesse um oceano grande o suficiente."),
        ("buraco_negro", "O buraco negro M87* fotografado em 2019 tem 6,5 bilhões de vezes a massa do Sol."),
        ("galaxias", "A Via Láctea e Andrômeda vão colidir em cerca de 4,5 bilhões de anos."),
    ]

    conn.executemany(
        "INSERT INTO curiosidades (tema, texto) VALUES (?, ?)",
        curiosidades
    )
    conn.commit()