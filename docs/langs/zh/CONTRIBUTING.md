# 参与贡献

## 选择语言

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| [Русский](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/.github/CONTRIBUTING.md) | [English](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/en/CONTRIBUTING.md) | [Español](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/es/CONTRIBUTING.md) | **已选** | [Français](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/fr/CONTRIBUTING.md) | [Deutsch](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/de/CONTRIBUTING.md) |

可复现问题通过 Issues，疑问和想法通过 Discussions。不要发布真实数据、本地配置、密码或漏洞细节。重大变更先与维护者商定。

- 可复现的错误：[GitHub Issues](https://github.com/yaleksandr89/docker-elasticsearch/issues)。
- 问题和想法：[GitHub Discussions](https://github.com/yaleksandr89/docker-elasticsearch/discussions)。

保留 Make 命令、配置名、数据兼容性及环境用途。镜像、网络、端口发布、认证/TLS 与存储变更须单独决定。测试使用新副本、合成数据、唯一容器名、端口和项目名；不要触碰工作环境。

## 检查

CI 在 `master` 的 push、pull request 及 Actions 手动触发时运行。`quality` 检查启动脚本语法、练习 fixtures 和解析后的 Compose；`docker-smoke` 使用固定版本构建隔离环境，检查两个虚拟主机的 HTTP、插件及搜索。只有 CI 实际结果才能证明成功。

```bash
bash -n docker-configs/nginx/start-nginx.sh
python3 tests/check-fixtures.py
python3 tests/test-runtime-contract.py
```

Make 默认使用 `WITH_EXTERNAL_NETWORK=0`。集成时将 `EXTERNAL_NETWORK` 设为现有可信网络，并给每条 Make 命令传入 `WITH_EXTERNAL_NETWORK=1`。仅 Elasticsearch 加入该网络；成员可以通过容器名和 9200 端口免认证访问。停止时 Compose 保留外部网络。

## Pull Request

从 `master` 创建主题分支，使用带俄语描述的签名 Conventional Commits。在 PR 说明原因、变更、数据和安全影响及实际检查。同步六种语言，不得为 CI 通过而削弱检查。

## 文档

- [入门](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/zh/guides/getting-started.md)
- [搜索与文本分析练习](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/zh/guides/search-lab.md)
- [运维与 Make 命令](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/zh/guides/operations.md)
- [故障排查](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/zh/guides/troubleshooting.md)
- [架构与配置](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/zh/reference/configuration.md)
