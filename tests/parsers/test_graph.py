import pytest

from vulcan.parsers.graph import get_table_creation_order

test_data = [
    # Simple linear dependency
    (
        {"TableA": [], "TableB": ["TableA"], "TableC": ["TableB"]},
        ["TableA", "TableB", "TableC"],
    ),
    # Complex dependency
    (
        {
            "TableA": [],
            "TableB": ["TableA"],
            "TableC": ["TableB", "TableA"],
            "TableD": ["TableC"],
        },
        ["TableA", "TableB", "TableC", "TableD"],
    ),
    # Independent tables
    ({"TableA": [], "TableB": [], "TableC": []}, ["TableA", "TableB", "TableC"]),
    # Circular dependency (should raise exception)
    ({"TableA": ["TableB"], "TableB": ["TableA"]}, ValueError),
]


@pytest.mark.parametrize("dependencies,expected", test_data)
def test_set_query_execution_order(dependencies, expected):
    if expected is ValueError:
        with pytest.raises(ValueError):
            get_table_creation_order(dependencies)
    else:
        result = get_table_creation_order(dependencies)
        assert result == expected or set(result) == set(
            expected
        ), f"Expected {expected} but got {result}"
