import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

from vulcan.database.core import execute_queries, initialize_database, reset_database

table_order = ["users", "posts", "friendships"]
tables = {
    "users": {
        "name": "users",
        "query": """CREATE TABLE users (
user_id INT PRIMARY KEY,
username VARCHAR(255) NOT NULL UNIQUE,
email VARCHAR(255) NOT NULL UNIQUE,
password_hash CHAR(64) NOT NULL,
bio TEXT,
profile_picture_url VARCHAR(255),
created_at TIMESTAMP
);""",
    },
    "posts": {
        "name": "posts",
        "query": """CREATE TABLE posts (
post_id INT PRIMARY KEY,
user_id INT,
content TEXT NOT NULL,
image_url VARCHAR(255),
created_at TIMESTAMP,
FOREIGN KEY (user_id) REFERENCES users(user_id)
);""",
    },
    "friendships": {
        "name": "friendships",
        "query": """CREATE TABLE friendships (
friendship_id INT PRIMARY KEY,
requester_id INT,
addressee_id INT,
status TEXT NOT NULL,
created_at TIMESTAMP,
FOREIGN KEY (requester_id) REFERENCES users(user_id),
FOREIGN KEY (addressee_id) REFERENCES users(user_id)
);""",
    },
}


@pytest.fixture(scope="function")
def db_engine():
    db_uri = "sqlite:///output/test.db"
    engine = initialize_database(db_uri)
    yield engine
    reset_database(engine)
    engine.dispose()


def execute_queries_safe(engine, table_order, tables):
    try:
        return execute_queries(engine, table_order, tables)
    except Exception as e:
        return False, e


def test_setup_and_populate_db(db_engine):
    status, error = execute_queries_safe(db_engine, table_order, tables)
    assert status, "The database setup and population should succeed without errors."
    assert error is None, "There should be no error."


def test_setup_and_populate_db_failure(db_engine):
    # Ensure tables are created in a potentially incorrect order.
    table_order_incorrect = ["posts", "users", "friendships"]
    status, _ = execute_queries_safe(db_engine, table_order_incorrect, tables)

    assert status

    # Attempt to insert data that violates foreign key constraints.
    with db_engine.connect() as conn:
        try:
            conn.execute(text("PRAGMA foreign_keys=ON"))
            conn.execute(
                text(
                    "INSERT INTO posts (user_id, content) VALUES (1, 'This should fail')"
                )
            )
            violated = False
        except IntegrityError:
            violated = True

    assert violated, "Foreign key constraints are not being enforced as expected."
