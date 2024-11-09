import os
import psycopg2

# Чтение данных подключения из переменных окружения
DB_NAME = os.getenv("railway")
DB_USER = os.getenv("postgres")
DB_PASSWORD = os.getenv("AhqmIlJgfwxlWfnKVWdZLmjcEGEGLKKl")
DB_HOST = os.getenv("postgres.railway.internal")
DB_PORT = os.getenv("5432")

# Подключение к базе данных
def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# Создание таблицы для хранения данных о драфте
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS drafts (
                        id SERIAL PRIMARY KEY,
                        match_date TIMESTAMP,
                        blue_side_draft TEXT,
                        red_side_draft TEXT,
                        team_name TEXT,
                        opponent_team TEXT,
                        game_duration TEXT,
                        win_or_loss TEXT
                    )''')
    conn.commit()
    cursor.close()
    conn.close()

# Вызов создания таблицы при запуске
create_table()
