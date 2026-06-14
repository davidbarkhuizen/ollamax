```markdown
# dicts_to_table.py

def dicts_to_table(list_of_dicts):
    if not list_of_dicts:
        return ""

    headers = list_of_dicts[0].keys()
    rows = [headers]

    for dictionary in list_of_dicts:
        rows.append(dictionary.values())

    table = []
    for row in rows:
        table.append("| " + " | ".join(map(str, row)) + " |")

    header_separator = "| " + " | ".join(["---"] * len(headers)) + " |"
    table.insert(1, header_separator)

    return "\n".join(table)
```

```markdown
# test_dicts_to_table.py

import unittest

class TestDictsToTable(unittest.TestCase):
    def test_basic_functionality(self):
        list_of_dicts = [
            {"Name": "Alice", "Age": 30, "City": "New York"},
            {"Name": "Bob", "Age": 25, "City": "Los Angeles"}
        ]
        expected_output = (
            "| Name  | Age | City        |\n"
            "| ---   | --- | ----------- |\n"
            "| Alice | 30  | New York    |\n"
            "| Bob   | 25  | Los Angeles |"
        )
        self.assertEqual(dicts_to_table(list_of_dicts), expected_output)

    def test_empty_list(self):
        list_of_dicts = []
        expected_output = ""
        self.assertEqual(dicts_to_table(list_of_dicts), expected_output)

if __name__ == "__main__":
    unittest.main()
```