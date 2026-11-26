# Operación y comandos Make

## Elegir idioma

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| [Русский](../../ru/guides/operations.md) | [English](../../en/guides/operations.md) | **Seleccionado** | [中文](../../zh/guides/operations.md) | [Français](../../fr/guides/operations.md) | [Deutsch](../../de/guides/operations.md) |

El laboratorio usa el modo local por defecto. Prepare los directorios según la guía de inicio antes de arrancar.

[Primeros pasos](getting-started.md)

## Inicio rápido

```bash
make help
make init
make config
```

`COMPOSE_COMMAND` = `docker compose`.

```bash
make COMPOSE_COMMAND='docker compose' config
```

| Comando | Efecto |
|---|---|
| `make help` | Muestra la ayuda bilingüe. |
| `make init` | Crea `.docker.env` si falta y los directorios de `*_DATA_DIR`; conserva la configuración existente. |
| `make pull` | Descarga imágenes base oficiales según la configuración Make; no reconstruye las imágenes locales. |
| `make build` | Construye imágenes sin caché. |
| `make config` | Muestra la configuración Compose resuelta sin iniciar servicios. |
| `make up` | Compose inicia Kibana en segundo plano tras la comprobación HTTP de Elasticsearch. Revise /api/status para confirmar que Kibana está listo. Adapte las URL al dominio y puerto elegidos. |
| `make down` | Detiene y elimina contenedores y red gestionada, no el directorio de datos del host. |
| `make reset` | Ejecuta `down` y después `up -d`, recreando los contenedores y conservando datos e índices. |
| `make restart` | Reinicia contenedores existentes; no aplica cambios de imagen, Compose o variables. |
| `make in elasticsearch` | Inicia Bash en el servicio indicado: `elasticsearch`, `kibana`, `nginx`. |
| `make log kibana` | Muestra logs del servicio; no sigue el flujo automáticamente. |

```bash
docker compose --env-file .docker.env -f docker-compose.yml ps
make log elasticsearch
make restart
make down
```

## Conectar otro proyecto

Localice la red de confianza existente de la aplicación con `docker network ls` y compruebe sus miembros con `docker network inspect`. Indique su nombre real en `EXTERNAL_NETWORK` en `.docker.env`. Compose combina el archivo base y la extensión, conserva `backend` y conecta solo Elasticsearch a la red adicional. Desde el contenedor de la aplicación use `http://docker-elasticsearch-es:9200` o el nombre real de `ELASTIC_CONTAINER`. Todos los miembros acceden sin autenticación. Use la misma opción en los comandos posteriores, incluida la parada.

```bash
docker network ls
make config WITH_EXTERNAL_NETWORK=1
make up WITH_EXTERNAL_NETWORK=1
```

```bash
make down WITH_EXTERNAL_NETWORK=1
```

Para cambiar de modo, ejecute `down` con los archivos o la opción anteriores, conserve ambas rutas de datos y ejecute `up` con la nueva configuración. La red externa queda con su propietario. Use solo la red y rutas acordadas. `restart` conserva la red de los contenedores existentes.

```bash
docker compose --env-file .docker.env -f docker-compose.yml -f docker-compose.external.yml config
docker compose --env-file .docker.env -f docker-compose.yml -f docker-compose.external.yml up -d
docker compose --env-file .docker.env -f docker-compose.yml -f docker-compose.external.yml down
```

## Persistencia y actualizaciones

Ambos montajes sobreviven a la recreación. Kibana guarda la mayoría de objetos en índices de sistema de Elasticsearch. Antes de parar el laboratorio anterior, revise `/usr/share/kibana/data` en su contenedor y guarde aparte los archivos locales necesarios.

Make carece de objetivos automáticos de limpieza, instantáneas y restauración. Copiar el directorio de Elasticsearch en ejecución es una copia de seguridad poco fiable. Antes de parar, anote versiones activas, nombres, puerto y ambos montajes. Si procede, cree una [instantánea](https://www.elastic.co/docs/deploy-manage/tools/snapshot-and-restore), pruebe la restauración en otro laboratorio y verifique los plugins para cada paso de la [ruta admitida](https://www.elastic.co/docs/deploy-manage/upgrade). Conserve el `ELASTIC_CONTAINER` configurado para clientes existentes, por ejemplo `global-elasticsearch`. Cambie el puerto antiguo 80 a 8080 solo si así lo decide. La actualización requiere una decisión del propietario.

Pare el laboratorio anterior con su configuración original. Si desconoce la versión de origen, compruebe primero la compatibilidad. Es peligroso volver a una versión anterior con datos ya actualizados.

## Comprobaciones

CI se ejecuta para push y pull request a `master` y manualmente desde Actions. `quality` comprueba sintaxis de scripts, fixtures y Compose resuelto; `docker-smoke` construye un laboratorio aislado con versiones fijas y comprueba HTTP por ambos hosts virtuales, plugins y búsqueda. Solo los resultados CI confirman el éxito.

Python 3 solo es necesario para verificar fixtures y CI.

```bash
bash -n docker-configs/nginx/start-nginx.sh
python3 tests/check-fixtures.py
python3 tests/test-runtime-contract.py
```

Ejecute `tests/smoke.py` solo en una copia desechable. En local requiere `/tmp/docker-elasticsearch-review.XXXXXXXX/candidate` y el proyecto `elastic-learning-test-xxxxxxxx`, con los mismos ocho caracteres alfanuméricos en minúsculas en el nombre. Antes de crear el índice comprueba etiquetas, imágenes, red, puerto y ambos montajes. `--persisted` verifica los documentos creados previamente.

## Documentación

- [Primeros pasos](getting-started.md)
- [Práctica de búsqueda y análisis de texto](search-lab.md)
- [Diagnóstico](troubleshooting.md)
- [Arquitectura y configuración](../reference/configuration.md)
- [Contribuir](../CONTRIBUTING.md)
