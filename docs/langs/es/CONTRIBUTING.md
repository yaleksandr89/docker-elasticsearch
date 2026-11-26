# Contribuir

## Elegir idioma

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| [Русский](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/.github/CONTRIBUTING.md) | [English](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/en/CONTRIBUTING.md) | **Seleccionado** | [中文](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/zh/CONTRIBUTING.md) | [Français](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/fr/CONTRIBUTING.md) | [Deutsch](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/de/CONTRIBUTING.md) |

Informe errores reproducibles en Issues y preguntas/ideas en Discussions. No publique datos reales, configuración local, contraseñas ni detalles de vulnerabilidades. Acuerde cambios importantes con el propietario primero.

- Errores reproducibles: [GitHub Issues](https://github.com/yaleksandr89/docker-elasticsearch/issues).
- Preguntas e ideas: [GitHub Discussions](https://github.com/yaleksandr89/docker-elasticsearch/discussions).

Conserve comandos Make, nombres de configuración, compatibilidad de datos y finalidad. Cambios de imágenes, red, puertos, auth/TLS y almacenamiento requieren decisión separada. Pruebe en copia nueva con datos sintéticos, contenedores, puerto y proyecto únicos; no toque el laboratorio activo.

## Comprobaciones

CI se ejecuta para push y pull request a `master` y manualmente desde Actions. `quality` comprueba sintaxis de scripts, fixtures y Compose resuelto; `docker-smoke` construye un laboratorio aislado con versiones fijas y comprueba HTTP por ambos hosts virtuales, plugins y búsqueda. Solo los resultados CI confirman el éxito.

```bash
bash -n docker-configs/nginx/start-nginx.sh
python3 tests/check-fixtures.py
python3 tests/test-runtime-contract.py
```

Make usa `WITH_EXTERNAL_NETWORK=0` por defecto. Para la integración, indique una red de confianza existente en `EXTERNAL_NETWORK` y pase `WITH_EXTERNAL_NETWORK=1` en cada comando Make. Solo Elasticsearch se conecta a ella. Sus miembros acceden sin contraseña por el nombre del contenedor y el puerto 9200. Compose conserva la red externa al parar.

## Pull Request

Cree una rama temática desde `master` y use Conventional Commits firmados con descripción rusa. En PR indique motivo, cambio, impacto en datos/seguridad y comprobaciones reales. Sincronice seis idiomas; no debilite checks para obtener CI verde.

## Documentación

- [Primeros pasos](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/es/guides/getting-started.md)
- [Práctica de búsqueda y análisis de texto](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/es/guides/search-lab.md)
- [Operación y comandos Make](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/es/guides/operations.md)
- [Diagnóstico](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/es/guides/troubleshooting.md)
- [Arquitectura y configuración](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/es/reference/configuration.md)
