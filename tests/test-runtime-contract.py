"""Check Make and both Compose models in a temporary copy with synthetic inputs."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

if not __debug__:
    raise SystemExit('Run contract checks without Python optimization.')

root = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as directory:
    work = Path(directory)
    for name in ('Makefile', '.docker.env.example', 'docker-compose.yml', 'docker-compose.external.yml'):
        shutil.copy(root / name, work)
    shutil.copytree(root / 'docker-configs', work / 'docker-configs')
    env = {'PATH': os.environ['PATH'], 'HOME': directory}

    def run(*args, ok=True):
        result = subprocess.run(args, cwd=work, env=env, text=True, capture_output=True, timeout=30)
        if (result.returncode == 0) != ok:
            raise RuntimeError(f'{args}: exit {result.returncode}\n{result.stderr}')
        return result.stdout

    # Only Bash is available on PATH. Run GNU Make by its absolute path.
    make = shutil.which('make')
    bash = shutil.which('bash')
    assert make and bash
    bin_dir = work / 'bin'
    bin_dir.mkdir()
    (bin_dir / 'bash').symlink_to(bash)
    before_help = sorted(work.rglob('*'))
    help_output = subprocess.check_output(
        [make, 'help'], cwd=work, env={**env, 'PATH': str(bin_dir)}, text=True, timeout=10)
    for target in ('help', 'init', 'pull', 'build', 'config', 'up', 'down', 'reset', 'restart', 'in SERVICE', 'log SERVICE'):
        assert any(line.startswith(f'make {target} ') and ' / ' in line for line in help_output.splitlines())
    for text in ('Показать справку', 'WITH_EXTERNAL_NETWORK=0|1', 'EXTERNAL_NETWORK', 'without authentication',
                 'make in elasticsearch', 'make log kibana', 'elasticsearch, kibana, nginx'):
        assert text in help_output
    for target in ('config', 'up', 'down'):
        assert f'make {target} WITH_EXTERNAL_NETWORK=1' in help_output
    assert sorted(work.rglob('*')) == before_help
    assert not (work / '.docker.env').exists() and not (work / 'data').exists()

    run('make', 'init')
    settings = work / '.docker.env'
    original = settings.read_text()
    assert original == (work / '.docker.env.example').read_text()
    sentinel = work / 'data/kibana/test'
    sentinel.write_text('keep')
    settings.write_text(original + '\n# preserve\n')
    run('make', 'init')
    assert sentinel.read_text() == 'keep' and settings.read_text() == original + '\n# preserve\n'
    # An ambient override must never add this service.
    (work / 'compose.override.yaml').write_text('services: {other: {image: invalid}}')
    run('make', 'config')
    args = ['docker', 'compose', '--env-file', '.docker.env', '-f', 'docker-compose.yml']
    base = json.loads(run(*args, 'config', '--format', 'json'))
    external = json.loads(run(*args, '-f', 'docker-compose.external.yml', 'config', '--format', 'json'))
    assert set(base['networks']) == {'backend'}
    assert base['networks']['backend']['driver'] == 'bridge'
    assert not base['networks']['backend'].get('external')
    extra_network = external['networks'].pop('external_network')
    assert extra_network['external'] and extra_network['name'] == 'external_network'
    assert 'external_network' in external['services']['elasticsearch']['networks']
    del external['services']['elasticsearch']['networks']['external_network']
    assert external == base
    assert 'external: true' in run('make', 'config', 'WITH_EXTERNAL_NETWORK=1')
    services = base['services']
    assert set(services) == {'nginx', 'kibana', 'elasticsearch'}
    for service, data in services.items():
        assert set(data['networks']) == {'backend'}
        if service != 'nginx':
            assert not data.get('ports')
            mount, = data['volumes']
            assert (mount['type'], mount['source'], mount['target']) == (
                'bind', str(work / 'data' / service), f'/usr/share/{service}/data')
    port, = services['nginx']['ports']
    assert (port['host_ip'], str(port['published']), port['target'], port['protocol']) == ('127.0.0.1', '8080', 80, 'tcp')
    assert services['kibana']['environment']['SERVER_PUBLICBASEURL'] == 'http://kibana.local:8080'
    assert len({s['container_name'] for s in services.values()}) == 3
    for service, key, version in [('elasticsearch', 'ELASTIC', '9.5.7'), ('kibana', 'KIBANA', '9.5.7'),
                                  ('nginx', 'NGINX', '1.30.8-trixie')]:
        assert services[service]['build']['args'][key + '_VERSION'] == version
    for setting in ('WITH_EXTERNAL_NETWORK=yes', 'ELASTIC_VERSION=latest', 'NGINX_VERSION=lates',
                    'KIBANA_VERSION=9.5.6', 'ELASTIC_DOMAIN=KIBANA.LOCAL', 'ELASTIC_DOMAIN=*.local',
                    'ELASTIC_PORT=9300', 'NGINX_PORT=0', 'NGINX_PORT=', 'NGINX_PORT=invalid',
                    'NGINX_PORT=65536', 'KIBANA_DATA_DIR='):
        run('make', 'config', setting, ok=False)
    settings.write_text(original.replace('NGINX_PORT=8080\n', ''))
    run('make', 'config', ok=False)
    settings.write_text(original.replace('NGINX_PORT=8080', 'NGINX_PORT=18080'))
    run('make', 'config')
    moved = json.loads(run(*args, 'config', '--format', 'json'))['services']
    assert moved['nginx']['ports'] == [{**port, 'published': '18080'}]
    assert moved['kibana']['environment']['SERVER_PUBLICBASEURL'] == 'http://kibana.local:18080'
    dry = run('make', '-n', '-j4', 'reset', 'WITH_EXTERNAL_NETWORK=1').splitlines()
    assert dry[-2:] == ['docker compose --env-file .docker.env -f docker-compose.yml -f docker-compose.external.yml ' + action
                        for action in ('down', 'up -d')]
print('Both Compose models, Make validation, init preservation and reset order passed.')
