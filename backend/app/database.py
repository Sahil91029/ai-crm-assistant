import sqlite3
from pathlib import Path

# =====================================================
# Database Configuration
# =====================================================

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "crm.db"


# =====================================================
# Get Connection
# =====================================================

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# =====================================================
# Create Table
# =====================================================

def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interactions (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        hcp_name TEXT,

        interaction_type TEXT,

        interaction_date TEXT,

        interaction_time TEXT,

        attendees TEXT,

        topics TEXT,

        materials TEXT,

        samples TEXT,

        sentiment TEXT,

        outcome TEXT,

        follow_up TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()


# =====================================================
# Insert Interaction
# =====================================================

def save_interaction(form):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO interactions (

            hcp_name,
            interaction_type,
            interaction_date,
            interaction_time,
            attendees,
            topics,
            materials,
            samples,
            sentiment,
            outcome,
            follow_up

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            form.get("hcpName", ""),
            form.get("interactionType", ""),
            form.get("date", ""),
            form.get("time", ""),
            form.get("attendees", ""),
            form.get("topics", ""),
            form.get("materials", ""),
            form.get("samples", ""),
            form.get("sentiment", ""),
            form.get("outcome", ""),
            form.get("followUp", ""),
        ),
    )

    conn.commit()

    interaction_id = cursor.lastrowid

    conn.close()

    return interaction_id


# =====================================================
# Update Interaction
# =====================================================

def update_interaction(interaction_id, form):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE interactions
        SET

            hcp_name=?,
            interaction_type=?,
            interaction_date=?,
            interaction_time=?,
            attendees=?,
            topics=?,
            materials=?,
            samples=?,
            sentiment=?,
            outcome=?,
            follow_up=?

        WHERE id=?
        """,
        (
            form.get("hcpName", ""),
            form.get("interactionType", ""),
            form.get("date", ""),
            form.get("time", ""),
            form.get("attendees", ""),
            form.get("topics", ""),
            form.get("materials", ""),
            form.get("samples", ""),
            form.get("sentiment", ""),
            form.get("outcome", ""),
            form.get("followUp", ""),
            interaction_id,
        ),
    )

    conn.commit()

    conn.close()


# =====================================================
# Search by Doctor Name
# =====================================================

def search_hcp(hcp_name):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM interactions
        WHERE LOWER(hcp_name)
        LIKE LOWER(?)
        ORDER BY id DESC
        """,
        (f"%{hcp_name}%",),
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# =====================================================
# Get All Interactions
# =====================================================

def get_all_interactions():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM interactions
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# =====================================================
# Delete Interaction
# =====================================================

def delete_interaction(interaction_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM interactions
        WHERE id=?
        """,
        (interaction_id,),
    )

    conn.commit()

    conn.close()