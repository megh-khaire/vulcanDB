# Replace with the actual import path
from vulcan.db.setup import setup_and_populate_db

# Test case with SQL queries as input


def test_setup_and_populate_db():
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
        # More queries can be added here for testing
    ]

    success, error = setup_and_populate_db(db_file_path, sql_queries)

    assert success, f"Database setup failed with error: {error}"

# Negative test case to ensure unique constraint on email is enforced


def test_setup_and_populate_db_failure():
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
        # Intentional duplicate
        "INSERT INTO users (name, email) VALUES ('Duplicate Alice', 'alice.smith@example.com');",
    ]

    success, error = setup_and_populate_db(db_file_path, sql_queries)

    assert not success, "The function should have failed due to a unique constraint violation."
    assert "UNIQUE constraint failed" in error, f"Expected a unique constraint error, but got: {error}"
