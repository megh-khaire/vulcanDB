import pytest
from vulcan.generators.query import validate_sql_query


def test_valid_select_query():
    query = "SELECT * FROM users"
    is_valid, errors = validate_sql_query(query)
    assert is_valid == True
    assert errors == []


def test_invalid_syntax():
    query = "SELEC * FROM users"  # Misspelled SELECT
    is_valid, errors = validate_sql_query(query)
    assert is_valid == False
    assert len(errors) > 0


def test_valid_insert_query():
    query = "INSERT INTO users (id, name) VALUES (1, 'John')"
    is_valid, errors = validate_sql_query(query)
    assert is_valid == True
    assert errors == []


def test_empty_query():
    query = ""
    is_valid, errors = validate_sql_query(query)
    assert is_valid == False
    assert len(errors) > 0
