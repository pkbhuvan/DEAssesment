from sqlalchemy import text
from src.database.connection import engine
from src.utils.logger import logger


def create_tables():

    with open("src/database/schema.sql", "r") as file:
        sql = file.read()

    with engine.connect() as connection:

        connection.execute(text(sql))
        connection.commit()

    logger.info("Database tables created successfully.")