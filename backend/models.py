import random
from backend.database import get_connection


def salvar_sessao(sessao_id: str):
    conn = get_connection()
    conn.execute(
        "INSERT OR IGNORE INTO sessoes (id) VALUES (?)",
        (sessao_id,)
    )
    conn.commit()
    conn.close()


def salvar_mensagem(sessao_id: str, autor: str, mensagem: str, tag: str = None):
    conn = get_connection()
    conn.execute(
        "INSERT INTO historico (sessao_id, autor, mensagem, tag) VALUES (?, ?, ?, ?)",
        (sessao_id, autor, mensagem, tag)
    )
    conn.commit()
    conn.close()


def buscar_historico(sessao_id: str, limite: int = 50) -> list:
    conn = get_connection()
    rows = conn.execute(
        """SELECT autor, mensagem, tag, criada_em
           FROM historico
           WHERE sessao_id = ?
           ORDER BY criada_em ASC
           LIMIT ?""",
        (sessao_id, limite)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def buscar_curiosidade_por_tema(tema):
    conn = get_connection()
    cur = conn.execute(
        "SELECT texto FROM curiosidades WHERE tema = ? ORDER BY RANDOM() LIMIT 1",
        (tema,)
    )
    row = cur.fetchone()
    conn.close()
    return row["texto"] if row else None

def buscar_ultimo_tema(sessao_id):
    conn = get_connection()

    cur = conn.execute("""
        SELECT tag FROM historico
        WHERE sessao_id = ? AND autor = 'bot' AND tag IS NOT NULL
        ORDER BY id DESC
        LIMIT 1
    """, (sessao_id,))

    row = cur.fetchone()
    conn.close()

    return row["tag"] if row else None


def curiosidade_aleatoria(tema: str = "geral") -> str:
    conn = get_connection()

    row = conn.execute(
        "SELECT texto FROM curiosidades WHERE tema = ? ORDER BY RANDOM() LIMIT 1",
        (tema,)
    ).fetchone()

    if row is None:
        row = conn.execute(
            "SELECT texto FROM curiosidades ORDER BY RANDOM() LIMIT 1"
        ).fetchone()

    conn.close()
    return row["texto"] if row else "O universo é cheio de mistérios ainda por descobrir!"