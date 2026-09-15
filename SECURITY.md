# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 2.4.x   | ✅        |
| < 2.4   | ❌        |

## Design notes

AI Context Extractor performs **all analysis locally**. No source code, path or
metadata is uploaded anywhere by the application itself.

If you optionally enable an AI provider integration, only the context you explicitly
send is transmitted, to the provider you configure. Review the generated context
before sending it.

## Built-in protection

- **Safe Sanitizer** (on by default) redacts common secret patterns — AWS keys, Google
  API keys, generic `api_key` / `token` / `password` assignments, bearer tokens, emails
  and non-private IPv4 addresses — before content is copied to the clipboard or exported.

> The sanitizer is a best-effort safety net, **not** a guarantee. Always review exported
> context before sharing it.

## Reporting a vulnerability

Please **do not** open a public issue for security problems.

Email the maintainers at `hasnainrazamemon9@gmail.com` (override via `AICE_SUPPORT_EMAIL`)
with:

- a description of the issue and its impact,
- steps to reproduce,
- affected version(s),
- any suggested fix.

We aim to acknowledge reports within 72 hours.
