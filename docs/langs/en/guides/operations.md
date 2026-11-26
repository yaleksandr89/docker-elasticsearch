# Operations and Make commands

## Choose language

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| [Русский](../../ru/guides/operations.md) | **Selected** | [Español](../../es/guides/operations.md) | [中文](../../zh/guides/operations.md) | [Français](../../fr/guides/operations.md) | [Deutsch](../../de/guides/operations.md) |

The lab uses local mode by default. Prepare the data directories as described in the getting-started guide before starting.

[Getting started](getting-started.md)

## Quick start

```bash
make help
make init
make config
```

`COMPOSE_COMMAND` = `docker compose`.

```bash
make COMPOSE_COMMAND='docker compose' config
```

| Command | Effect |
|---|---|
| `make help` | Shows bilingual help. |
| `make init` | Creates `.docker.env` if absent and directories from both `*_DATA_DIR` variables; preserves existing configuration. |
| `make pull` | Pulls base images from official registries using Make configuration versions; does not rebuild local images. |
| `make build` | Builds images without cache. |
| `make config` | Shows resolved Compose configuration without starting services. |
| `make up` | Compose starts Kibana in the background after the Elasticsearch HTTP health check succeeds. Check Kibana readiness at /api/status. Adjust example URLs for any custom domain or port. |
| `make down` | Stops and removes containers and managed network, but not the host data directory. |
| `make reset` | Runs `down` then `up -d` in order, recreating containers and preserving data and indices. |
| `make restart` | Restarts existing containers; does not apply image, Compose or environment changes. |
| `make in elasticsearch` | Starts Bash in the chosen service. Names: `elasticsearch`, `kibana`, `nginx`. |
| `make log kibana` | Prints the chosen service logs; does not follow automatically. |

```bash
docker compose --env-file .docker.env -f docker-compose.yml ps
make log elasticsearch
make restart
make down
```

## Connect a separate project

Find the application’s existing trusted network with `docker network ls` and check its members with `docker network inspect`. Set its actual name as `EXTERNAL_NETWORK` in `.docker.env`. Compose merges the base and extension, keeps `backend`, and attaches only Elasticsearch to the extra network. From the application container use `http://docker-elasticsearch-es:9200` or the actual `ELASTIC_CONTAINER` name. All network members get unauthenticated access. Keep the flag on subsequent commands, including shutdown.

```bash
docker network ls
make config WITH_EXTERNAL_NETWORK=1
make up WITH_EXTERNAL_NETWORK=1
```

```bash
make down WITH_EXTERNAL_NETWORK=1
```

To switch modes, run `down` with the old file set or flag, keep both data paths, then run `up` with the new setting. The external network remains with its owner. Use only the agreed network and data paths. `restart` retains the existing container network settings.

```bash
docker compose --env-file .docker.env -f docker-compose.yml -f docker-compose.external.yml config
docker compose --env-file .docker.env -f docker-compose.yml -f docker-compose.external.yml up -d
docker compose --env-file .docker.env -f docker-compose.yml -f docker-compose.external.yml down
```

## Persistence and upgrades

Both bind mounts survive recreation. Kibana stores most saved objects in Elasticsearch system indices. Before stopping the old stack, inspect `/usr/share/kibana/data` in its container and save any needed container-local files separately.

Make has no automatic cleanup, snapshot or restore targets. Copying a live Elasticsearch data directory is unreliable as a backup. Before shutdown, record the running versions, container names, port and both mount paths. When needed, take an official [snapshot](https://www.elastic.co/docs/deploy-manage/tools/snapshot-and-restore), test restoration in a separate lab and verify plugin compatibility at each step of the [supported upgrade path](https://www.elastic.co/docs/deploy-manage/upgrade). Keep the configured `ELASTIC_CONTAINER` name for existing clients, such as `global-elasticsearch`. Change an old port 80 to 8080 only deliberately. The owner decides whether to upgrade separately.

Stop the old lab with its original configuration. If the source version is unknown, establish compatibility first. Downgrading on upgraded data is unsafe.

## Checks

CI runs for pushes and pull requests to `master`, and manually from Actions. `quality` checks startup script syntax, training fixtures and resolved Compose; `docker-smoke` builds an isolated lab with fixed versions and checks HTTP via both virtual hosts, plugins and training searches. CI results, not the presence of a workflow, establish whether it passed.

Python 3 is needed only for fixture and CI checks.

```bash
bash -n docker-configs/nginx/start-nginx.sh
python3 tests/check-fixtures.py
python3 tests/test-runtime-contract.py
```

Run `tests/smoke.py` only in a disposable checkout. Locally it requires `/tmp/docker-elasticsearch-review.XXXXXXXX/candidate` and project `elastic-learning-test-xxxxxxxx`, with the same eight alphanumeric characters lowercased in the project name. Before creating the index it checks labels, images, network, port and both mounts. Use `--persisted` to verify the previously created documents.

## Documentation

- [Getting started](getting-started.md)
- [Search and text analysis exercises](search-lab.md)
- [Troubleshooting](troubleshooting.md)
- [Architecture and configuration](../reference/configuration.md)
- [Contributing](../CONTRIBUTING.md)
