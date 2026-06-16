from rich.console import Console
from rich.markdown import Markdown


def new_markdown_console() -> Console:
    return Console()


def display_markdown(console: Console, markdown: Markdown):
    console.print(markdown)


def display_text_as_markdown(console: Console, text: str):
    console.print(Markdown(text))
