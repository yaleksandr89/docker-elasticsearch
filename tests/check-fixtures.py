"""Validate the published training fixture and the resolved local Compose model."""
import json
import os
import sys
from pathlib import Path

if not __debug__:
    raise SystemExit('Run checks without optimization.')

root = Path(__file__).resolve().parents[1]
index = json.loads((root / 'docs/examples/products-index.json').read_text())
lines = (root / 'docs/examples/products.ndjson').read_text().splitlines()
assert len(lines) == 6
records = [json.loads(line) for line in lines]
assert [r['create']['_id'] for r in records[::2]] == ['1', '2', '3']
assert all(set(r) == set(index['mappings']['properties']) for r in records[1::2])
assert (root / 'docs/examples/products.ndjson').read_bytes().endswith(b'\n')
if len(sys.argv) == 2:
    # Before building or starting the isolated smoke project.
    model = json.loads(Path(sys.argv[1]).read_text())
    project = os.environ['COMPOSE_PROJECT_NAME']
    assert model['name'] == project and set(model['networks']) == {'backend'}
    assert model['networks']['backend']['name'] == project + '_backend'
    assert not model['networks']['backend'].get('external')
    assert model['networks']['backend']['driver'] == 'bridge'
    services = model['services']
    assert set(services) == {'elasticsearch', 'kibana', 'nginx'}
    for service, key, suffix in [('elasticsearch', 'ELASTIC', 'es'), ('kibana', 'KIBANA', 'kibana'),
                                  ('nginx', 'NGINX', 'nginx')]:
        data = services[service]
        assert data['container_name'] == project + '-' + suffix
        assert set(data['networks']) == {'backend'}
        assert data['build']['context'] == str(root / 'docker-configs' / service)
        assert data['build']['args'][key + '_VERSION'] == ('1.30.8-trixie' if service == 'nginx' else '9.5.7')
        if service == 'nginx':
            port, = data['ports']
            assert (port['host_ip'], port['published'], port['target']) == ('127.0.0.1', os.environ['NGINX_PORT'], 80)
            assert not data.get('volumes')
        else:
            assert not data.get('ports')
            volume, = data['volumes']
            assert volume['type'] == 'bind' and volume['source'] == str(root / 'data' / service)
            assert Path(volume['source']).resolve() == root / 'data' / service
            assert volume['target'] == f'/usr/share/{service}/data'
    env = services['kibana']['environment']
    assert env['SERVER_NAME'] == 'kibana.local'
    assert env['SERVER_PUBLICBASEURL'] == 'http://kibana.local:' + os.environ['NGINX_PORT']
    assert json.loads(env['ELASTICSEARCH_HOSTS']) == ['http://elasticsearch:9200']
print('Training fixtures and requested model checks passed.')
