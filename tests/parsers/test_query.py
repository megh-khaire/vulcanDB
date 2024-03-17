import pytest

from vulcan.parsers.query import parse_sql_query

test_cases = [
    {
        "query": "CREATE TABLE Employees (Id INT, Name VARCHAR(100), ManagerId INT, FOREIGN KEY (ManagerId) REFERENCES Managers(Id))",
        "expected_output": {"table_name": "Employees", "foreign_keys": ["Managers"]},
    },
    {
        "query": "CREATE TABLE Departments (Id INT, DepartmentName VARCHAR(100), FOREIGN KEY (DepartmentId) REFERENCES Departments(Id), FOREIGN KEY (ManagerId) REFERENCES Managers(Id))",
        "expected_output": {
            "table_name": "Departments",
            "foreign_keys": ["Departments", "Managers"],
        },
    },
]


@pytest.mark.parametrize("case", test_cases)
def test_sql_parser(case):
    table_name, foreign_keys = parse_sql_query(case["query"])
    expected_output = case["expected_output"]
    assert (
        table_name == expected_output["table_name"]
    ), f"Table name mismatch: {table_name} != {expected_output['table_name']}"
    assert sorted(foreign_keys) == sorted(
        expected_output["foreign_keys"]
    ), f"Foreign keys mismatch: {foreign_keys} != {expected_output['foreign_keys']}"
