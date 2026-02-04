# Changelog

Alle bedeutenden Änderungen am disk2iso DVD Modul werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

## [Unreleased]

### Geplant

- Automatische Chapter-Erkennung
- Multi-Angle Support
- Untertitel-Extraktion
- Audio-Track Auswahl

## [1.2.0] - 2026-02-04

### Added

- Initiale Abtrennung als eigenständiges Modul
- dvdbackup Unterstützung für entschlüsselte Backups
- ddrescue Fallback für robustes Kopieren
- dd Fallback-Methode
- Intelligentes 3-Stufen Fallback-System
- Manifest-Datei (libdvd.ini)
- Mehrsprachige Unterstützung (DE, EN, ES, FR)
- Fortschritts-Tracking mit Prozentanzeige
- Ausgabe-Ordner Konfiguration
- Retry-Mechanismus bei Fehlern

### Changed

- Unabhängiges Repository von disk2iso Core
- Modulare INI-basierte Konfiguration
- Optionale Integration (nicht mehr im Core)

### Fixed

- Keine bekannten Fehler

## [1.0.0] - 2025-XX-XX

### Features

- Erste Version als Teil von disk2iso Core
- Basis-Funktionalität für DVD-Video Kopieren

---

[Unreleased]: https://github.com/DirkGoetze/disk2iso-dvd/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/DirkGoetze/disk2iso-dvd/releases/tag/v1.2.0
[1.0.0]: https://github.com/DirkGoetze/disk2iso-dvd/releases/tag/v1.0.0
