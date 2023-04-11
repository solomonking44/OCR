from sqlalchemy import create_engine

engine = create_engine("sqlite3:///memory.sqlite3", echo=True)