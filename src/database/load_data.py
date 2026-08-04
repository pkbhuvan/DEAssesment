from src.database.connection import engine
from src.utils.logger import logger


def load_dataframe(df, table_name):
    """
    Load any DataFrame into the specified PostgreSQL table.
    """

    try:
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",
            index=False
        )

        logger.info(f"{table_name} loaded successfully.")

    except Exception:
        logger.exception(f"Failed to load {table_name}.")
        raise