## summary

return a python function called `dicts_to_table`, and any additional helper functions, classes, and modules as required

list_of_dicts_to_table function
- takes a list of string, string dictionaries as an argument
- assume that all the dictionaries in the list have the same keys
- returns a single multiline string that corresponds to a table in markdown format
  * each column should correspond to a dictionary key, and have the key as the column header
  * each row should correspond to the values of a specific dictionary in the list
