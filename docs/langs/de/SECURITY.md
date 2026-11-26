# Sicherheitsrichtlinie

## Sprache wählen

| Русский | English | Español | 中文 | Français | Deutsch |
|---|---|---|---|---|---|
| [Русский](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/.github/SECURITY.md) | [English](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/en/SECURITY.md) | [Español](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/es/SECURITY.md) | [中文](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/zh/SECURITY.md) | [Français](https://github.com/yaleksandr89/docker-elasticsearch/blob/master/docs/langs/fr/SECURITY.md) | **Deutsch** |

## Unterstützte Versionen

Sicherheitskorrekturen werden für den aktuellen Stand von `master` und die zuletzt veröffentlichte Version geprüft. Ältere Versionen können andere Netzwerkeinstellungen haben; vor einem Upgrade die Datenkompatibilität prüfen.

| Version | Unterstützt |
|---|---|
| `master` | Ja |
| Zuletzt veröffentlichte Version | Ja |

## Sicherheitsgrenzen des Labors

Dies ist ein lokales Lernlabor für synthetische Daten, kein Produktionsbetrieb. In der aktuellen Konfiguration läuft Elasticsearch ohne Authentifizierung und TLS; standardmäßig wird nur Nginx auf `127.0.0.1` veröffentlicht, und die internen Ports von Elasticsearch und Kibana werden nicht auf dem Host veröffentlicht. Mit `WITH_EXTERNAL_NETWORK=1` erhalten Mitglieder des ausgewählten vertrauenswürdigen Docker-Netzes Zugriff auf Elasticsearch ohne Authentifizierung. Dieses Verhalten ist beabsichtigt und für sich genommen keine Schwachstelle. Keine nicht vertrauenswürdigen Netze verbinden und keine echten Daten verwenden.

Zu Sicherheitsproblemen zählen insbesondere:

- unbeabsichtigte Veröffentlichung von Diensten außerhalb von Loopback oder Verbindung mit einem externen Netz ohne ausdrückliche Aktivierung;
- Umgehung erwarteter Nginx-Routing-Beschränkungen oder Offenlegung interner Dateien oder Konfiguration;
- unsichere Verarbeitung von Parametern oder Pfaden, die zur Befehlsausführung oder Änderung fremder Daten führt;
- unbeabsichtigtes Löschen, Überschreiben oder Offenlegen von Daten bei Laboroperationen;
- Probleme mit Images, Plugins oder CI, die die Sicherheit dieses Projekts beeinträchtigen.

Gewöhnliche Fehler über [GitHub Issues](https://github.com/yaleksandr89/docker-elasticsearch/issues), Fragen und Ideen über [GitHub Discussions](https://github.com/yaleksandr89/docker-elasticsearch/discussions) melden. Liegt das Problem in einer Upstream-Komponente, deren genaue Version und Auswirkung auf das Labor angeben; Fehler der Komponente selbst auch nach den Regeln ihrer Maintainer melden.

## Eine Schwachstelle melden

Bevorzugt GitHub Private Vulnerability Reporting nutzen: **Security and quality → Report a vulnerability** öffnen. Ist dies nicht verfügbar, in GitHub Discussions um einen privaten Kommunikationskanal bitten, ohne technische Schwachstellendetails zu veröffentlichen.

Vor koordinierter Offenlegung keine Passwörter, Tokens, lokalen oder Produktionskonfigurationen, echten Daten, vollständigen Logs, funktionsfähigen Exploits oder sensiblen Details veröffentlichen. Nur synthetische Daten oder bereinigte Ausschnitte verwenden.

## Inhalt des Berichts

- Betroffener Release, Branch oder Commit sowie relevante Versionen von Elasticsearch, Kibana, Nginx, Docker und Compose.
- Startmodus (lokal oder Integration), erwartete Zugriffsgrenze und mögliche Auswirkungen.
- Minimale Reproduktionsschritte, erwartetes und tatsächliches Verhalten.
- Bereinigte Anfrage-, Antwort- oder Log-Ausschnitte und eine mögliche Korrektur, falls bekannt.

## Bearbeitung des Berichts

Berichte werden nach Verfügbarkeit geprüft; kein festes SLA wird versprochen. Die Offenlegung mit dem Maintainer abstimmen. Nach Bestätigung werden Korrekturen und Informationen zu betroffenen Versionen im Rahmen koordinierter Offenlegung veröffentlicht. Es wird kein Prämienprogramm für Schwachstellen angegeben.
