# Betrieb und Make-Befehle

## Sprache wählen

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| [Русский](../../ru/guides/operations.md) | [English](../../en/guides/operations.md) | [Español](../../es/guides/operations.md) | [中文](../../zh/guides/operations.md) | [Français](../../fr/guides/operations.md) | **Ausgewählt** |

Standardmäßig läuft das Labor lokal. Vor dem Start die Datenverzeichnisse nach der Anleitung vorbereiten.

[Erste Schritte](getting-started.md)

## Schnellstart

```bash
make help
make init
make config
```

`COMPOSE_COMMAND` = `docker compose`.

```bash
make COMPOSE_COMMAND='docker compose' config
```

| Befehl | Wirkung |
|---|---|
| `make help` | Zeigt die zweisprachige Hilfe. |
| `make init` | Erstellt fehlende `.docker.env` und beide `*_DATA_DIR`-Verzeichnisse; erhält bestehende Konfiguration. |
| `make pull` | Lädt offizielle Basis-Images gemäß Make-Konfiguration; baut lokale Images nicht neu. |
| `make build` | Baut Images ohne Cache. |
| `make config` | Zeigt aufgelöste Compose-Konfiguration ohne Start. |
| `make up` | Nach erfolgreicher HTTP-Prüfung von Elasticsearch startet Compose Kibana im Hintergrund. Die Bereitschaft von Kibana über /api/status prüfen. Bei eigenen Domains oder Ports die Beispiel-URLs anpassen. |
| `make down` | Stoppt und entfernt Container und verwaltetes Netzwerk, nicht das Host-Datenverzeichnis. |
| `make reset` | Führt nacheinander `down` und `up -d` aus, erstellt die Container neu und erhält Daten und Indizes. |
| `make restart` | Startet vorhandene Container neu; übernimmt keine Image-, Compose- oder Umgebungsänderungen. |
| `make in elasticsearch` | Startet Bash im gewählten Dienst: `elasticsearch`, `kibana`, `nginx`. |
| `make log kibana` | Zeigt Logs des gewählten Dienstes, ohne automatisch zu folgen. |

```bash
docker compose --env-file .docker.env -f docker-compose.yml ps
make log elasticsearch
make restart
make down
```

## Ein anderes Projekt verbinden

Das bestehende vertrauenswürdige Anwendungsnetz mit `docker network ls` ermitteln und seine Mitglieder mit `docker network inspect` prüfen. Den tatsächlichen Namen als `EXTERNAL_NETWORK` in `.docker.env` eintragen. Compose führt beide Dateien zusammen, behält `backend` bei und verbindet nur Elasticsearch mit dem Zusatznetz. Im Anwendungscontainer `http://docker-elasticsearch-es:9200` oder den tatsächlichen Namen aus `ELASTIC_CONTAINER` verwenden. Alle Netzmitglieder erhalten Zugriff ohne Anmeldung. Die Option auch bei späteren Befehlen bis zum Herunterfahren setzen.

```bash
docker network ls
make config WITH_EXTERNAL_NETWORK=1
make up WITH_EXTERNAL_NETWORK=1
```

```bash
make down WITH_EXTERNAL_NETWORK=1
```

Zum Moduswechsel zuerst `down` mit den bisherigen Dateien oder der bisherigen Option ausführen, beide Datenpfade behalten und dann `up` mit der neuen Einstellung aufrufen. Das externe Netz bleibt bei seinem Eigentümer. Nur vereinbarte Netze und Datenpfade verwenden. `restart` behält die Netzkonfiguration der vorhandenen Container bei.

```bash
docker compose --env-file .docker.env -f docker-compose.yml -f docker-compose.external.yml config
docker compose --env-file .docker.env -f docker-compose.yml -f docker-compose.external.yml up -d
docker compose --env-file .docker.env -f docker-compose.yml -f docker-compose.external.yml down
```

## Persistenz und Updates

Beide Bind-Mounts bleiben beim Neuerstellen erhalten. Kibana speichert die meisten gespeicherten Objekte in Elasticsearch-Systemindizes. Vor dem Stoppen des alten Labors im Container `/usr/share/kibana/data` prüfen und benötigte lokale Dateien getrennt sichern.

Make hat keine Ziele für automatische Bereinigung, Snapshots oder Wiederherstellung. Das Kopieren eines laufenden Elasticsearch-Datenverzeichnisses ist als Sicherung unzuverlässig. Vor dem Stoppen laufende Versionen, Containernamen, Port und beide Mount-Pfade erfassen. Bei Bedarf einen offiziellen [Snapshot](https://www.elastic.co/docs/deploy-manage/tools/snapshot-and-restore) erstellen, die Wiederherstellung separat testen und die Plug-in-Kompatibilität für jeden Schritt des [unterstützten Upgrade-Pfads](https://www.elastic.co/docs/deploy-manage/upgrade) prüfen. Für bestehende Clients den eingestellten `ELASTIC_CONTAINER`-Namen wie `global-elasticsearch` behalten. Port 80 nur bewusst auf 8080 ändern. Der Eigentümer entscheidet separat über ein Upgrade.

Das alte Labor mit seiner ursprünglichen Konfiguration stoppen. Bei unbekannter Ausgangsversion zuerst die Kompatibilität prüfen. Ein Downgrade auf aktualisierten Daten ist unsicher.

## Prüfungen

CI läuft bei Push und Pull Request auf `master` sowie manuell über Actions. `quality` prüft Startup-Skriptsyntax, Übungs-Fixtures und aufgelöstes Compose; `docker-smoke` baut isoliert mit festen Versionen und prüft HTTP über beide virtuellen Hosts, Plugins und Suche. Nur CI-Ergebnisse belegen Erfolg, nicht das Vorhandensein des Workflows.

Python 3 ist nur für Fixture- und CI-Prüfungen erforderlich.

```bash
bash -n docker-configs/nginx/start-nginx.sh
python3 tests/check-fixtures.py
python3 tests/test-runtime-contract.py
```

`tests/smoke.py` nur in einer Wegwerfkopie ausführen. Lokal werden `/tmp/docker-elasticsearch-review.XXXXXXXX/candidate` und der Projektname `elastic-learning-test-xxxxxxxx` mit denselben acht alphanumerischen Zeichen in Kleinschreibung erwartet. Vor dem Anlegen des Index prüft das Skript Labels, Images, Netz, Port und beide Mounts. `--persisted` prüft die zuvor erstellten Dokumente.

## Dokumentation

- [Erste Schritte](getting-started.md)
- [Übungen zu Suche und Textanalyse](search-lab.md)
- [Fehlerbehebung](troubleshooting.md)
- [Architektur und Konfiguration](../reference/configuration.md)
- [Mitwirken](../CONTRIBUTING.md)
