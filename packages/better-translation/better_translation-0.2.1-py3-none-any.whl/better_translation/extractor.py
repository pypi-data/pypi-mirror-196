from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence
    from pathlib import Path

    from better_translation.types import MessageID, TranslatedText


FUNCTION_NAMES_TO_EXTRACT_FROM = (
    "gettext",
    "ngettext",
    "lazy_gettext",
    "lazy_ngettext",
    "_",
    "__",
)


def _get_regex_to_extract_function_calls(
    function_names: Sequence[str],
) -> re.Pattern[str]:
    """Return a regex that matches calls of the given function names."""
    _function_names = "|".join(function_names)
    return re.compile(rf"""({_function_names})(\(["|'].*["|'].*\))""")


@dataclass(slots=True)
class ExtractedMessage:
    id: MessageID = field(init=False)
    default: TranslatedText | None = field(init=False)
    default_plural: TranslatedText | None = field(init=False)
    context: Any | None = field(init=False)
    extra: dict[str, str | int | None] = field(init=False)

    def __init__(
        self,
        message_id: str,
        /,
        default: TranslatedText | None = None,
        default_plural: TranslatedText | None = None,
        context: Any | None = None,
        **extra: Any,
    ) -> None:
        self.id = message_id
        self.default = default
        self.default_plural = default_plural
        self.context = context
        self.extra = extra


def extract_from_code(
    code: str,
    function_names: Sequence[str] = FUNCTION_NAMES_TO_EXTRACT_FROM,
) -> Iterable[ExtractedMessage]:
    """Extract messages from Python code."""
    regex = _get_regex_to_extract_function_calls(function_names)
    for match in regex.finditer(code):
        call_params = match.group(2)
        yield eval(f"ExtractedMessage{call_params}")  # noqa: PGH001


def extract_from_file(
    file_path: Path,
    function_names: Sequence[str] = FUNCTION_NAMES_TO_EXTRACT_FROM,
) -> Iterable[ExtractedMessage]:
    """Extract messages from a Python file."""
    yield from extract_from_code(file_path.read_text(), function_names)


def extract_from_dir(
    directory_path: Path,
    function_names: Sequence[str] = FUNCTION_NAMES_TO_EXTRACT_FROM,
) -> Iterable[ExtractedMessage]:
    """Extract messages from Python files in a directory."""
    for path in directory_path.rglob("*.py"):
        yield from extract_from_file(path, function_names)
