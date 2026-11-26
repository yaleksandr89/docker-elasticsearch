# Política de seguridad

## Elegir idioma

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| [Русский](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/.github/SECURITY.md) | [English](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/en/SECURITY.md) | **Español** | [中文](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/zh/SECURITY.md) | [Français](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/fr/SECURITY.md) | [Deutsch](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/de/SECURITY.md) |

## Versiones compatibles

Se consideran correcciones de seguridad para el estado actual de `master` y la última versión publicada. Las versiones anteriores pueden tener otra configuración de red; compruebe la compatibilidad de los datos antes de actualizar.

| Versión | Compatible |
|---|---|
| `master` | Sí |
| Última versión publicada | Sí |

## Límites de seguridad del laboratorio

Este es un laboratorio local de aprendizaje con datos sintéticos, no un despliegue de producción. En la configuración actual Elasticsearch funciona sin autenticación ni TLS; por defecto solo Nginx se publica en `127.0.0.1`, y los puertos internos de Elasticsearch y Kibana no se publican en el host. Con `WITH_EXTERNAL_NETWORK=1`, los miembros de la red Docker de confianza seleccionada acceden a Elasticsearch sin autenticación. Es un comportamiento intencionado, no una vulnerabilidad por sí solo. No conecte redes no confiables ni use datos reales.

Entre los problemas de seguridad se incluyen:

- publicación no prevista de servicios fuera de loopback o conexión a una red externa sin activación explícita;
- elusión de las restricciones previstas de enrutamiento de Nginx o exposición de archivos internos o configuración;
- tratamiento inseguro de parámetros o rutas que provoque ejecución de comandos o modificación de datos ajenos;
- eliminación, sobrescritura o divulgación no prevista de datos durante las operaciones del laboratorio;
- problemas de imágenes, plugins o CI que afecten a la seguridad de este proyecto.

Comunique errores ordinarios en [GitHub Issues](https://github.com/yaleksandr89/docker-elasticsearch/issues), preguntas e ideas en [GitHub Discussions](https://github.com/yaleksandr89/docker-elasticsearch/discussions). Si el problema está en un componente upstream, indique su versión exacta y el impacto en el laboratorio; informe también de los defectos del propio componente a sus mantenedores según sus reglas.

## Cómo informar de una vulnerabilidad

Se prefiere GitHub Private Vulnerability Reporting: abra **Security and quality → Report a vulnerability**. Si no está disponible, solicite un canal privado en GitHub Discussions sin publicar detalles técnicos de la vulnerabilidad.

No publique contraseñas, tokens, configuraciones locales o de producción, datos reales, logs completos, exploits funcionales ni detalles sensibles antes de la divulgación coordinada. Utilice solo datos sintéticos o fragmentos saneados.

## Qué incluir en el informe

- Release, branch o commit afectado y versiones de Elasticsearch, Kibana, Nginx, Docker y Compose cuando sean pertinentes.
- Modo de ejecución (local o integración), límite de acceso previsto e impacto posible.
- Pasos mínimos de reproducción y comportamiento esperado y real.
- Fragmentos saneados de solicitudes, respuestas o logs y una posible solución, si se conoce.

## Gestión del informe

Los informes se revisan según la disponibilidad; no se promete un SLA fijo. Coordine la divulgación con el mantenedor. Una vez confirmado el problema, las correcciones y la información sobre versiones afectadas se publican mediante divulgación coordinada. No se declara un programa de recompensas por vulnerabilidades.
