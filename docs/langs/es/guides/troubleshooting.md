# Diagnóstico

## Elegir idioma

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| [Русский](../../ru/guides/troubleshooting.md) | [English](../../en/guides/troubleshooting.md) | **Seleccionado** | [中文](../../zh/guides/troubleshooting.md) | [Français](../../fr/guides/troubleshooting.md) | [Deutsch](../../de/guides/troubleshooting.md) |

Empiece por la configuración resuelta, el estado y los registros. Quite credenciales, tokens, datos y nombres internos antes de compartir la salida. Los comandos usan el modo local. Para integración, añada `WITH_EXTERNAL_NETWORK=1` a Make y `-f docker-compose.external.yml` a Compose.

[Primeros pasos](getting-started.md)

```bash
make config
docker compose --env-file .docker.env -f docker-compose.yml ps -a
make log elasticsearch
make log kibana
make log nginx
```

## Error de red externa

Una red externa ausente solo impide arrancar en modo de integración. Compare `EXTERNAL_NETWORK` con `docker network ls` y ejecute `docker network inspect` con el nombre real. Confirme los miembros con el propietario. Respete las redes de otros proyectos. La captura es histórica (6.8).

```bash
docker network ls
```

![Error de red externa](../../../assets/make-up-error.png) (6.8)

## Puertos, dominios y 502/503

Si el puerto está ocupado, elija un `NGINX_PORT` libre y actualice todas las URL y argumentos `--resolve`. Los puertos internos 9200 y 5601 son fijos. Si funciona curl pero falla el navegador, compruebe su archivo hosts y la exclusión del proxy para ambos dominios. Un Host desconocido devuelve HTTP 404. Para 502/503, revise el estado y los registros del servicio. Compose espera una comprobación HTTP acotada de Elasticsearch. Kibana está listo si `/api/status` indica `status.overall.level: available`. Si Elasticsearch agota los intentos, diagnostique sus registros. Aplique cambios de imagen con `make build` y de configuración con `make up`, o haga `down` seguido de `up` conservando los montajes. `restart` mantiene la configuración actual.

```bash
curl --noproxy '*' --resolve elastic.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 http://elastic.local:8080/
curl --noproxy '*' --resolve elastic.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 'http://elastic.local:8080/_cluster/health?pretty'
curl --noproxy '*' --resolve elastic.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 'http://elastic.local:8080/_cat/plugins?v'
curl --noproxy '*' --resolve kibana.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 http://kibana.local:8080/api/status
```

## Construcción, plugins y recursos

Si falla la construcción, compruebe el acceso a los registros oficiales y a las descargas de plugins. Elasticsearch y Kibana deben tener la misma versión. `_cat/plugins` debe mostrar `analysis-icu` y `analysis-phonetic` con esa versión. Para errores de inicio, compruebe disco, memoria de Docker, avisos OOM, `vm.max_map_count` y los [permisos de ambos UID/GID](getting-started.md) en las rutas reales. Para errores del analizador, lea la respuesta de la API y revise `config/analysis/synonyms.txt`. Investigue reglas inválidas antes de cambiar el comportamiento con `lenient`.

## Documentación

- [Primeros pasos](getting-started.md)
- [Práctica de búsqueda y análisis de texto](search-lab.md)
- [Operación y comandos Make](operations.md)
- [Arquitectura y configuración](../reference/configuration.md)
- [Contribuir](../CONTRIBUTING.md)
