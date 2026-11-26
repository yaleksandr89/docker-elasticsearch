"""Run only on a freshly created isolated CI stack with synthetic data."""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

root = Path(__file__).resolve().parents[1]
if not __debug__:
    raise SystemExit('Smoke safety checks require Python without optimization.')
project = os.environ['COMPOSE_PROJECT_NAME']
if os.environ.get('GITHUB_ACTIONS') == 'true':
    assert project == f"elastic-learning-ci-{os.environ['GITHUB_RUN_ID']}-{os.environ['GITHUB_RUN_ATTEMPT']}"
    assert root == Path(os.environ['RUNNER_TEMP']).resolve() / project
else:
    assert root.parent.parent == Path('/tmp') and root.name == 'candidate'
    match = re.fullmatch(r'docker-elasticsearch-review\.([a-zA-Z0-9]{8})', root.parent.name)
    assert match and project == 'elastic-learning-test-' + match[1].lower()

def docker(*args):
    return subprocess.check_output(['docker', '--context', 'default', *args], text=True, timeout=20).strip()

assert docker('context', 'inspect', 'default', '--format', '{{.Endpoints.docker.Host}}') == 'unix:///var/run/docker.sock'
port = int(os.environ['NGINX_PORT'])
base = f'http://127.0.0.1:{port}'
index = 'es-lab-products'
network = json.loads(docker('network', 'inspect', project + '_backend'))[0]
assert network['Labels']['com.docker.compose.project'] == project
assert network['Labels']['com.docker.compose.network'] == 'backend'
assert network['Driver'] == 'bridge'
expected_ids = set()
for service, suffix in [('elasticsearch', 'es'), ('kibana', 'kibana'), ('nginx', 'nginx')]:
    name = project + '-' + suffix
    container = json.loads(docker('inspect', name))[0]
    expected_ids.add(container['Id'])
    labels = container['Config']['Labels']
    assert labels['com.docker.compose.project'] == project and labels['com.docker.compose.service'] == service
    assert labels['com.docker.compose.project.working_dir'] == str(root)
    assert labels['com.docker.compose.project.config_files'] == str(root / 'docker-compose.yml')
    assert container['Image'] == docker('image', 'inspect', project + '-' + service, '--format', '{{.Id}}')
    networks = container['NetworkSettings']['Networks']
    assert set(networks) == {network['Name']} and networks[network['Name']]['NetworkID'] == network['Id']
    bindings = {k: v for k, v in container['NetworkSettings']['Ports'].items() if v}
    if service == 'nginx':
        assert bindings == {'80/tcp': [{'HostIp': '127.0.0.1', 'HostPort': str(port)}]}
        assert not container['Mounts']
        subprocess.run(['docker', '--context', 'default', 'exec', name, 'nginx', '-t'], check=True, timeout=10)
        version = subprocess.check_output(['docker', '--context', 'default', 'exec', name, 'nginx', '-v'],
                                          stderr=subprocess.STDOUT, text=True, timeout=10)
        assert version.strip() == 'nginx version: nginx/1.30.8'
    else:
        assert not bindings and docker('exec', name, 'id', '-u') == '1000'
        mount, = container['Mounts']
        assert mount['Type'] == 'bind' and mount['RW']
        assert mount['Destination'] == f'/usr/share/{service}/data'
        assert Path(mount['Source']).resolve() == root / 'data' / service
        if service == 'kibana':
            assert f'SERVER_PUBLICBASEURL=http://kibana.local:{port}' in container['Config']['Env']
assert set(network['Containers']) == expected_ids

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


opener = build_opener(ProxyHandler({}), NoRedirect())


def request(path, method='GET', body=None, host='elastic.local', content_type='application/json'):
    if isinstance(body, dict):
        body = json.dumps(body).encode()
    headers = {'Host': f'{host}:{port}', 'Content-Type': content_type}
    req = Request(base + path, data=body, headers=headers, method=method)
    with opener.open(req, timeout=10) as response:
        return json.load(response)


def wait(path, predicate, host='elastic.local'):
    deadline = time.monotonic() + 300
    last = None
    while time.monotonic() < deadline:
        try:
            last = request(path, host=host)
            if predicate(last):
                return last
        except HTTPError as error:
            with error:
                error.read()
                last = f'HTTP {error.code}'
        except (URLError, TimeoutError, ValueError) as error:
            last = str(error)
        time.sleep(5)
    raise RuntimeError(f'{host}{path} not ready: {last}')


info = wait('/', lambda value: 'version' in value)
assert info['version']['number'] == '9.5.7' and info['cluster_name'] == 'custom-cluster'
health = wait('/_cluster/health', lambda value: value['status'] in ('green', 'yellow'))
print('Cluster health:', health['status'])
kibana = wait('/api/status', lambda value: value['status']['overall']['level'] == 'available', 'kibana.local')
kibana_version = json.loads(docker('exec', project + '-kibana', 'cat', '/usr/share/kibana/package.json'))['version']
assert kibana_version == '9.5.7'
print('Kibana status:', kibana['status']['overall']['level'], kibana_version)
plugins = request('/_cat/plugins?format=json')
assert {'analysis-icu', 'analysis-phonetic'} == {p['component'] for p in plugins}
assert all(p['version'] == info['version']['number'] for p in plugins)
print('Cluster, plugins and Kibana ready:', info['cluster_name'], info['version']['number'], plugins, flush=True)
def expect_missing(path, host):
    try:
        request(path, 'HEAD', host=host)
    except HTTPError as error:
        with error:
            error.read()
            assert error.code == 404, (path, error.code)
    else:
        raise RuntimeError(f'Expected 404 for {host}{path}')


expect_missing('/', 'unknown.invalid')
if sys.argv[1:] == ['--persisted']:
    assert request('/' + index + '/_count')['count'] == 3
    fixture = [json.loads(line) for line in (root / 'docs/examples/products.ndjson').read_text().splitlines()]
    expected = {action['create']['_id']: doc for action, doc in zip(fixture[::2], fixture[1::2])}
    hits = request('/' + index + '/_search')['hits']['hits']
    assert {hit['_id']: hit['_source'] for hit in hits} == expected
    print('All three original documents survived recreation.')
    sys.exit(0)
assert len(sys.argv) == 1
expect_missing('/' + index, 'elastic.local')
assert request('/' + index, 'PUT', (root / 'docs/examples/products-index.json').read_bytes())['acknowledged']
bulk = request('/' + index + '/_bulk?refresh=wait_for', 'POST', (root / 'docs/examples/products.ndjson').read_bytes(), content_type='application/x-ndjson')
assert bulk['errors'] is False and [i['create']['status'] for i in bulk['items']] == [201] * 3
assert request('/' + index + '/_count')['count'] == 3


def search(query):
    return request('/' + index + '/_search', 'POST', query)


def ids(result):
    matched = {hit['_id'] for hit in result['hits']['hits']}
    print('Search IDs:', sorted(matched))
    return matched


assert ids(search({'query': {'match': {'title': 'laptop'}}})) == {'1', '2'}
assert ids(search({'query': {'term': {'category': 'computers'}}})) == {'1', '2'}
assert ids(search({'query': {'bool': {'must': {'match': {'title': 'laptop'}}, 'filter': [{'term': {'in_stock': True}}, {'range': {'price': {'lte': 1000}}}]}}})) == {'1'}
assert ids(search({'query': {'match': {'title.folded': 'cafe'}}})) == {'3'}
assert ids(search({'query': {'match': {'brand.sound': 'Smith'}}})) == {'1', '2'}
agg = search({'size': 0, 'aggs': {'categories': {'terms': {'field': 'category'}}}})
print('Category buckets:', agg['aggregations']['categories']['buckets'])
assert {b['key']: b['doc_count'] for b in agg['aggregations']['categories']['buckets']} == {'computers': 2, 'audio': 1}
def tokens(analyzer, text):
    result = request('/' + index + '/_analyze', 'POST', {'analyzer': analyzer, 'text': text})
    values = {item['token'] for item in result['tokens']}
    print(analyzer, text, sorted(values))
    return values


assert tokens('lab_icu', 'Café') == {'cafe'}
sounds = tokens('lab_sound', 'Smith')
assert sounds and sounds == tokens('lab_sound', 'Smyth')
assert tokens('lab_search', 'laptop') == {'laptop', 'notebook'}
# The dictionary is packaged but not automatically attached to an analyzer.
analysis = request('/_analyze', 'POST', {'tokenizer': 'standard', 'filter': ['lowercase', {'type': 'synonym_graph', 'synonyms_path': 'analysis/synonyms.txt'}], 'text': 'russia'})
print('Dictionary tokens:', [token['token'] for token in analysis['tokens']])
assert 'россия' in {token['token'] for token in analysis['tokens']}
print('Isolated Elasticsearch and Kibana smoke passed.')
