from rich.console import Console
from rich.markdown import Markdown

console = Console()


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


def display_markdown(markdown: Markdown):
    global console
    console.print(markdown)


def display_text_as_markdown(text: str):
    global console
    console.print(Markdown(text))
