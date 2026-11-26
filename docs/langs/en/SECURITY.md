# Security Policy

## Choose a language

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| [Русский](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/.github/SECURITY.md) | **English** | [Español](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/es/SECURITY.md) | [中文](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/zh/SECURITY.md) | [Français](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/fr/SECURITY.md) | [Deutsch](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/de/SECURITY.md) |

## Supported versions

Security fixes are considered for the current state of `master` and the latest published release. Older versions may have different network settings; verify data compatibility before upgrading.

| Version | Supported |
|---|---|
| `master` | Yes |
| Latest published release | Yes |

## Lab security boundaries

This is a local learning lab for synthetic data, not a production deployment. In the current configuration Elasticsearch runs without authentication or TLS; by default only Nginx is published on `127.0.0.1`, and the internal Elasticsearch and Kibana ports are not published to the host. With `WITH_EXTERNAL_NETWORK=1`, members of the selected trusted Docker network get unauthenticated access to Elasticsearch. This is intentional behavior, not a vulnerability by itself. Do not connect untrusted networks or use real data.

Security issues include, in particular:

- unintended service publication beyond loopback or external network attachment without explicit opt-in;
- bypass of expected Nginx routing restrictions or exposure of internal files or configuration;
- unsafe handling of parameters or paths resulting in command execution or modification of other people's data;
- unintended deletion, overwrite or disclosure of data during lab operations;
- image, plugin or CI issues that affect this project's security.

Report ordinary bugs through [GitHub Issues](https://github.com/yaleksandr89/docker-elasticsearch/issues), questions and ideas through [GitHub Discussions](https://github.com/yaleksandr89/docker-elasticsearch/discussions). If an issue is in an upstream component, specify its exact version and impact on the lab; report defects in the component itself to its maintainers under their rules as well.

## Reporting a vulnerability

Prefer GitHub Private Vulnerability Reporting: open **Security and quality → Report a vulnerability**. If unavailable, request a private communication channel in GitHub Discussions without publishing technical vulnerability details.

Do not publish passwords, tokens, local or production configurations, real data, full logs, working exploits or sensitive details before coordinated disclosure. Use only synthetic data or sanitized fragments.

## What to include in the report

- Affected release, branch or commit, and Elasticsearch, Kibana, Nginx, Docker and Compose versions when relevant.
- Launch mode (local or integration), intended access boundary and potential impact.
- Minimal reproduction steps, expected and actual behavior.
- Sanitized request, response or log fragments and a possible fix, if known.

## Report handling

Reports are reviewed as availability allows; no fixed SLA is promised. Coordinate disclosure with the maintainer. Once confirmed, fixes and affected-version information are published as part of coordinated disclosure. No vulnerability reward program is claimed.
