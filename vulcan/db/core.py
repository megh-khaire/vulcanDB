import os
from typing import List, Optional, Tuple

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


def initialize_database(db_uri: str) -> create_engine:
    """
    Initializes a database engine.

    :param db_uri: Database URI for connection, e.g., 'sqlite:///example.db' for SQLite.
    :return: SQLAlchemy Engine instance.
    """
    engine = create_engine(db_uri, echo=True, future=True)
    return engine


def execute_queries(
    engine: create_engine, queries: List[str]
) -> Tuple[bool, Optional[str]]:
    """
    Executes a list of SQL queries using the given engine.

    :param engine: SQLAlchemy Engine instance.
    :param queries: List of SQL query strings to be executed.
    :return: Tuple of success flag and error message (if any).
    """
    with engine.connect() as conn:
        try:
            for query in queries:
                conn.execute(text(query))
            conn.commit()
            return True, None
        except SQLAlchemyError as e:
            return False, str(e)


def delete_database(db_file: str):
    """
    Deletes the database file if it exists.

    :param db_file: The file path of the database to delete.
    """
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Deleted existing database file: {db_file}")
    else:
        print("Database file does not exist, no need to delete.")


def setup_and_populate_db(db_file_path: str, sql_queries: list[str]):
    delete_database(db_file_path)
    engine = initialize_database(f"sqlite:///{db_file_path}")
    return execute_queries(engine, sql_queries)
