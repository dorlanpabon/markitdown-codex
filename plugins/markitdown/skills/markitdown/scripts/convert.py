# /// script
# requires-python = ">=3.12,<3.14"
# dependencies = [
#   "markitdown[docx,pptx,xlsx,xls,pdf]==0.1.7",
#   "mcp==1.26.0",
# ]
# ///
"""Local-only MarkItDown conversion, available through stdio MCP or a CLI."""

import argparse
import io
import os
import sys
import zipfile
from pathlib import Path
from typing import Annotated

from markitdown import MarkItDown, StreamInfo
from markitdown.converters import (
    CsvConverter,
    DocxConverter,
    HtmlConverter,
    IpynbConverter,
    PdfConverter,
    PlainTextConverter,
    PptxConverter,
    XlsConverter,
    XlsxConverter,
)
from pydantic import BaseModel, Field

MAX_INPUT_BYTES = 25 * 1024 * 1024
MAX_ARCHIVE_BYTES = 100 * 1024 * 1024
CONVERTERS = {
    ".pdf": PdfConverter,
    ".docx": DocxConverter,
    ".pptx": PptxConverter,
    ".xlsx": XlsxConverter,
    ".xls": XlsConverter,
    ".html": HtmlConverter,
    ".htm": HtmlConverter,
    ".csv": CsvConverter,
    ".ipynb": IpynbConverter,
    **dict.fromkeys((".txt", ".md", ".json", ".xml"), PlainTextConverter),
}


class ConversionError(ValueError):
    """A user-facing error without document contents or parser tracebacks."""


class MarkdownPage(BaseModel):
    markdown: str
    total_chars: int
    offset: int
    next_offset: int | None
    warnings: list[str]


def local_path(value: str) -> Path:
    if not value or "://" in value or value.startswith(("\\\\", "//")):
        raise ConversionError(
            "Use an absolute local file path, not a URI or network share."
        )
    path = Path(value)
    if not path.is_absolute():
        raise ConversionError("Use an absolute local file path.")
    path = path.resolve()
    if str(path).startswith(("\\\\", "//")):
        raise ConversionError("Network shares are not supported.")
    root = os.environ.get("MARKITDOWN_ROOT")
    if root:
        allowed = Path(root)
        if not allowed.is_absolute() or not allowed.is_dir():
            raise ConversionError(
                "MARKITDOWN_ROOT must be an existing absolute directory."
            )
        if not path.is_relative_to(allowed.resolve()):
            raise ConversionError("Input is outside MARKITDOWN_ROOT.")
    if not path.is_file():
        raise ConversionError("Input must be an existing regular file.")
    if path.suffix.lower() not in CONVERTERS:
        raise ConversionError("Unsupported file format.")
    return path


def convert_document(value: str) -> str:
    try:
        path = local_path(value)
        with path.open("rb") as source:
            data = source.read(MAX_INPUT_BYTES + 1)
        if len(data) > MAX_INPUT_BYTES:
            raise ConversionError("Input exceeds the 25 MiB limit.")
        if path.suffix.lower() in {".docx", ".pptx", ".xlsx"}:
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                entries = archive.infolist()
                if (
                    len(entries) > 10_000
                    or sum(e.file_size for e in entries) > MAX_ARCHIVE_BYTES
                ):
                    raise ConversionError(
                        "Office archive exceeds the expanded content limit."
                    )
        converter = MarkItDown(enable_builtins=False, enable_plugins=False)
        converter.register_converter(CONVERTERS[path.suffix.lower()]())
        return converter.convert_stream(
            io.BytesIO(data), stream_info=StreamInfo(extension=path.suffix.lower())
        ).markdown
    except ConversionError:
        raise
    except Exception as exc:
        raise ConversionError(
            "Conversion failed. Check file access, format and integrity."
        ) from exc


def convert_to_markdown(
    path: Annotated[
        str, Field(description="Absolute path to the user-selected local document.")
    ],
    offset: Annotated[
        int, Field(ge=0, description="Character offset; start at zero.")
    ] = 0,
    max_chars: Annotated[int, Field(ge=1, le=100_000)] = 20_000,
) -> MarkdownPage:
    """Read a local document and return a Markdown page without modifying the file.

    Supports PDF, Office, HTML, CSV and text, up to 25 MiB. No URLs or OCR.
    Returns document content to the assistant. Use next_offset for more pages.
    """
    if offset < 0 or not 1 <= max_chars <= 100_000:
        raise ConversionError("Invalid pagination bounds.")
    markdown = convert_document(path)
    if offset > len(markdown):
        raise ConversionError("Offset exceeds the converted document length.")
    end = min(offset + max_chars, len(markdown))
    return MarkdownPage(
        markdown=markdown[offset:end],
        total_chars=len(markdown),
        offset=offset,
        next_offset=end if end < len(markdown) else None,
        warnings=[]
        if markdown.strip()
        else ["No text extracted; the document may require OCR."],
    )


def create_server():
    from mcp.server.fastmcp import FastMCP
    from mcp.types import ToolAnnotations

    server = FastMCP("markitdown", log_level="ERROR")
    server.tool(
        annotations=ToolAnnotations(
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
            idempotentHint=True,
        ),
        structured_output=True,
    )(convert_to_markdown)
    return server


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", help="Absolute local input path")
    parser.add_argument(
        "--output", type=Path, help="New Markdown output file; never overwritten"
    )
    parser.add_argument(
        "--stdio", action="store_true", help="Start the local MCP server"
    )
    args = parser.parse_args()
    if args.stdio:
        if args.path or args.output:
            parser.error("--stdio cannot be combined with a file or --output")
        create_server().run(transport="stdio")
        return 0
    if not args.path:
        parser.error("provide an absolute input path or --stdio")
    try:
        markdown = convert_document(args.path)
        if args.output:
            with args.output.open("x", encoding="utf-8", newline="\n") as destination:
                destination.write(markdown)
        else:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stdout.write(markdown)
        if not markdown.strip():
            print("Warning: no text extracted; OCR may be required.", file=sys.stderr)
        return 0
    except (ConversionError, OSError) as exc:
        message = (
            str(exc)
            if isinstance(exc, ConversionError)
            else "Cannot create output; use a new writable path."
        )
        print(f"Error: {message}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
