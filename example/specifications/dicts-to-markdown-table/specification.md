## specification

convert list of python dictionaries to markdown table string

### inputs

- takes a `list[dict[str, str]]` as an argument

#### input validation

- in the case of being sent an empty list, then return an empty string
- check that all the dictionaries in the list have the same keys
  * otherwise raise a ValueError() exception
- raise a ValueError exception if a dictionary item key of None is encountered

### outputs

return a single multiline string that corresponds to a table in markdown format

### markdown table format specification

Markdown tables structure data using pipe character (|) to separate columns and a row of three hyphens (---) to define the header.  This syntax is part of GitHub-Flavored Markdown (GFM) and is widely supported in documentation, wikis, and README files.

Basic Syntax To create a simple table, place headers in the first row, followed by a separator line, and then the data rows. Pipes are required at the start and end of each line for clarity

### example of basic syntax for markdown tables

| Name    | Age | City       |
|---------|-----|------------|
| Alice   | 25  | New York   |
| Bob     | 30  | London     |


### text alignment in markdown tables

Text Alignment You can control column alignment using colons (:) in the separator row. A colon on the left aligns text left, on the right aligns right, and on both sides centers the text.

#### example of text alignment in markdown tables

| Left  | Center | Right |
|:------|:------:|------:|
| Data1 | Data2  | Data3 |
| Data4 | Data5  | Data6 |
