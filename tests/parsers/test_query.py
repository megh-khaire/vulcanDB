import pytest

from vulcan.parsers.query import parse_sql_query

test_cases = [
    {
        "query": "CREATE TABLE Employees (Id INT, Name VARCHAR(100), ManagerId INT, FOREIGN KEY (ManagerId) REFERENCES Managers(Id))",
        "expected_output": {
            "table_name": "Employees",
            "columns": ["Id", "Name", "ManagerId"],
            "foreign_keys": ["Managers"],
        },
    },
    {
        "query": "CREATE TABLE Departments (Id INT, DepartmentName VARCHAR(100), FOREIGN KEY (DepartmentId) REFERENCES Departments(Id), FOREIGN KEY (ManagerId) REFERENCES Managers(Id))",
        "expected_output": {
            "table_name": "Departments",
            "columns": ["Id", "DepartmentName"],
            "foreign_keys": ["Departments", "Managers"],
        },
    },
]


@pytest.mark.parametrize("case", test_cases)
def test_sql_parser(case):
    output = parse_sql_query(case["query"])
    expected_output = case["expected_output"]
    assert (
        output["name"] == expected_output["table_name"]
    ), f"Table name mismatch: {output['name']} != {expected_output['table_name']}"
    assert set(output["columns"]) == set(
        expected_output["columns"]
    ), f"Column mismatch: {output['columns']} != {expected_output['columns']}"
    assert set(output["foreign_keys"]) == set(
        expected_output["foreign_keys"]
    ), f"Foreign keys mismatch: {output['foreign_keys']} != {expected_output['foreign_keys']}"
