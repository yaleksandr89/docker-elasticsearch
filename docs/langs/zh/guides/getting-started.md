# 入门

## 选择语言

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| [Русский](../../ru/guides/getting-started.md) | [English](../../en/guides/getting-started.md) | [Español](../../es/guides/getting-started.md) | **已选** | [Français](../../fr/guides/getting-started.md) | [Deutsch](../../de/guides/getting-started.md) |

本地 Elasticsearch 学习环境：索引、文档、全文搜索、过滤、聚合和文本分析。Kibana 提供 Dev Tools 和数据探索功能；Nginx 将 HTTP 请求转发给相应服务。环境不预装商品数据库，请按指南创建练习索引。

仅限合成数据。本机进程、浏览器和有 Docker 权限的用户均可通过 HTTP 免认证访问。请勿将环境暴露到公网。

## 要求

Git、GNU Make、Bash、curl、Docker Engine 28+ 或 Docker Desktop，Compose v2.14.2+。推荐 Linux、macOS 或 Windows + WSL2。首次构建需要访问官方镜像仓库、系统软件仓库和插件服务器，并有可用磁盘及至少 4 GiB 可用内存（推荐 6–8 GiB）；Elasticsearch JVM 堆为 2 GiB，Kibana 和 Docker 还需额外内存。

## 准备宿主机

启动前检查版本和可用资源。在 Linux 及 Docker/WSL 使用的 Linux 环境中检查 `vm.max_map_count`；当前 Elasticsearch 的官方建议值为 `1048576`。如果较低且 Elasticsearch 报 bootstrap check 错误，按[官方说明](https://www.elastic.co/docs/deploy-manage/deploy/self-managed/vm-max-map-count)设置实际运行 Docker 的内核。不要盲目修改宿主机。Docker Desktop 的内存分配给其虚拟机。

```bash
docker version
docker compose version
make --version
# Linux / WSL
sysctl vm.max_map_count
```

## 快速开始

```bash
git clone https://github.com/yaleksandr89/docker-elasticsearch.git
cd docker-elasticsearch
make init
make config
```

构建前检查端口是否空闲、Docker 内存及项目名和三个容器名是否可用。`make config` 应仅显示 `backend` 网络，且只发布 `127.0.0.1:8080`。第二份环境需使用独立的名称、端口和两个数据目录。镜像用户须能写入各自目录。

```bash
docker compose ls -a
docker ps -a
ls -ld data/elasticsearch data/kibana
make build
```

`make init` 保留现有 `.docker.env` 并创建缺失的目录，保留原有权限。实测 Elasticsearch 的 UID 为 1000，主 GID 为 0。Kibana 的 UID 为 1000，主 GID 为 1000，附加组为 0。以下命令适用于本地 Linux 上使用默认设置的全新副本。先用 `make config` 核对路径，再核对实际 ID、所有者及两个目录是否为空。

```bash
docker run --rm --network none --read-only --entrypoint id docker-elasticsearch-elasticsearch
docker run --rm --network none --read-only --entrypoint id docker-elasticsearch-kibana
id
ls -ldn data/elasticsearch data/kibana
find data/elasticsearch data/kibana -mindepth 1 -maxdepth 1 -print
```

如果镜像 UID 与目录所有者不同且缺少访问权限，所有者可仅对这两个新建的空目录授权。确认 UID 为 1000 及准确路径后再执行示例。此示例需要支持 POSIX ACL 的本地文件系统以及可选的 `setfacl` 和 `getfacl`。不支持时与所有者确认一个新的可写位置。请保留现有数据目录。

```bash
setfacl -m u:1000:rwx -- data/elasticsearch data/kibana
getfacl -- data/elasticsearch data/kibana
```

```bash
make up
```

Elasticsearch 通过 HTTP 健康检查后，Compose 在后台启动 Kibana。请通过 /api/status 确认 Kibana 就绪。自定义域名或端口时请同步修改示例 URL。 [Kibana](http://kibana.local:8080) · [Elasticsearch](http://elastic.local:8080)

## 连接和就绪检查

在运行浏览器的系统 hosts 文件中添加两行：Linux/macOS `/etc/hosts`，Windows `C:\Windows\System32\drivers\etc\hosts`（需要相应权限）。curl 无需修改 hosts：`--resolve` 将带有正确 Host 的请求发送到 loopback。

```text
127.0.0.1    elastic.local
127.0.0.1    kibana.local
```

```bash
curl --noproxy '*' --resolve elastic.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 http://elastic.local:8080/
curl --noproxy '*' --resolve elastic.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 'http://elastic.local:8080/_cluster/health?pretty'
curl --noproxy '*' --resolve elastic.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 'http://elastic.local:8080/_cat/plugins?v'
curl --noproxy '*' --resolve kibana.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 http://kibana.local:8080/api/status
```

Elasticsearch 根响应包含 `version.number` 和 `cluster_name`；`_cluster/health` 返回状态。`green` 表示所有分片可用，单节点 `yellow` 可能表示副本未分配，`red` 需要排查。`_cat/plugins` 应包含两个插件。当 `/api/status` 返回 `status.overall.level: available` 时 Kibana 就绪，此前可能出现 502/503。随后打开 [Kibana](http://kibana.local:8080) 的 Dev Tools → Console。

[启动故障排查](troubleshooting.md) · [搜索与文本分析练习](search-lab.md)

## 历史截图

保留早期环境（Elasticsearch 6.8.0）的原始截图。当前版本的布局、菜单和响应不同；这些图片不证明当前运行成功。

![Elasticsearch 6.8.0 — 根响应](../../../assets/elastic-local-1.png)

![Elasticsearch 6.8.0 — 搜索响应](../../../assets/elastic-local-2.png)

![Kibana — 集群概览](../../../assets/kibana-local-1.png)

![Kibana — Discover 文档](../../../assets/kibana-local-2.png)

![Kibana — Dev Tools 控制台](../../../assets/kibana-local-3.png)

## 文档

- [搜索与文本分析练习](search-lab.md)
- [运维与 Make 命令](operations.md)
- [故障排查](troubleshooting.md)
- [架构与配置](../reference/configuration.md)
- [参与贡献](../CONTRIBUTING.md)
