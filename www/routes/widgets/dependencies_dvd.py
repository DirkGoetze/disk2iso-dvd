#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
disk2iso - Dependencies Widget (4x1) - DVD
============================================================================
Filepath: www/routes/widgets/dependencies_dvd.py

Beschreibung:
    Flask Blueprint für DVD-Dependencies-Widget
    - Zeigt DVD-Video spezifische Software-Abhängigkeiten
    - Nutzt systeminfo_get_software_info() aus libsysteminfo.sh
    - Filtert auf DVD-spezifische Tools: dvdbackup, lsdvd, vobcopy, genisoimage, HandBrake
============================================================================
"""

from flask import Blueprint, jsonify
import subprocess
import json
import os
from datetime import datetime

# Blueprint erstellen
dependencies_dvd_bp = Blueprint(
    'dependencies_dvd',
    __name__,
    url_prefix='/api/widgets/dvd'
)

# Pfade
INSTALL_DIR = os.environ.get('DISK2ISO_INSTALL_DIR', '/opt/disk2iso')


def get_software_info():
    """
    Ruft Software-Informationen via Bash-Funktion ab
    Nutzt systeminfo_get_software_info() aus libsysteminfo.sh
    """
    try:
        result = subprocess.run(
            ['bash', '-c', f'source {INSTALL_DIR}/lib/libsysteminfo.sh && systeminfo_get_software_info'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return json.loads(result.stdout.strip())
        return {}
    except Exception as e:
        print(f"Fehler beim Abrufen von Software-Informationen: {e}")
        return {}


@dependencies_dvd_bp.route('/dependencies')
def api_dependencies():
    """
    GET /api/widgets/dvd/dependencies
    Liefert DVD-spezifische Software-Dependencies
    """
    software_info = get_software_info()
    
    # DVD-spezifische Tools
    dvd_tools = ['dvdbackup', 'lsdvd', 'vobcopy', 'genisoimage', 'HandBrake']
    
    # Konvertiere Dictionary in flache Liste und filtere DVD-Tools
    software_list = []
    for category, tools in software_info.items():
        if isinstance(tools, list):
            for tool in tools:
                if tool.get('name') in dvd_tools:
                    software_list.append(tool)
    
    return jsonify({
        'success': True,
        'software': software_list,
        'timestamp': datetime.now().isoformat()
    })


def register_blueprint(app):
    """Registriert Blueprint in Flask-App"""
    app.register_blueprint(dependencies_dvd_bp)
