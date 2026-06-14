# dicts_to_table.py

```python
def dicts_to_table(list_of_dicts):
    if not list_of_dicts:
        return ""

    # Extract headers from the first dictionary's keys
    headers = list_of_dicts[0].keys()

    # Create the header row
    header_row = "| " + " | ".join(headers) + " |"
    separator_row = "|-" + "-|-".join([""] * len(headers)) + "-|"

    # Create rows for each dictionary
    rows = []
    for d in list_of_dicts:
        row = "| " + " | ".join([str(d[key]) for key in headers]) + " |"
        rows.append(row)

    # Combine all parts into the final table string
    table = header_row + "\n" + separator_row + "\n" + "\n".join(rows)
    return table

# Helper function to test the output of dicts_to_table
def test_dicts_to_table():
    data = [
        {"name": "Alice", "age": 30, "city": "New York"},
        {"name": "Bob", "age": 25, "city": "Los Angeles"},
        {"name": "Charlie", "age": 35, "city": "Chicago"}
    ]
    
    expected_output = """| name   | age | city      |
|--------|-----|-----------|
| Alice  | 30  | New York  |
| Bob    | 25  | Los Angeles |
| Charlie| 35  | Chicago   |"""

    result = dicts_to_table(data)
    assert result.strip() == expected_output.strip(), f"Expected:\n{expected_output}\nGot:\n{result}"

if __name__ == "__main__":
    test_dicts_to_table()
```

# README.md

```markdown
# dicts_to_table

This module provides a function `dicts_to_table` that converts a list of dictionaries into a markdown formatted table.

## Usage

```python
from dicts_to_table import dicts_to_table

data = [
    {"name": "Alice", "age": 30, "city": "New York"},
    {"name": "Bob", "age": 25, "city": "Los Angeles"},
    {"name": "Charlie", "age": 35, "city": "Chicago"}
]

table = dicts_to_table(data)
print(table)
```

## Testing

To run the tests, execute the `dicts_to_table.py` script directly:

```sh
python dicts_to_table.py
```


| name | age | city |
|--|--|--|
| Alice | 30 | New York |
| Bob | 25 | Los Angeles |
| Charlie | 35 | Chicago |
