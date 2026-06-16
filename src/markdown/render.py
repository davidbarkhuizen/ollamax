from dataclasses import dataclass
from enum import Enum

from rich.markdown import Markdown

from markdown.model import DEFAULT_LANGUAGE_MARKER, FileExtensionsForLanguageMarker, LanguageMarker
from model.model import TextFile


def dicts_to_markdown_table(list_of_dicts: list[dict[str, str]]) -> Markdown:
    if not list_of_dicts:
        return Markdown("")

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

    return Markdown(table)


def language_marker_from_file_extension(file_path: str) -> LanguageMarker:

    for lang_marker in LanguageMarker:
        for file_extension in FileExtensionsForLanguageMarker[lang_marker]:
            if file_path.endswith(file_extension):
                return lang_marker

    return DEFAULT_LANGUAGE_MARKER


def markdown_file_block_for_text_file(text_file: TextFile):

    language: str = language_marker_from_file_extension(text_file.path).value
    file_path: str = text_file.path
    contents: str = text_file.contents

    return f"""

**`{file_path}`**
```{language}
{contents}
```

"""
