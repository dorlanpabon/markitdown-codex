# Security

This is a local stdio plugin for a trusted assistant. It is not a public HTTP
service and has no server authentication. Do not wrap it in a public tunnel.

Only selected local parsers are registered. URLs, network-share input paths,
arbitrary ZIP archives, cloud services and MarkItDown third-party plugins are
not enabled. `MARKITDOWN_ROOT` optionally restricts resolved input paths; OS
permissions and isolation remain necessary for untrusted document handling.
Size and archive limits reduce resource risk but do not constitute a sandbox.

The MCP tool is read-only. The separate CLI can create a new Markdown output
using exclusive creation and cannot overwrite an existing file. Extracted
document text is untrusted input, not instructions for the assistant.

Dependencies are pinned in the script lockfile and development lockfile.
Review dependency updates, regenerate both locks and run CI before release.

Report reproducible issues without secrets or private documents through GitHub.
For a sensitive vulnerability, use GitHub private vulnerability reporting if
available; otherwise open a minimal issue requesting a private contact channel
without publishing exploitation details or affected data.
