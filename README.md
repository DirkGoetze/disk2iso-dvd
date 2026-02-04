# disk2iso DVD Module

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/github/v/release/DirkGoetze/disk2iso-dvd)](https://github.com/DirkGoetze/disk2iso-dvd/releases)

Video-DVD Ripping Plugin für [disk2iso](https://github.com/DirkGoetze/disk2iso) - ermöglicht entschlüsseltes und verschlüsseltes Kopieren von DVD-Video Discs.

## 🚀 Features

- **Entschlüsseltes DVD-Backup** - dvdbackup mit libdvdcss2
- **Verschlüsselte ISO-Kopien** - ddrescue/dd Fallback
- **Intelligentes Fallback-System** - Automatischer Methodenwechsel bei Fehlern
- **Retry-Mechanismus** - Bis zu 3 Versuche mit verschiedenen Methoden
- **TMDB Integration** - Automatische Film-Metadaten (optional)
- **Fortschritts-Tracking** - Echtzeit-Prozentanzeige
- **Multi-Method Support** - 3 verschiedene Kopiermethoden

## 📋 Voraussetzungen

- **disk2iso** >= v1.2.0 ([Installation](https://github.com/DirkGoetze/disk2iso))
- **dvdbackup** (empfohlen, für entschlüsselte Backups)
- **libdvd-pkg** / **libdvdcss2** (für CSS-Entschlüsselung)
- **genisoimage** (für ISO-Erstellung aus entschlüsselten Backups)
- **ddrescue** (optional, für robustes Kopieren)
- **dd** (Fallback, immer verfügbar)

## 📦 Installation

### Automatisch (empfohlen)

```bash
# Download neueste Version
curl -L https://github.com/DirkGoetze/disk2iso-dvd/releases/latest/download/dvd-module.zip -o /tmp/dvd.zip

# Entpacken nach disk2iso
cd /opt/disk2iso
sudo unzip /tmp/dvd.zip

# Service neu starten
sudo systemctl restart disk2iso
```

### Manuell

1. Download [neueste Release](https://github.com/DirkGoetze/disk2iso-dvd/releases/latest)
2. Entpacke nach `/opt/disk2iso/`
3. Setze Berechtigungen: `sudo chown -R root:root /opt/disk2iso/`
4. Restart Service: `sudo systemctl restart disk2iso`

### Via Web-UI (ab v1.3.0)

1. Öffne disk2iso Web-UI
2. Gehe zu **Einstellungen → Module**
3. Klicke auf **DVD → Installieren**

## ⚙️ Konfiguration

### Manifest-Datei

Das Modul wird über `conf/libdvd.ini` konfiguriert:

```ini
[module]
name=dvd
version=1.2.0
enabled=true

[dependencies]
# Kritische externe Tools
external=

# Optionale Tools
optional=dvdbackup,genisoimage,ddrescue

[folders]
# Ausgabe-Ordner (unterhalb von OUTPUT_DIR)
output=dvd
```

### libdvdcss2 installieren (für CSS-Entschlüsselung)

```bash
# Debian/Ubuntu
sudo apt install libdvd-pkg
sudo dpkg-reconfigure libdvd-pkg

# Oder manuell
sudo apt install libdvdcss2
```

### Modul aktivieren/deaktivieren

```bash
# Deaktivieren (im Manifest)
sudo nano /opt/disk2iso/conf/libdvd.ini
# Setze: enabled=false

# Service neu starten
sudo systemctl restart disk2iso
```

## 🔧 Verwendung

### Automatisch

Lege eine Video-DVD ein - disk2iso erkennt automatisch den Typ und startet das Kopieren:

```bash
# Status prüfen
sudo systemctl status disk2iso

# Logs ansehen
sudo journalctl -u disk2iso -f
```

### Via Web-UI

1. Öffne <http://your-server:5000>
2. Lege DVD ein
3. Klicke auf **Kopieren starten**
4. Verfolge Fortschritt in Echtzeit

## 📊 Ausgabe-Struktur

### Methode 1: Entschlüsselt (dvdbackup)

```text
/media/iso/dvd/
├── Movie_Title_2024/
│   ├── VIDEO_TS/                  # Entschlüsselter DVD-Inhalt
│   │   ├── VIDEO_TS.IFO
│   │   ├── VTS_01_0.IFO
│   │   ├── VTS_01_1.VOB
│   │   └── ...
│   └── Movie_Title_2024.iso       # ISO aus VIDEO_TS erstellt
└── Movie_Title_2024.log           # Kopiervorgang-Log
```

### Methode 2/3: Verschlüsselt (ddrescue/dd)

```text
/media/iso/dvd/
├── Movie_Title_2024.iso           # ISO-Image (verschlüsselt)
└── Movie_Title_2024.iso.log       # Kopiervorgang-Log
```

## 🛠️ Kopiermethoden

### Methode 1: dvdbackup + genisoimage (empfohlen)

- **Entschlüsselt** - CSS-Schutz wird entfernt
- **Schnell** - Optimierte Lesegeschwindigkeit
- **Kompatibel** - Spielt auf allen Geräten ab
- **Ordner-Struktur** - VIDEO_TS zugänglich

```bash
# Automatisch verwendet wenn dvdbackup verfügbar
sudo apt-get install dvdbackup genisoimage libdvd-pkg
```

### Methode 2: ddrescue (Fallback bei Fehlern)

- **Robust** - Automatisches Retry bei Lesefehlern
- **Verschlüsselt** - ISO bleibt kopiergeschützt
- **Fortsetzen** - Map-Datei für Unterbrechungen

```bash
sudo apt-get install gddrescue
```

### Methode 3: dd (Letzter Fallback)

- **Einfach** - Keine Extra-Tools nötig
- **Langsam** - Keine Fehlerbehandlung
- **Verschlüsselt** - ISO bleibt kopiergeschützt

```bash
# Immer verfügbar (Teil von coreutils)
```

## 🔄 Intelligentes Fallback-System

Das Modul versucht automatisch verschiedene Methoden:

1. **Versuch 1**: dvdbackup (entschlüsselt, schnell)
2. **Versuch 2**: ddrescue (verschlüsselt, robust) - bei dvdbackup-Fehler
3. **Versuch 3**: dd (verschlüsselt, langsam) - bei ddrescue-Fehler

Fehler werden geloggt und der Benutzer wird informiert:

```text
[ERROR] dvdbackup failed (Exit: 1) - trying ddrescue...
[INFO] Switching to ddrescue method
[SUCCESS] DVD copied successfully with ddrescue
```

## 🔌 API-Endpunkte

Keine zusätzlichen API-Endpunkte - das Modul integriert sich in die Haupt-API:

```bash
# Status-Abfrage
curl http://localhost:5000/api/status

# Ausgabe bei DVD Kopiervorgang:
{
  "status": "copying",
  "disc_type": "dvd-video",
  "progress": 65,
  "method": "dvdbackup",
  "current_attempt": 1
}
```

## 🧪 Entwicklung

### Struktur

```text
disk2iso-dvd/
├── conf/
│   └── libdvd.ini              # Modul-Manifest
├── lang/
│   ├── libdvd.de               # Deutsche Übersetzung
│   ├── libdvd.en               # Englische Übersetzung
│   ├── libdvd.es               # Spanische Übersetzung
│   └── libdvd.fr               # Französische Übersetzung
└── lib/
    └── libdvd.sh               # Haupt-Bibliothek
```

### Lokale Tests

```bash
# In disk2iso-Umgebung testen
cd /opt/disk2iso
source lib/libcommon.sh
source lib/libdvd.sh

# Abhängigkeiten prüfen
dvd_check_dependencies

# Testlauf mit DVD
copy_video_dvd
```

## 📝 Changelog

Siehe [CHANGELOG.md](CHANGELOG.md) für alle Änderungen.

## 🤝 Beitragen

1. Fork das Repository
2. Erstelle einen Feature Branch (`git checkout -b feature/amazing-feature`)
3. Commit deine Änderungen (`git commit -m 'Add amazing feature'`)
4. Push zum Branch (`git push origin feature/amazing-feature`)
5. Öffne einen Pull Request

## 📜 Lizenz

MIT License - siehe [LICENSE](LICENSE) für Details.

## 🔗 Links

- [disk2iso Core](https://github.com/DirkGoetze/disk2iso)
- [Blu-ray Module](https://github.com/DirkGoetze/disk2iso-bluray) (optional)
- [TMDB Module](https://github.com/DirkGoetze/disk2iso-tmdb) (optional)
- [MQTT Module](https://github.com/DirkGoetze/disk2iso-mqtt) (optional)

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/DirkGoetze/disk2iso-dvd/issues)
- **Diskussionen**: [GitHub Discussions](https://github.com/DirkGoetze/disk2iso-dvd/discussions)
- **Core Projekt**: [disk2iso](https://github.com/DirkGoetze/disk2iso)
