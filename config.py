import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw")

DATABASE = {
    "host": "localhost",
    "port": 5432,
    "database": "waymark",
    "user": "postgres",
    "password": "postgres"
}