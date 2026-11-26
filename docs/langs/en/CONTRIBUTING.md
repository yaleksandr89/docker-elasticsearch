# Contributing

## Choose language

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| [Русский](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/.github/CONTRIBUTING.md) | **Selected** | [Español](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/es/CONTRIBUTING.md) | [中文](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/zh/CONTRIBUTING.md) | [Français](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/fr/CONTRIBUTING.md) | [Deutsch](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/de/CONTRIBUTING.md) |

Report reproducible bugs via Issues, questions and ideas via Discussions. Do not publish real data, local configuration, passwords or vulnerability details. Agree substantial changes with the owner first.

- Reproducible bugs: [GitHub Issues](https://github.com/yaleksandr89/docker-elasticsearch/issues).
- Questions and ideas: [GitHub Discussions](https://github.com/yaleksandr89/docker-elasticsearch/discussions).
- Vulnerabilities: [security policy](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/en/SECURITY.md).

Preserve Make commands, configuration names, data compatibility and the lab’s purpose. Image, network, port publication, auth/TLS and storage changes require a separate decision. Test in a fresh checkout with synthetic data and unique containers, port and project; do not touch the working lab.

## Checks

CI runs for pushes and pull requests to `master`, and manually from Actions. `quality` checks startup script syntax, training fixtures and resolved Compose; `docker-smoke` builds an isolated lab with fixed versions and checks HTTP via both virtual hosts, plugins and training searches. CI results, not the presence of a workflow, establish whether it passed.

```bash
bash -n docker-configs/nginx/start-nginx.sh
python3 tests/check-fixtures.py
python3 tests/test-runtime-contract.py
```

Make defaults to `WITH_EXTERNAL_NETWORK=0`. For integration set `EXTERNAL_NETWORK` to an existing trusted network and pass `WITH_EXTERNAL_NETWORK=1` to every Make command. Only Elasticsearch joins it. Its members get unauthenticated access by container name on port 9200. Compose leaves the external network in place on shutdown.

## Pull Request

Create a topic branch from `master`, use signed Conventional Commits with Russian descriptions. In the PR state the reason, change, data and security impact and actual checks. Synchronize six locales; do not weaken checks for green CI.

## Documentation

- [Getting started](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/en/guides/getting-started.md)
- [Search and text analysis exercises](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/en/guides/search-lab.md)
- [Operations and Make commands](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/en/guides/operations.md)
- [Troubleshooting](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/en/guides/troubleshooting.md)
- [Architecture and configuration](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/en/reference/configuration.md)
