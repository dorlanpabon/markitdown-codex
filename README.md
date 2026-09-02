# MarkItDown for Codex

Community plugin by [dorlanpabon](https://github.com/dorlanpabon), powered by
[Microsoft MarkItDown](https://github.com/microsoft/markitdown).

Convert local PDF, Word, PowerPoint, Excel and text documents into Markdown.
Includes a Codex plugin manifest, repository marketplace, conversion skill and
local MCP integration. Not affiliated with Microsoft or OpenAI.

## Install in Codex

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/) on your
PATH. The locked runtime uses Python 3.12 or 3.13; uv can provision it when needed.
Restart Codex after installing uv so the desktop app inherits the updated PATH.

In Codex, open **Plugins**, add the GitHub marketplace
`https://github.com/dorlanpabon/markitdown-codex`, and install **MarkItDown for Codex**.
The equivalent commands in the official OpenAI Codex CLI are:

```sh
codex plugin marketplace add dorlanpabon/markitdown-codex
codex plugin add markitdown@dorlanpabon-markitdown
```

Start a new task after installation, then ask:

> Usa MarkItDown para convertir este PDF a Markdown y guarda el resultado.

> Extract the tables from this Excel file into Markdown.

First use downloads dependencies into uv's cache. No API key, Microsoft account,
paid infrastructure or hosted backend is required.

## What is included

| Component | Purpose |
| --- | --- |
| `plugins/markitdown` | Installable Codex plugin |
| `.agents/plugins/marketplace.json` | GitHub marketplace catalog |
| `skills/markitdown/SKILL.md` inside the plugin | Conversion and export workflow |
| `convert_to_markdown` | Local stdio MCP tool with structured, paginated output |
| `dist/markitdown-skills-0.1.0.zip` after building | Self-contained skills-only submission bundle |

The plugin uses the stable `markitdown==0.1.7` library and `mcp==1.26.0`, with
transitive dependencies locked. It does not depend on the prerelease
`markitdown-mcp` package. The adapter registers only the selected local parser;
it does not enable MarkItDown cloud, URL, audio or third-party plugin converters.

Supported inputs: PDF, DOCX, PPTX, XLSX, XLS, HTML/HTM, CSV, JSON, XML, TXT, MD and
IPYNB. Extraction is intended for analysis, not faithful visual reproduction.
Scanned PDFs need a separate OCR workflow. Legacy DOC/PPT, ZIP, EPUB, images and
audio are outside this plugin's scope.

## MCP usage

```json
{"path": "/absolute/path/report.pdf", "offset": 0, "max_chars": 20000}
```

On Windows, use an absolute path such as `C:\\Documents\\report.pdf`. URIs and
UNC/network shares are rejected. Results contain `markdown`, `total_chars`,
`offset`, `next_offset` and `warnings`. Follow `next_offset` until null for the
complete document. Pagination reconverts the input; keep it unchanged between calls.

The MCP tool reads files and returns content to the assistant; it never writes
the input or an output file. Exports use the CLI below or the assistant's file tools.

Limits: 25 MiB input, 100 MiB expanded Office content, 10,000 Office archive entries,
and up to 100,000 returned characters per MCP call. These limits are not a
complete sandbox or a CPU/memory quota for hostile documents.

## CLI export

From a clone of this repository:

```sh
uv run --locked --script plugins/markitdown/skills/markitdown/scripts/convert.py "/absolute/path/report.pdf" --output "report.md"
```

The CLI writes the full result as UTF-8 and refuses to overwrite an existing
output. Omit `--output` to print Markdown. Conversion errors return exit code 1.

Set `MARKITDOWN_ROOT` before starting Codex to restrict readable inputs to an
existing absolute local directory. Without it, the process can read local files
accessible to the current OS user. Symlinks are resolved before checking the root.
For isolated or untrusted inputs, use an OS sandbox/container as well.

## ChatGPT / public directory

The GitHub marketplace is public and installable in Codex. That is separate from
approval in OpenAI's universal Plugin Directory.

This repository also builds a **skills-only** bundle that runs the same converter
through a shell-capable environment. This avoids exposing local filesystem tools
as an unauthenticated public server. It requires Python/uv execution support;
compatibility with every ChatGPT surface is not claimed.

See [submission materials](docs/SUBMISSION.md) for listing copy, five positive
cases, three negative cases and the remaining publisher requirements. Public
submission requires a verified developer identity, portal access, review and
subsequent publication. The local MCP server is not a hosted ChatGPT endpoint.

## Development

```sh
uv sync --locked
uv run ruff check
uv run ruff format --check
uv run pytest -q
uv run python scripts/build_release.py
```

Tests generate synthetic documents and exercise real parsers, pagination,
path restrictions, size limits, overwrite protection and the exact stdio command
from `.mcp.json`. CI runs on Windows and Ubuntu with Python 3.12 and 3.13.

## Privacy, support and attribution

See [privacy](PRIVACY.md), [terms](TERMS.md), [security](SECURITY.md) and [MIT license](LICENSE).
Support: [GitHub issues](https://github.com/dorlanpabon/markitdown-codex/issues).
Do not attach confidential documents to public issues.

Microsoft MarkItDown is maintained separately and has its own
[MIT license](https://github.com/microsoft/markitdown/blob/main/LICENSE).
All dependencies retain their respective licenses. This community integration
does not imply sponsorship or endorsement by Microsoft or OpenAI.
