from sqlalchemy import text
from src.database.connection import engine
from src.utils.logger import logger


def create_tables():
    with open("src/database/schema.sql", "r") as file:
        sql = file.read()

    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()

    logger.info("Database tables created successfully.")