# Contribuer

## Choisir la langue

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| [Русский](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/.github/CONTRIBUTING.md) | [English](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/en/CONTRIBUTING.md) | [Español](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/es/CONTRIBUTING.md) | [中文](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/zh/CONTRIBUTING.md) | **Sélectionné** | [Deutsch](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/de/CONTRIBUTING.md) |

Signalez les bugs reproductibles via Issues, questions et idées via Discussions. Ne publiez pas de données réelles, configuration locale, mots de passe ou détails de vulnérabilités. Convenez d’abord des changements importants avec le propriétaire.

- Bugs reproductibles : [GitHub Issues](https://github.com/yaleksandr89/docker-elasticsearch/issues).
- Questions et idées : [GitHub Discussions](https://github.com/yaleksandr89/docker-elasticsearch/discussions).
- Vulnérabilités : [politique de sécurité](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/fr/SECURITY.md).

Préservez les commandes Make, les noms de configuration, la compatibilité des données et l’objectif du laboratoire. Les changements d’images, réseau, ports, auth/TLS et stockage exigent une décision séparée. Testez dans une copie neuve avec données synthétiques, conteneurs, port et projet uniques ; ne touchez pas au laboratoire actif.

## Vérifications

CI s’exécute sur push et pull request vers `master`, ainsi que manuellement via Actions. `quality` vérifie la syntaxe des scripts, les fixtures et Compose résolu ; `docker-smoke` construit un laboratoire isolé à versions fixes et vérifie HTTP via deux hôtes virtuels, plugins et recherche. Seuls les résultats CI établissent le succès.

```bash
bash -n docker-configs/nginx/start-nginx.sh
python3 tests/check-fixtures.py
python3 tests/test-runtime-contract.py
```

Make utilise `WITH_EXTERNAL_NETWORK=0` par défaut. Pour une intégration, indiquez un réseau de confiance existant dans `EXTERNAL_NETWORK` et passez `WITH_EXTERNAL_NETWORK=1` à chaque commande Make. Seul Elasticsearch le rejoint. Ses membres y accèdent sans mot de passe par le nom du conteneur sur le port 9200. Compose conserve ce réseau à l’arrêt.

## Pull Request

Créez une branche thématique depuis `master`, utilisez des Conventional Commits signés avec description russe. Dans la PR indiquez raison, changement, impact données/sécurité et vérifications réelles. Synchronisez six langues ; n’affaiblissez pas les contrôles pour un CI vert.

## Documentation

- [Premiers pas](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/fr/guides/getting-started.md)
- [Exercices de recherche et d’analyse de texte](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/fr/guides/search-lab.md)
- [Exploitation et commandes Make](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/fr/guides/operations.md)
- [Diagnostic](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/fr/guides/troubleshooting.md)
- [Architecture et configuration](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/fr/reference/configuration.md)
