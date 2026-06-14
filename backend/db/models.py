from backend.db.database import get_connection


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


def buscar_ultimo_tema(sessao_id: str):
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


def buscar_historico_recente(sessao_id: str, limite: int = 6) -> list[dict]:
    """Recupera as últimas mensagens para dar memória real à Stella."""
    conn = get_connection()
    cur = conn.execute("""
        SELECT autor, mensagem FROM historico
        WHERE sessao_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (sessao_id, limite))
    rows = cur.fetchall()
    conn.close()
    return [{"role": r["autor"], "content": r["mensagem"]} for r in reversed(rows)]
