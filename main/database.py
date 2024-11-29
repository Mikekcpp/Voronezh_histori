import sqlite3


def create_database():
    # Создание базы данных с пользователями и вопросами
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS writers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            book TEXT,
            year INTEGER
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT,
            password TEXT,
            score INTEGER
        )
    """
    )

    cursor.execute(
        """
        DROP TABLE IF EXISTS questions
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY,
            question TEXT,
            answer TEXT,
            difficulty INTEGER,
            score INTEGER
        )
    """
    )

    # Добавление вопросов в базу данных
    questions = [
        ("Кто написал роман 'Война и мир'?", "Лев Толстой", 1, 10),
        ("Кто написал роман 'Преступление и наказание'?", "Федор Достоевский", 1, 10),
        ("Кто написал роман 'Анна Каренина'?", "Лев Толстой", 1, 10),
        ("Кто написал роман 'Братья Карамазовы'?", "Федор Достоевский", 1, 10),
        ("Кто написал роман 'Воскресение'?", "Лев Толстой", 1, 10),
        # Добавьте еще вопросы...
    ]

    for question, answer, difficulty, score in questions:
        cursor.execute("INSERT OR IGNORE INTO questions (question, answer, difficulty, score) VALUES (?, ?, ?, ?)",
                       (question, answer, difficulty, score))

    conn.commit()
    conn.close()
