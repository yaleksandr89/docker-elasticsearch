# 运维与 Make 命令

## 选择语言

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| [Русский](../../ru/guides/operations.md) | [English](../../en/guides/operations.md) | [Español](../../es/guides/operations.md) | **已选** | [Français](../../fr/guides/operations.md) | [Deutsch](../../de/guides/operations.md) |

实验环境默认采用本地模式。启动前按入门指南准备数据目录。

[入门](getting-started.md)

## 快速开始

```bash
make help
make init
make config
```

`COMPOSE_COMMAND` = `docker compose`.

```bash
make COMPOSE_COMMAND='docker compose' config
```

| 命令 | 行为 |
|---|---|
| `make help` | 显示双语帮助。 |
| `make init` | 缺失时创建 `.docker.env` 及两个 `*_DATA_DIR` 目录；保留已有配置。 |
| `make pull` | 按 Make 配置版本拉取官方基础镜像；不重建本地镜像。 |
| `make build` | 无缓存构建镜像. |
| `make config` | 显示解析后的 Compose 配置，不启动服务。 |
| `make up` | Elasticsearch 通过 HTTP 健康检查后，Compose 在后台启动 Kibana。请通过 /api/status 确认 Kibana 就绪。自定义域名或端口时请同步修改示例 URL。 |
| `make down` | 停止并删除容器及托管网络，不删除宿主机数据目录。 |
| `make reset` | 依次执行 `down` 和 `up -d`，重建容器并保留数据和索引。 |
| `make restart` | 重启现有容器，不应用镜像、Compose 或环境变量变更。 |
| `make in elasticsearch` | 在指定服务运行 Bash：`elasticsearch`、`kibana`、`nginx`。 |
| `make log kibana` | 输出所选服务日志，不自动持续跟踪。 |

```bash
docker compose --env-file .docker.env -f docker-compose.yml ps
make log elasticsearch
make restart
make down
```

## 连接独立项目

用 `docker network ls` 找到应用现有的可信网络，用 `docker network inspect` 核对成员，把实际名称写入 `.docker.env` 的 `EXTERNAL_NETWORK`。Compose 合并基础文件和扩展文件，保留 `backend`，并仅将 Elasticsearch 接入额外网络。从应用容器访问 `http://docker-elasticsearch-es:9200` 或实际的 `ELASTIC_CONTAINER` 名称。所有网络成员均可免认证访问。后续命令（包括停止）使用同一选项。

```bash
docker network ls
make config WITH_EXTERNAL_NETWORK=1
make up WITH_EXTERNAL_NETWORK=1
```

```bash
make down WITH_EXTERNAL_NETWORK=1
```

切换模式前先用原文件组合或选项执行 `down`，保留两个数据路径，再用新配置执行 `up`。外部网络仍归其所有者。只使用约定的网络和数据路径。`restart` 保留现有容器的网络设置。

```bash
docker compose --env-file .docker.env -f docker-compose.yml -f docker-compose.external.yml config
docker compose --env-file .docker.env -f docker-compose.yml -f docker-compose.external.yml up -d
docker compose --env-file .docker.env -f docker-compose.yml -f docker-compose.external.yml down
```

## 持久化与升级

两个绑定挂载在容器重建后保留。Kibana 的大部分保存对象位于 Elasticsearch 系统索引中。停止旧环境前，检查其容器内的 `/usr/share/kibana/data` 并单独保存所需的本地文件。

Make 没有自动清理、快照或恢复目标。复制运行中的 Elasticsearch 数据目录不是可靠备份。停止前记录实际版本、容器名、端口和两个挂载路径。必要时创建官方[快照](https://www.elastic.co/docs/deploy-manage/tools/snapshot-and-restore)，在独立实验环境验证恢复，并检查[受支持升级路径](https://www.elastic.co/docs/deploy-manage/upgrade)每一阶段的插件兼容性。现有客户端继续使用已配置的 `ELASTIC_CONTAINER`，例如 `global-elasticsearch`。仅在有意调整时将旧端口 80 改为 8080。升级由所有者另行决定。

用原配置停止旧实验环境。若源版本未知，先确认兼容性。在已升级的数据上降级是不安全的。

## 检查

CI 在 `master` 的 push、pull request 及 Actions 手动触发时运行。`quality` 检查启动脚本语法、练习 fixtures 和解析后的 Compose；`docker-smoke` 使用固定版本构建隔离环境，检查两个虚拟主机的 HTTP、插件及搜索。只有 CI 实际结果才能证明成功。

仅 fixtures 检查和 CI 需要 Python 3。

```bash
bash -n docker-configs/nginx/start-nginx.sh
python3 tests/check-fixtures.py
python3 tests/test-runtime-contract.py
```

仅在一次性副本中运行 `tests/smoke.py`。本地路径必须为 `/tmp/docker-elasticsearch-review.XXXXXXXX/candidate`，项目名为 `elastic-learning-test-xxxxxxxx`，使用相同的八个字母或数字，项目名中的字母转为小写。创建索引前脚本核对标签、镜像、网络、端口和两个挂载。使用 `--persisted` 验证已有测试文档。

## 文档

- [入门](getting-started.md)
- [搜索与文本分析练习](search-lab.md)
- [故障排查](troubleshooting.md)
- [架构与配置](../reference/configuration.md)
- [参与贡献](../CONTRIBUTING.md)
