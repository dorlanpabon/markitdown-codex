# Privacy

Effective: September 2, 2026. Publisher: dorlanpabon.

The plugin converts documents in the environment where it runs. It has no
publisher-operated backend, analytics, accounts or document storage service.
The bundled adapter uses local parsers; it does not fetch document URLs or enable
cloud converters. Initial dependency installation contacts Python package and
runtime distribution services through uv.

When used through MCP, extracted document text is returned to the assistant and
may become part of the conversation under the host application's policies.
When the CLI is used, output is printed or saved to the path selected by the
user. Users control and can delete exported files. The plugin does not configure
or override the host's conversation retention, processing or sharing policies.

The converter may read any local file accessible to its process unless
`MARKITDOWN_ROOT` restricts the input directory. Use only documents you are
authorized to process. Errors are summarized without including document content;
host/runtime diagnostics and conversation records are controlled by their hosts.

Public GitHub issues are visible to others. Never upload confidential documents,
credentials or personal identifiers there. For privacy questions, open an issue
without sensitive details at
https://github.com/dorlanpabon/markitdown-codex/issues.
