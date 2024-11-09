import streamlit as st
import pandas as pd
import db_setup  # Импортируем файл db_setup для подключения к базе данных

# Функция для загрузки данных из базы
def load_data():
    conn = db_setup.get_db_connection()
    query = "SELECT match_date, blue_side_draft, red_side_draft, opponent_team, game_duration, win_or_loss FROM drafts"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Streamlit интерфейс
st.title("История игр: Драфты")
st.write("Загрузка данных из базы данных PostgreSQL:")

# Загружаем данные и отображаем в Streamlit
data = load_data()
st.dataframe(data)
