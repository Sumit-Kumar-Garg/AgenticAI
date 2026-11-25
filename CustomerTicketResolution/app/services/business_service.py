
import sqlite3

DB_PATH = "data/support.db"


def get_connection():

    connection = sqlite3.connect(DB_PATH)

    # Return rows as dictionary-like objects
    connection.row_factory = sqlite3.Row

    return connection


def get_tickets(status=None, limit=100):
    connection = get_connection()

    try:
        query = """
            SELECT
                t.ticket_id,
                t.customer_id,
                c.name AS customer_name,
                t.booking_id,
                t.description,
                t.priority,
                t.status
            FROM tickets t
            LEFT JOIN customers c
                ON t.customer_id = c.customer_id
        """

        params = []

        if status and status.upper() != "ALL":
            query += " WHERE UPPER(t.status) = ?"
            params.append(status.upper())

        query += """
            ORDER BY
                CASE UPPER(t.priority)
                    WHEN 'CRITICAL' THEN 1
                    WHEN 'HIGH' THEN 2
                    WHEN 'MEDIUM' THEN 3
                    ELSE 4
                END,
                t.ticket_id DESC
            LIMIT ?
        """

        params.append(limit)

        rows = connection.execute(
            query,
            params
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


def get_customer(customer_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT customer_id, name, email
            FROM customers
            WHERE customer_id = ?
            """,
            (customer_id,)
        )

        row = cursor.fetchone()

        return dict(row) if row else None

    finally:
        connection.close()


def get_booking(booking_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                b.booking_id,
                b.customer_id,
                b.hotel_id,
                h.name AS hotel_name,
                h.location,
                b.status AS booking_status,
                b.amount
            FROM bookings b
            LEFT JOIN hotels h
                ON b.hotel_id = h.hotel_id
            WHERE b.booking_id = ?
            """,
            (booking_id,)
        )

        row = cursor.fetchone()

        return dict(row) if row else None

    finally:
        connection.close()


def get_ticket(ticket_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                t.ticket_id,
                t.customer_id,
                c.name AS customer_name,
                t.booking_id,
                t.description,
                t.priority,
                t.status
            FROM tickets t
            LEFT JOIN customers c
                ON t.customer_id = c.customer_id
            WHERE t.ticket_id = ?
            """,
            (ticket_id,)
        )

        row = cursor.fetchone()

        return dict(row) if row else None

    finally:
        connection.close()


def get_customer_tickets(customer_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                ticket_id,
                booking_id,
                description,
                priority,
                status
            FROM tickets
            WHERE customer_id = ?
            ORDER BY ticket_id
            """,
            (customer_id,)
        )

        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()
