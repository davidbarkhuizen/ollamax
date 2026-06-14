## specification of expected behaviour

### summary

write python code to achieve the following desire behaviour

#### inputs

- file path to a source markdown document
  * in the form of a string
- folder path to a destination folder to write the extracted code files to 
  * in the form of a string

### processing

- load the source markdown document from the local file system
- scan through the document, identifying all markdown code sections
- for each markdown code section identified
  * check if that section is immediately preceded (previous line) by a file path marker (format defined below)
    - in the positive case
      * write the contents of the code section to the local file system at the destination folder
        - use the file path in the associated file path marker as a relative path
        - check that the relative path does not refer to a location that is actually a parent folder to the destination folder through containing one or more `..` entries 
    - in the negative case
      * continue with the loop

#### file path marker example

what follows is an example of file path marker immediately preceding a section of markdown code in a source markdown file, where the file path marker corresponds to a relative file path of `src/dicts_to_table.py`, and a filename of `dicts_to_table.py`

**`src/dicts_to_table.py`**
```python
def divide_by_zero(n: int) -> int:
    return n / 0
```

### outputs

a list of the destination paths of the successfully extracted files
