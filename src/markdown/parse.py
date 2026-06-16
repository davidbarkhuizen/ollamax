import re
from typing import List

from model.model import TextFile


def extract_embedded_text_files_from_markdown(markdown_str: str) -> List[TextFile]:
    """
    Extracts code blocks from a markdown document

    Args:
        markdown_str: multiline markdown document string

    Returns:
        List of tuples, where each tuple is
        [ file_contents, file_path ]
    """
    code_files = []

    # Regex patterns
    #
    # Marker: **`path**`
    marker_pattern = re.compile(r"^\*\*`(.+)`\*\*$")
    # Code block start: ``` (optionally followed by language identifier)
    code_start_pattern = re.compile(r"^`{3,}")
    # Code block end: ``` (with optional whitespace)
    code_end_pattern = re.compile(r"^\s*`{3,}\s*$")

    lines = markdown_str.split("\n")

    in_code_block = False
    code_content = []
    relative_file_path = ""
    prev_line = None

    for line in lines:
        line_stripped = line.rstrip("\n\r")

        if not in_code_block:
            if code_start_pattern.match(line_stripped):
                # Check previous line for marker
                if prev_line is not None:
                    match = marker_pattern.match(prev_line.strip())
                    if match:
                        relative_file_path = match.group(1)
                        in_code_block = True
                        code_content = []
            # Update prev_line for next iteration
            prev_line = line_stripped
        else:
            if code_end_pattern.match(line_stripped):
                code_files.append(TextFile(contents="\n".join(code_content), path=relative_file_path))
                in_code_block = False
                relative_file_path = ""
                code_content = []
            else:
                code_content.append(line_stripped)

    return code_files
