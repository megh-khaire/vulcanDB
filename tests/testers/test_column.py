import pandas as pd
import pytest
from vulcan.testers.column import get_missing_columns


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame(
        {"column1": range(10), "column2": range(10, 20), "column3": range(20, 30)}
    )


# Test a single CREATE query that includes all DataFrame columns
def test_single_create_query_all_columns(sample_dataframe):
    queries = ["CREATE TABLE new_table (column1 INT, column2 INT, column3 INT)"]
    assert not get_missing_columns(queries, sample_dataframe)


# Test multiple CREATE queries, each creating a table with one of the DataFrame columns
def test_multiple_create_queries_all_columns(sample_dataframe):
    queries = [
        "CREATE TABLE table1 (column1 INT)",
        "CREATE TABLE table2 (column2 INT)",
        "CREATE TABLE table3 (column3 INT)",
    ]
    assert not get_missing_columns(queries, sample_dataframe)


# Parameterized tests to check various scenarios
@pytest.mark.parametrize(
    "queries, expected_missing",
    [
        (["CREATE TABLE table1 (column1 INT)"], {"column2", "column3"}),
        (["CREATE TABLE table4 (column4 INT)"], {"column1", "column2", "column3"}),
        (["CREATE TABLE table5 (column1 INT, column4 INT)"], {"column2", "column3"}),
    ],
)
def test_create_queries_with_expected_missing_columns(
    sample_dataframe, queries, expected_missing
):
    """Test CREATE queries with expected missing columns."""
    missing_columns = get_missing_columns(queries, sample_dataframe)
    assert missing_columns == expected_missing


# Test behavior when DataFrame is empty
def test_empty_dataframe_create_query():
    """Test behavior with an empty DataFrame using CREATE query."""
    df = pd.DataFrame()
    queries = ["CREATE TABLE table1 (column1 INT)"]
    assert not get_missing_columns(queries, df)
