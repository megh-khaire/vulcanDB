import pytest

from vulcan.testers.constraint import count_constraints


# Test data setup for different scenarios
@pytest.mark.parametrize(
    "sql_query, expected",
    [
        # Single Column Constraints
        (
            "CREATE TABLE Employees (ID int PRIMARY KEY)",
            {
                "primary_key": 1,
                "foreign_key": 0,
                "unique": 0,
                "check": 0,
                "not_null": 0,
                "default": 0,
            },
        ),
        (
            "CREATE TABLE Employees (ID int NOT NULL)",
            {
                "primary_key": 0,
                "foreign_key": 0,
                "unique": 0,
                "check": 0,
                "not_null": 1,
                "default": 0,
            },
        ),
        (
            "CREATE TABLE Employees (ID int UNIQUE)",
            {
                "primary_key": 0,
                "foreign_key": 0,
                "unique": 1,
                "check": 0,
                "not_null": 0,
                "default": 0,
            },
        ),
        (
            "CREATE TABLE Employees (ID int DEFAULT 1)",
            {
                "primary_key": 0,
                "foreign_key": 0,
                "unique": 0,
                "check": 0,
                "not_null": 0,
                "default": 1,
            },
        ),
        # Multiple Column Constraints
        (
            "CREATE TABLE Employees (ID int PRIMARY KEY, Name varchar(100) UNIQUE)",
            {
                "primary_key": 1,
                "foreign_key": 0,
                "unique": 1,
                "check": 0,
                "not_null": 0,
                "default": 0,
            },
        ),
        # Combined Column Constraints
        (
            "CREATE TABLE Employees (ID int PRIMARY KEY NOT NULL UNIQUE DEFAULT 0)",
            {
                "primary_key": 1,
                "foreign_key": 0,
                "unique": 1,
                "check": 0,
                "not_null": 1,
                "default": 1,
            },
        ),
        # Table-Level Constraints
        (
            "CREATE TABLE Employees (ID int, CONSTRAINT fk_ID FOREIGN KEY (ID) REFERENCES Managers(ID), CHECK (ID > 0))",
            {
                "primary_key": 0,
                "foreign_key": 1,
                "unique": 0,
                "check": 1,
                "not_null": 0,
                "default": 0,
            },
        ),
        # Mixed Constraints
        (
            "CREATE TABLE Employees (ID int PRIMARY KEY, Name varchar(100), CONSTRAINT fk_Name FOREIGN KEY (Name) REFERENCES Departments(Name))",
            {
                "primary_key": 1,
                "foreign_key": 1,
                "unique": 0,
                "check": 0,
                "not_null": 0,
                "default": 0,
            },
        ),
        # No Constraints
        (
            "CREATE TABLE Employees (ID int, Name varchar(100))",
            {
                "primary_key": 0,
                "foreign_key": 0,
                "unique": 0,
                "check": 0,
                "not_null": 0,
                "default": 0,
            },
        ),
        # Multiple CHECK Constraints
        (
            "CREATE TABLE Employees (ID int CHECK (ID > 0), Age int CHECK (Age >= 18))",
            {
                "primary_key": 0,
                "foreign_key": 0,
                "unique": 0,
                "check": 2,
                "not_null": 0,
                "default": 0,
            },
        ),
        # Multiple FOREIGN KEY Constraints
        (
            "CREATE TABLE Employees (ManagerID int, DepartmentID int, CONSTRAINT fk_Manager FOREIGN KEY (ManagerID) REFERENCES Managers(ID), CONSTRAINT fk_Department FOREIGN KEY (DepartmentID) REFERENCES Departments(ID))",
            {
                "primary_key": 0,
                "foreign_key": 2,
                "unique": 0,
                "check": 0,
                "not_null": 0,
                "default": 0,
            },
        ),
        # Multiple NOT NULL Constraints
        (
            "CREATE TABLE Employees (ID int NOT NULL, Name varchar(100) NOT NULL, Age int NOT NULL)",
            {
                "primary_key": 0,
                "foreign_key": 0,
                "unique": 0,
                "check": 0,
                "not_null": 3,
                "default": 0,
            },
        ),
        # Multiple UNIQUE Constraints
        (
            "CREATE TABLE Employees (ID int UNIQUE, Email varchar(100) UNIQUE)",
            {
                "primary_key": 0,
                "foreign_key": 0,
                "unique": 2,
                "check": 0,
                "not_null": 0,
                "default": 0,
            },
        ),
        # Multiple DEFAULT Constraints
        (
            "CREATE TABLE Employees (ID int DEFAULT 1, Age int DEFAULT 18, Salary decimal DEFAULT 50000)",
            {
                "primary_key": 0,
                "foreign_key": 0,
                "unique": 0,
                "check": 0,
                "not_null": 0,
                "default": 3,
            },
        ),
    ],
)
def test_count_constraints(sql_query, expected):
    assert count_constraints(sql_query) == expected
