from vulcan.validators.query import validate_sql_query


def test_valid_select_query():
    query = "SELECT * FROM users"
    is_valid, errors = validate_sql_query(query)
    assert is_valid is True
    assert errors == []


def test_invalid_syntax():
    # Misspelled SELECT
    query = "SELEC * FROM users"
    is_valid, errors = validate_sql_query(query)
    assert is_valid is False


def test_valid_insert_query():
    query = "INSERT INTO users (id, name) VALUES (1, 'John')"
    is_valid, errors = validate_sql_query(query)
    assert is_valid is True, "The query should be valid."
    assert errors == [], f"Expected no errors, but got: {errors}"


def test_empty_query():
    query = ""
    is_valid, errors = validate_sql_query(query)
    assert is_valid is False
