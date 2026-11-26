# 搜索与文本分析练习

## 选择语言

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| [Русский](../../ru/guides/search-lab.md) | [English](../../en/guides/search-lab.md) | [Español](../../es/guides/search-lab.md) | **已选** | [Français](../../fr/guides/search-lab.md) | [Deutsch](../../de/guides/search-lab.md) |

目标：创建独立练习索引，理解 `text` 与 `keyword` 的差别，比较 Query DSL、分析器与聚合。仅在指南中的隔离本地环境运行。数据为合成数据，ID 1–3。下文为预期结果，并非已执行记录。

[入门](getting-started.md)

## 创建索引并加载数据

[`products-index.json`](../../../examples/products-index.json) · [`products.ndjson`](../../../examples/products.ndjson)

Mapping 定义字段类型。`title` 为分析文本，带独立同义词搜索分析器；`title.folded` 为 Unicode folding 多字段，`brand.sound` 为语音多字段，`category` 为过滤和聚合的精确值，`price` 为数字，`in_stock` 为布尔值。练习索引包含一个主分片、零副本。

在仓库根目录确认 `es-lab-products` 不存在（HTTP 404）。若已存在，不要覆盖他人的文档，先确认索引归属。`PUT` 使用显式 mapping 创建索引；`_bulk` 接受以换行结尾的 NDJSON。`refresh=wait_for` 等待记录可被搜索。检查 `acknowledged: true`、bulk 的 `errors: false` 和计数 3。

```bash
es() {
    curl --noproxy '*' --resolve elastic.local:8080:127.0.0.1 --fail --silent --show-error --max-time 30 "$@"
}
status=$(curl --noproxy '*' --resolve elastic.local:8080:127.0.0.1 --silent --show-error --max-time 10 --head --output /dev/null --write-out '%{http_code}' http://elastic.local:8080/es-lab-products)
test "$status" = 404
```

```bash
test "$status" = 404 && es -X PUT -H 'Content-Type: application/json' --data-binary @docs/examples/products-index.json http://elastic.local:8080/es-lab-products
```

仅在 `acknowledged: true` 后继续，创建索引失败时停止。Bulk 使用 `create`：重复加载不会覆盖已有 ID，但可能部分失败（检查 `errors` 和 `items`）。

```bash
es -X POST -H 'Content-Type: application/x-ndjson' --data-binary @docs/examples/products.ndjson 'http://elastic.local:8080/es-lab-products/_bulk?refresh=wait_for'
es 'http://elastic.local:8080/es-lab-products/_count?pretty'
```

## Query DSL：搜索、过滤与聚合

在 Kibana Dev Tools → Console 中逐个执行以下代码块。查看 `hits.hits`（文档）、`_score`（相关性分数）及 `aggregations`。同分结果顺序不保证。

`match` 分析查询；搜索同义词 `laptop, notebook` 应返回文档 1 和 2。

```http
GET es-lab-products/_search
{"query":{"match":{"title":"laptop"}}}
```

`term` 匹配精确 `keyword`，不分析字符串。预期文档 1 和 2。`text` 上的 `term` 不能替代全文 `match`。

```http
GET es-lab-products/_search
{"query":{"term":{"category":"computers"}}}
```

`bool.must` 参与相关性评分，`filter` 限制结果而不评分。库存中价格不超过 1000 的笔记本预期仅文档 1。

```http
GET es-lab-products/_search
{
  "query": {
    "bool": {
      "must": {"match": {"title": "laptop"}},
      "filter": [
        {"term": {"in_stock": true}},
        {"range": {"price": {"lte": 1000}}}
      ]
    }
  }
}
```

`terms` 按 `category` 分组。`size: 0` 仅返回元数据与聚合，预期 `computers: 2`、`audio: 1`。

```http
GET es-lab-products/_search
{"size":0,"aggs":{"categories":{"terms":{"field":"category"}}}}
```

## 文本分析原理

```mermaid
flowchart LR
    A["输入字符串"] --> B["分词"]
    B --> C["词元过滤器"]
    C --> D["搜索词元"]
```

分析器将字符串转换为词元。索引时词元写入倒排索引，搜索时用于匹配。`_analyze` 无需添加文档即可查看结果。搜索时同义词扩展查询，不修改原始 `_source`。

```http
POST es-lab-products/_analyze
{"analyzer":"lab_search","text":"laptop"}
```

ICU folding 规范化 Unicode，包括变音符号。比较 `Café` 和 `cafe` 的词元，再搜索 `title.folded`，预期文档 3。这不是通用语言翻译。

```http
POST es-lab-products/_analyze
{"analyzer":"lab_icu","text":["Café","cafe"]}

GET es-lab-products/_search
{"query":{"match":{"title.folded":"cafe"}}}
```

Double Metaphone 编码发音。`Smith` 和 `Smyth` 应通过 `brand.sound` 匹配（1 和 2）。保留普通 `brand` 字段独立搜索：语音匹配可能误匹配且依赖语言。

```http
POST es-lab-products/_analyze
{"analyzer":"lab_sound","text":["Smith","Smyth"]}

GET es-lab-products/_search
{"query":{"match":{"brand.sound":"Smith"}}}
```

项目词典 `analysis/synonyms.txt` 在构建时复制到 Elasticsearch 配置目录，不会自动应用到标准分析器。通过 `_analyze` 显式验证，`russia` 的词元中应含 `россия`。它是地名变体词典，并非通用语言词典，可能需编辑审查。多词同义词应在搜索阶段使用 `synonym_graph`。修改文件需重建镜像并适当应用分析器变更，不会自动重建索引。

```http
POST /_analyze
{
  "tokenizer": "standard",
  "filter": ["lowercase", {"type":"synonym_graph","synonyms_path":"analysis/synonyms.txt"}],
  "text": "russia"
}
```

## Kibana Discover

在 Kibana Discover 中为 `es-lab-products` 创建 data view，不选择时间字段（mapping 无 timestamp）。打开文档，添加 `category`、`price`、`in_stock`，比较过滤与 Query DSL。菜单名称可能随版本变化。

## 结束练习

可保留索引继续查询。只有确认该索引由您在此一次性实验环境创建且不再需要时，才执行下列命令；它删除全部文档和 mapping，无自动恢复。不要使用通配符或在其他集群执行。

```http
DELETE es-lab-products
```

## 官方文档

- [Match query](https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-match-query)
- [ICU analysis](https://www.elastic.co/docs/reference/elasticsearch/plugins/analysis-icu)
- [Phonetic filter](https://www.elastic.co/docs/reference/elasticsearch/plugins/analysis-phonetic-token-filter)
- [Synonym graph](https://www.elastic.co/docs/reference/text-analysis/analysis-synonym-graph-tokenfilter)

## 文档

- [入门](getting-started.md)
- [运维与 Make 命令](operations.md)
- [故障排查](troubleshooting.md)
- [架构与配置](../reference/configuration.md)
- [参与贡献](../CONTRIBUTING.md)
