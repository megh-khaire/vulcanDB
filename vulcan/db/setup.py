from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Tuple, Optional
from vulcan.db.delete_db import delete_database


def initialize_database(db_uri: str) -> create_engine:
    """
    Initializes a database engine.

    :param db_uri: Database URI for connection, e.g., 'sqlite:///example.db' for SQLite.
    :return: SQLAlchemy Engine instance.
    """
    engine = create_engine(db_uri, echo=True, future=True)
    return engine


def execute_queries(engine: create_engine, queries: List[str]) -> Tuple[bool, Optional[str]]:
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
            return True, None  # No errors, successful execution
        except SQLAlchemyError as e:
            return False, str(e)  # Return False and the error message


# Modified function to take SQL queries as input
def setup_and_populate_db(db_file_path: str, sql_queries: list[str]):
    delete_database(db_file_path)

    engine = initialize_database(f'sqlite:///{db_file_path}')

    return execute_queries(engine, sql_queries)


# Example usage
if __name__ == "__main__":
    db_file_path = 'test.db'
    sql_queries = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            CHECK (email LIKE '%_@__%.__%')  -- Simple check for valid email format
        );
        """,
        "INSERT INTO users (name, email) VALUES ('Alice Smith', 'alice.smith@example.com');",
        "INSERT INTO users (name, email) VALUES ('Bob Jones', 'bob.jones@example.com');",
        "INSERT INTO users (name, email) VALUES ('Charlie Brown', 'charlie.brown@example.com');",
        # More queries can be added here
    ]

    success, error = setup_and_populate_db(db_file_path, sql_queries)

    if success:
        print("All queries executed successfully.")
    else:
        print(f"An error occurred: {error}")
