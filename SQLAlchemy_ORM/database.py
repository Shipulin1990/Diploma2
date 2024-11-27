from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Настройте строку подключения к вашей базе данных
DATABASE_URI = 'postgresql+psycopg2://user:password@localhost/university_db'

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

