import sqlite3
import hashlib
from pathlib import Path


DB_FOLDER = Path("data")
DB_FOLDER.mkdir(exist_ok=True)

DB_NAME = DB_FOLDER / "studyvision.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    # USERS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # SUBJECTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # STUDY HISTORY
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            subject TEXT,
            question TEXT,
            answer TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # QUIZ RESULTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            topic TEXT,
            score INTEGER,
            total INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # DOCUMENTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT,
            subject TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    connection.commit()
    connection.close()


def register_user(name, email, password):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users(name, email, password)
            VALUES (?, ?, ?)
            """,
            (
                name,
                email,
                hash_password(password)
            )
        )

        connection.commit()

        user_id = cursor.lastrowid

        connection.close()

        return True, user_id

    except sqlite3.IntegrityError:

        connection.close()

        return False, None


def login_user(email, password):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, email
        FROM users
        WHERE email = ? AND password = ?
        """,
        (
            email,
            hash_password(password)
        )
    )

    user = cursor.fetchone()

    connection.close()

    return user


def add_subject(user_id, subject):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO subjects(user_id, name)
        VALUES (?, ?)
        """,
        (user_id, subject)
    )

    connection.commit()
    connection.close()


def get_subjects(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name
        FROM subjects
        WHERE user_id = ?
        ORDER BY name
        """,
        (user_id,)
    )

    subjects = cursor.fetchall()

    connection.close()

    return subjects


def save_history(
    user_id,
    subject,
    question,
    answer
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO study_history(
            user_id,
            subject,
            question,
            answer
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            subject,
            question,
            answer
        )
    )

    connection.commit()
    connection.close()


def get_history(user_id, limit=20):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT subject, question, answer, created_at
        FROM study_history
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (user_id, limit)
    )

    history = cursor.fetchall()

    connection.close()

    return history


def save_quiz_result(
    user_id,
    topic,
    score,
    total
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO quiz_results(
            user_id,
            topic,
            score,
            total
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            topic,
            score,
            total
        )
    )

    connection.commit()
    connection.close()


def get_quiz_results(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT topic, score, total, created_at
        FROM quiz_results
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,)
    )

    results = cursor.fetchall()

    connection.close()

    return results


def save_document(
    user_id,
    filename,
    subject,
    content
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO documents(
            user_id,
            filename,
            subject,
            content
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            filename,
            subject,
            content
        )
    )

    connection.commit()
    connection.close()


def get_documents(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, filename, subject, content, created_at
        FROM documents
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,)
    )

    documents = cursor.fetchall()

    connection.close()

    return documents