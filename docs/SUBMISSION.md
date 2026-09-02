# OpenAI plugin submission materials

Prepared September 2, 2026. This file is preparation, not proof of submission,
approval or directory publication.

## Distribution choices

- **Codex:** install the full plugin from the public GitHub marketplace.
- **Public directory:** submit the generated skills-only ZIP. It contains the
  same SKILL.md, converter and lockfile tested locally. The CLI works without
  a registered MCP connection in an environment with shell, Python and uv.
- **Hosted MCP:** not provided. The local file-reading MCP must not be exposed
  to the internet. A future hosted variant would need an isolated upload flow,
  production HTTPS, domain verification and an appropriate retention policy.

## Listing copy

| Field | Prepared value |
| --- | --- |
| Name | MarkItDown for Codex |
| Subtitle | Local documents to Markdown |
| Category | Productivity |
| Publisher | dorlanpabon; select the matching verified identity in the portal |
| Website | https://github.com/dorlanpabon/markitdown-codex |
| Support | https://github.com/dorlanpabon/markitdown-codex/issues |
| Privacy | https://github.com/dorlanpabon/markitdown-codex/blob/main/PRIVACY.md |
| Terms | https://github.com/dorlanpabon/markitdown-codex/blob/main/TERMS.md |
| Logo | plugins/markitdown/assets/logo.png |
| Skill bundle | dist/markitdown-skills-0.1.0.zip |

Description:

> Convert local PDF, Word, PowerPoint, Excel, HTML and text documents into
> Markdown for reading, analysis and export. The skill uses Microsoft MarkItDown
> in a local Python environment, preserves extractable text and tables, reports
> conversion failures and never overwrites an existing output. Requires a
> shell-capable environment with uv/Python. No hosted conversion service, API key,
> URL fetching or OCR is included. Community integration by dorlanpabon, not
> affiliated with Microsoft or OpenAI.

Starter prompts:

1. Convert this PDF to Markdown and save the result.
2. Extrae las tablas de este Excel a Markdown.
3. Convert this Word document into Markdown for analysis.

Initial release notes:

> First release of the MarkItDown conversion skill, including a self-contained
> Python converter, dependency lockfile, local document validation and exclusive
> output creation. Review using the supplied synthetic fixtures. The GitHub
> distribution additionally includes a local stdio MCP server; this skills-only
> submission does not register or expose that server.

## Positive review cases

Synthetic input documents are in the release's `markitdown-review-fixtures.zip`.
The expected route for skills-only review is the `markitdown` skill and bundled
CLI; for a local Codex MCP review, `convert_to_markdown` is the read-only tool.

| Prompt | Fixture | Expected result |
| --- | --- | --- |
| Convert this PDF to Markdown and save it. | sample.pdf | New Markdown file containing "Quarterly report 2026". |
| Convert this Word document for analysis. | sample.docx | Markdown containing "Project document" without modifying input. |
| Extract the slide text from this presentation. | sample.pptx | Markdown containing "Project slides". |
| Extract the table from this workbook. | sample.xlsx | Markdown containing Product, Quantity, Coffee and 12. |
| Convert this Spanish text and preserve accents. | unicode.txt | Markdown containing "Bogotá" and "café". |

## Negative review cases

| Prompt / scenario | Expected behavior |
| --- | --- |
| Convert https://example.com/private.pdf directly. | Explain that URL inputs are unsupported; request a local file. No network fetch. |
| Transcribe this audio recording. | Do not trigger this conversion workflow; explain that audio is outside scope. |
| Convert this document and replace an already existing result.md. | Exclusive output creation fails; preserve the existing file and propose a new filename. |

## Portal steps and owner requirements

1. Open https://platform.openai.com/plugins with the publishing organization.
2. Verify the developer identity and Apps Management write permission.
3. Create a **Skills only** draft. Upload the skill ZIP and logo, then use the
   prepared copy, prompts, fixtures and cases above.
4. Verify execution in the target ChatGPT surface; local tests alone do not
   establish universal compatibility.
5. The publisher selects supported countries and reviews policy attestations.
   Do not infer identity verification, legal attestations or availability.
6. Submit for review. After approval, publish from the portal.

Source: [OpenAI's current submission guide](https://developers.openai.com/plugins/deploy/submission).
GitHub publication and workspace marketplace import do not grant public
directory approval.
