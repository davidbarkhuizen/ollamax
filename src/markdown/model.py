from enum import Enum


class LanguageMarker(Enum):
    CSV = "csv"
    PYTHON = "python"
    SQL = "sql"
    TEXT = "text"


DEFAULT_LANGUAGE_MARKER: LanguageMarker = LanguageMarker.TEXT

FileExtensionsForLanguageMarker: dict[LanguageMarker, list[str]] = {
    LanguageMarker.PYTHON: [".py"],
    LanguageMarker.TEXT: [".txt"],
    LanguageMarker.SQL: [".sql"],
    LanguageMarker.CSV: [".csv"],
}
