from __future__ import annotations

import codecs
import os
import re
from typing import IO

# Regexp to match python magic encoding line
PYTHON_MAGIC_COMMENT_re = re.compile(
    rb"[ \t\f]* \# .* coding[=:][ \t]*([-\w.]+)",
    re.VERBOSE,
)


def parse_encoding(fp: IO[bytes]) -> str | None:
    """Deduce the encoding of a source file from magic comment.

    It does this in the same way as the `Python interpreter`__

    .. __: https://docs.python.org/3.4/reference/lexical_analysis.html#encoding-declarations

    The ``fp`` argument should be a seekable file object.

    (From Jeff Dairiki)
    """
    pos = fp.tell()
    fp.seek(0)
    try:
        line1 = fp.readline()
        has_bom = line1.startswith(codecs.BOM_UTF8)
        if has_bom:
            line1 = line1[len(codecs.BOM_UTF8) :]

        m = PYTHON_MAGIC_COMMENT_re.match(line1)
        if not m:
            try:
                import ast

                ast.parse(line1.decode("latin-1"))
            except (ImportError, SyntaxError, UnicodeEncodeError):
                # Either it's a real syntax error, in which case the source is
                # not valid python source, or line2 is a continuation of line1,
                # in which case we don't want to scan line2 for a magic
                # comment.
                pass
            else:
                line2 = fp.readline()
                m = PYTHON_MAGIC_COMMENT_re.match(line2)

        if has_bom:
            if m:
                magic_comment_encoding = m.group(1).decode("latin-1")
                if magic_comment_encoding != "utf-8":
                    raise SyntaxError(
                        "encoding problem: {} with BOM".format(
                            magic_comment_encoding,
                        ),
                    )
            return "utf-8"
        elif m:
            return m.group(1).decode("latin-1")
        else:
            return None
    finally:
        fp.seek(pos)


PYTHON_FUTURE_IMPORT_re = re.compile(r"from\s+__future__\s+import\s+\(*(.+)\)*")


def parse_future_flags(fp: IO[bytes], encoding: str = "latin-1") -> int:
    """Parse the compiler flags by :mod:`__future__` from the given Python
    code.
    """
    import __future__

    pos = fp.tell()
    fp.seek(0)
    flags = 0
    try:
        body = fp.read().decode(encoding)

        # Fix up the source to be (hopefully) parsable by regexpen.
        # This will likely do untoward things if the source code itself is broken.

        # (1) Fix `import (\n...` to be `import (...`.
        body = re.sub(r"import\s*\([\r\n]+", "import (", body)
        # (2) Join line-ending commas with the next line.
        body = re.sub(r",\s*[\r\n]+", ", ", body)
        # (3) Remove backslash line continuations.
        body = re.sub(r"\\\s*[\r\n]+", " ", body)

        for m in PYTHON_FUTURE_IMPORT_re.finditer(body):
            names = [x.strip().strip("()") for x in m.group(1).split(",")]
            for name in names:
                feature = getattr(__future__, name, None)
                if feature:
                    flags |= feature.compiler_flag
    finally:
        fp.seek(pos)
    return flags


def pathmatch(pattern: str, filename: str) -> bool:
    """Extended pathname pattern matching.

    This function is similar to what is provided by the ``fnmatch`` module in
    the Python standard library, but:

     * can match complete (relative or absolute) path names, and not just file
       names, and
     * also supports a convenience pattern ("**") to match files at any
       directory level.

    Examples
    --------
    >>> pathmatch('**.py', 'bar.py')
    True
    >>> pathmatch('**.py', 'foo/bar/baz.py')
    True
    >>> pathmatch('**.py', 'templates/index.html')
    False

    >>> pathmatch('./foo/**.py', 'foo/bar/baz.py')
    True
    >>> pathmatch('./foo/**.py', 'bar/baz.py')
    False

    >>> pathmatch('^foo/**.py', 'foo/bar/baz.py')
    True
    >>> pathmatch('^foo/**.py', 'bar/baz.py')
    False

    >>> pathmatch('**/templates/*.html', 'templates/index.html')
    True
    >>> pathmatch('**/templates/*.html', 'templates/foo/bar.html')
    False

    :param pattern: the glob pattern
    :param filename: the path name of the file to match against
    """
    symbols = {
        "?": "[^/]",
        "?/": "[^/]/",
        "*": "[^/]+",
        "*/": "[^/]+/",
        "**/": "(?:.+/)*?",
        "**": "(?:.+/)*?[^/]+",
    }

    if pattern.startswith("^"):
        buf = ["^"]
        pattern = pattern[1:]
    elif pattern.startswith("./"):
        buf = ["^"]
        pattern = pattern[2:]
    else:
        buf = []

    for idx, part in enumerate(re.split("([?*]+/?)", pattern)):
        if idx % 2:
            buf.append(symbols[part])
        elif part:
            buf.append(re.escape(part))
    match = re.match("".join(buf) + "$", filename.replace(os.sep, "/"))
    return match is not None
