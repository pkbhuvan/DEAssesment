from sqlalchemy import create_engine

DATABASE_URL = (
    "postgresql://postgres:postgres@localhost:5432/waymark"
)

engine = create_engine(DATABASE_URL)