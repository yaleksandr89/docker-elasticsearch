# Fehlerbehebung

## Sprache wählen

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| [Русский](../../ru/guides/troubleshooting.md) | [English](../../en/guides/troubleshooting.md) | [Español](../../es/guides/troubleshooting.md) | [中文](../../zh/guides/troubleshooting.md) | [Français](../../fr/guides/troubleshooting.md) | **Ausgewählt** |

Zuerst aufgelöste Konfiguration, Containerzustand und Protokolle prüfen. Vor der Weitergabe Zugangsdaten, Tokens, Daten und interne Namen entfernen. Die Befehle gelten lokal. Bei Integration Make um `WITH_EXTERNAL_NETWORK=1` und Compose um `-f docker-compose.external.yml` ergänzen.

[Erste Schritte](getting-started.md)

```bash
make config
docker compose --env-file .docker.env -f docker-compose.yml ps -a
make log elasticsearch
make log kibana
make log nginx
```

## Fehler externes Netzwerk

Ein fehlendes externes Netz verhindert den Start nur bei aktivierter Integration. `EXTERNAL_NETWORK` mit `docker network ls` abgleichen und `docker network inspect` mit dem tatsächlichen Namen ausführen. Mitglieder mit dem Eigentümer prüfen. Netze anderer Projekte unangetastet lassen. Das Bild stammt aus Version 6.8.

```bash
docker network ls
```

![Fehler externes Netzwerk](../../../assets/make-up-error.png) (6.8)

## Ports, Domains und 502/503

Bei belegtem Port einen freien `NGINX_PORT` wählen und URLs sowie `--resolve`-Argumente anpassen. Die internen Ports 9200 und 5601 sind fest. Funktioniert curl allein, die hosts-Datei des Browser-Rechners und die Proxy-Ausnahmen beider Domains prüfen. Ein unbekannter Host liefert HTTP 404. Bei 502/503 Zustand und Protokolle des jeweiligen Dienstes prüfen. Compose wartet auf eine begrenzte HTTP-Statusprüfung von Elasticsearch. Kibana ist bereit, wenn `/api/status` den Wert `status.overall.level: available` liefert. Schlägt die Elasticsearch-Prüfung fehl, zuerst dessen Protokolle untersuchen. Image-Änderungen per `make build` und Konfiguration per `make up` anwenden oder `down` und `up` mit denselben Mounts ausführen. `restart` behält die aktuelle Konfiguration.

```bash
curl --noproxy '*' --resolve elastic.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 http://elastic.local:8080/
curl --noproxy '*' --resolve elastic.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 'http://elastic.local:8080/_cluster/health?pretty'
curl --noproxy '*' --resolve elastic.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 'http://elastic.local:8080/_cat/plugins?v'
curl --noproxy '*' --resolve kibana.local:8080:127.0.0.1 --fail --silent --show-error --max-time 10 http://kibana.local:8080/api/status
```

## Build, Plugins und Ressourcen

Bei Build-Fehlern Zugriff auf offizielle Registries und Plug-in-Downloads prüfen. Elasticsearch und Kibana benötigen dieselbe Version. `_cat/plugins` sollte `analysis-icu` und `analysis-phonetic` mit dieser Version zeigen. Bei Startfehlern Speicherplatz, Docker-Arbeitsspeicher, OOM-Meldungen, `vm.max_map_count` und die [Rechte beider UID/GID-Paare](getting-started.md) an den tatsächlichen Pfaden prüfen. Bei Analysefehlern die API-Antwort und `config/analysis/synonyms.txt` ansehen. Ungültige Regeln untersuchen, bevor `lenient` das Verhalten ändert.

## Dokumentation

- [Erste Schritte](getting-started.md)
- [Übungen zu Suche und Textanalyse](search-lab.md)
- [Betrieb und Make-Befehle](operations.md)
- [Architektur und Konfiguration](../reference/configuration.md)
- [Mitwirken](../CONTRIBUTING.md)
