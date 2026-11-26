# 故障排查

## 选择语言

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| [Русский](../../ru/guides/troubleshooting.md) | [English](../../en/guides/troubleshooting.md) | [Español](../../es/guides/troubleshooting.md) | **已选** | [Français](../../fr/guides/troubleshooting.md) | [Deutsch](../../de/guides/troubleshooting.md) |

先检查解析后的配置、容器状态和日志。分享输出前删除凭据、令牌、数据和内部名称。以下命令使用本地模式。集成模式下，Make 加 `WITH_EXTERNAL_NETWORK=1`，Compose 加 `-f docker-compose.external.yml`。

[入门](getting-started.md)

```bash
make config
docker compose --env-file .docker.env -f docker-compose.yml ps -a
make log elasticsearch
make log kibana
make log nginx
```

## 外部网络错误

只有显式启用集成时，外部网络缺失才会导致启动失败。用 `docker network ls` 对照 `EXTERNAL_NETWORK`，然后用实际名称执行 `docker network inspect`。与应用所有者确认成员。请勿改动其他项目的网络。下图为 6.8 历史截图。

```bash
docker network ls
```

![外部网络错误](../../../assets/make-up-error.png) (6.8)

## 端口、域名与 502/503

端口被占用时选择空闲的 `NGINX_PORT`，更新所有 URL 和 `--resolve` 参数。内部端口 9200 和 5601 固定。curl 正常而浏览器失败时，检查浏览器主机的 hosts 文件及两个域名的代理绕过。未知 Host 返回 HTTP 404。遇到 502/503 时检查上游状态和日志。Compose 等待有限次的 Elasticsearch HTTP 健康检查；`/api/status` 报告 `status.overall.level: available` 时 Kibana 才就绪。Elasticsearch 重试耗尽时先诊断其日志。镜像更改用 `make build`，配置更改用 `make up`；也可保留挂载后执行 `down` 和 `up`。`restart` 保留当前配置。

```bash
curl --noproxy '*' --resolve elastic.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 http://elastic.local:8080/
curl --noproxy '*' --resolve elastic.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 'http://elastic.local:8080/_cluster/health?pretty'
curl --noproxy '*' --resolve elastic.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 'http://elastic.local:8080/_cat/plugins?v'
curl --noproxy '*' --resolve kibana.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 http://kibana.local:8080/api/status
```

## 构建、插件与资源

构建失败时检查官方镜像仓库和插件下载是否可访问。Elasticsearch 与 Kibana 版本须一致。`_cat/plugins` 应显示同版本的 `analysis-icu` 和 `analysis-phonetic`。启动失败时检查磁盘、Docker 内存、OOM 日志、`vm.max_map_count` 以及实际路径的[两组 UID/GID 权限](getting-started.md)。分析器报错时查看 API 响应并检查 `config/analysis/synonyms.txt`。使用 `lenient` 改变行为前先排查无效规则。

## 文档

- [入门](getting-started.md)
- [搜索与文本分析练习](search-lab.md)
- [运维与 Make 命令](operations.md)
- [架构与配置](../reference/configuration.md)
- [参与贡献](../CONTRIBUTING.md)
