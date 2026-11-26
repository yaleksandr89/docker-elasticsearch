# Diagnostic

## Choisir la langue

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| [Русский](../../ru/guides/troubleshooting.md) | [English](../../en/guides/troubleshooting.md) | [Español](../../es/guides/troubleshooting.md) | [中文](../../zh/guides/troubleshooting.md) | **Sélectionné** | [Deutsch](../../de/guides/troubleshooting.md) |

Commencez par la configuration résolue, l’état des conteneurs et les journaux. Retirez identifiants, jetons, données et noms internes avant de partager la sortie. Ces commandes utilisent le mode local. Pour une intégration, ajoutez `WITH_EXTERNAL_NETWORK=1` à Make et `-f docker-compose.external.yml` à Compose.

[Premiers pas](getting-started.md)

```bash
make config
docker compose --env-file .docker.env -f docker-compose.yml ps -a
make log elasticsearch
make log kibana
make log nginx
```

## Erreur de réseau externe

Un réseau externe manquant empêche le démarrage uniquement en mode intégration. Comparez `EXTERNAL_NETWORK` à `docker network ls`, puis lancez `docker network inspect` avec le nom réel. Confirmez les membres avec le propriétaire. Préservez les réseaux des autres projets. La capture ci-dessous date de la version 6.8.

```bash
docker network ls
```

![Erreur de réseau externe](../../../assets/make-up-error.png) (6.8)

## Ports, domaines et 502/503

Si le port est occupé, choisissez un `NGINX_PORT` libre et mettez à jour les URL et les arguments `--resolve`. Les ports internes 9200 et 5601 sont fixes. Si curl fonctionne seul, vérifiez le fichier hosts de la machine du navigateur et l’exclusion du proxy pour les deux domaines. Un Host inconnu renvoie HTTP 404. Pour 502/503, vérifiez l’état et les journaux du service en amont. Compose attend un contrôle HTTP borné d’Elasticsearch. Kibana est prêt lorsque `/api/status` renvoie `status.overall.level: available`. En cas d’échec du contrôle Elasticsearch, commencez par ses journaux. Appliquez les changements d’image avec `make build` et de configuration avec `make up`, ou faites `down` puis `up` en gardant les montages. `restart` conserve la configuration actuelle.

```bash
curl --noproxy '*' --resolve elastic.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 http://elastic.local:8080/
curl --noproxy '*' --resolve elastic.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 'http://elastic.local:8080/_cluster/health?pretty'
curl --noproxy '*' --resolve elastic.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 'http://elastic.local:8080/_cat/plugins?v'
curl --noproxy '*' --resolve kibana.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 http://kibana.local:8080/api/status
```

## Construction, plugins et ressources

En cas d’échec de construction, vérifiez l’accès aux registres officiels et au téléchargement des extensions. Elasticsearch et Kibana doivent avoir la même version. `_cat/plugins` doit montrer `analysis-icu` et `analysis-phonetic` à cette version. Pour un échec du démarrage, vérifiez le disque, la mémoire Docker, les messages OOM, `vm.max_map_count` et les [droits des deux paires UID/GID](getting-started.md) sur les chemins utilisés. Pour une erreur d’analyse, lisez la réponse API et contrôlez `config/analysis/synonyms.txt`. Examinez les règles invalides avant de modifier le comportement avec `lenient`.

## Documentation

- [Premiers pas](getting-started.md)
- [Exercices de recherche et d’analyse de texte](search-lab.md)
- [Exploitation et commandes Make](operations.md)
- [Architecture et configuration](../reference/configuration.md)
- [Contribuer](../CONTRIBUTING.md)
