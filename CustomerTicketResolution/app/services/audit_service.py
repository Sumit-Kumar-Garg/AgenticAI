
import sqlite3
from datetime import datetime, timezone

DB_PATH = "data/support.db"


def initialize_audit_table():
    connection = sqlite3.connect(DB_PATH)

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS human_review_audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT NOT NULL,
                thread_id TEXT NOT NULL UNIQUE,
                reviewer TEXT NOT NULL,
                approved INTEGER NOT NULL,
                comment TEXT,
                final_status TEXT NOT NULL,
                decision_timestamp TEXT NOT NULL
            )
        """)

        connection.commit()

    finally:
        connection.close()


def save_human_review(
    ticket_id: str,
    thread_id: str,
    reviewer: str,
    approved: bool,
    comment: str,
    final_status: str
):
    connection = sqlite3.connect(DB_PATH)

    timestamp = datetime.now(timezone.utc).isoformat()

    try:
        connection.execute("""
            INSERT OR IGNORE INTO human_review_audit (
                ticket_id,
                thread_id,
                reviewer,
                approved,
                comment,
                final_status,
                decision_timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            ticket_id,
            thread_id,
            reviewer,
            int(approved),
            comment,
            final_status,
            timestamp
        ))

        connection.commit()

    finally:
        connection.close()


def get_review_audit(ticket_id: str):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    try:
        rows = connection.execute("""
            SELECT *
            FROM human_review_audit
            WHERE ticket_id = ?
            ORDER BY decision_timestamp DESC
        """, (ticket_id,)).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()
