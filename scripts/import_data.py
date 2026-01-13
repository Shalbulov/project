import pandas as pd
from sqlalchemy import create_engine
import os
import sys

# настройка подключения
if os.environ.get("DOCKER_ENV"):
    DATABASE_URL = "postgresql://postgres:mysecretpassword@db:5432/films_database"
else:
    DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost:5433/films_database"

def process_and_save_data():
    print("===== Запуск скрипта импорта данных =====")
    
    # идет поиск CSV файла
    possible_paths = [
        'data/films.csv',           # внутри docker
        '../data/films.csv',        # если запускать из scripts
        'films.csv'                 # если корне файле
    ]
    
    file_path = None
    for path in possible_paths:
        if os.path.exists(path):
            file_path = path
            break

    if not file_path:
        print(f"Ошибка: Файл films.csv не найден!")
        print(f"Текущая рабочая директория: {os.getcwd()}")
        return

    print(f"Файл найден: {file_path}")

    try:
        # чтение данных
        df = pd.read_csv(file_path)
        print(f"Считано строк из CSV: {len(df)}")
        
        # подключение к базе
        engine = create_engine(DATABASE_URL)
        
        # запись в базу
        df.to_sql('films', engine, if_exists='replace', index=False)
        
        print("Данные успешно импортированы в таблицу 'films'!")
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    process_and_save_data()