# Mitwirken

## Sprache wählen

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| [Русский](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/.github/CONTRIBUTING.md) | [English](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/en/CONTRIBUTING.md) | [Español](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/es/CONTRIBUTING.md) | [中文](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/zh/CONTRIBUTING.md) | [Français](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/fr/CONTRIBUTING.md) | **Ausgewählt** |

Reproduzierbare Fehler über Issues, Fragen und Ideen über Discussions melden. Keine echten Daten, lokale Konfigurationen, Passwörter oder Schwachstellendetails veröffentlichen. Größere Änderungen vorher mit dem Eigentümer abstimmen.

- Reproduzierbare Fehler: [GitHub Issues](https://github.com/yaleksandr89/docker-elasticsearch/issues).
- Fragen und Ideen: [GitHub Discussions](https://github.com/yaleksandr89/docker-elasticsearch/discussions).

Make-Befehle, Konfigurationsnamen, Datenkompatibilität und Laborzweck erhalten. Änderungen an Images, Netzwerk, Portfreigabe, Auth/TLS und Speicher benötigen separate Entscheidung. In frischer Kopie mit synthetischen Daten, eindeutigen Containern, Port und Projekt testen; Arbeitslabor nicht anfassen.

## Prüfungen

CI läuft bei Push und Pull Request auf `master` sowie manuell über Actions. `quality` prüft Startup-Skriptsyntax, Übungs-Fixtures und aufgelöstes Compose; `docker-smoke` baut isoliert mit festen Versionen und prüft HTTP über beide virtuellen Hosts, Plugins und Suche. Nur CI-Ergebnisse belegen Erfolg, nicht das Vorhandensein des Workflows.

```bash
bash -n docker-configs/nginx/start-nginx.sh
python3 tests/check-fixtures.py
python3 tests/test-runtime-contract.py
```

Standard ist `WITH_EXTERNAL_NETWORK=0`. Zur Integration ein bestehendes vertrauenswürdiges Netz in `EXTERNAL_NETWORK` angeben und bei jedem Make-Aufruf `WITH_EXTERNAL_NETWORK=1` setzen. Nur Elasticsearch tritt bei. Netzmitglieder erhalten ohne Anmeldung Zugriff über den Containernamen auf Port 9200. Compose erhält das externe Netz beim Herunterfahren.

## Pull Request

Themenbranch von `master` erstellen, signierte Conventional Commits mit russischer Beschreibung. Im PR Grund, Änderung, Daten-/Sicherheitswirkung und tatsächliche Checks nennen. Sechs Lokalisierungen synchron halten; keine Checks für grünes CI abschwächen.

## Dokumentation

- [Erste Schritte](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/de/guides/getting-started.md)
- [Übungen zu Suche und Textanalyse](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/de/guides/search-lab.md)
- [Betrieb und Make-Befehle](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/de/guides/operations.md)
- [Fehlerbehebung](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/de/guides/troubleshooting.md)
- [Architektur und Konfiguration](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/de/reference/configuration.md)
