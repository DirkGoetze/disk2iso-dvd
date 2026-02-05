"""
disk2iso - DVD Widget Settings Routes
Stellt die DVD-Einstellungen bereit (Settings Widget)
"""

import os
import sys
import configparser
from flask import Blueprint, render_template, jsonify, request
from i18n import t

# Blueprint für DVD Settings Widget
dvd_settings_bp = Blueprint('dvd_settings', __name__)

def get_dvd_ini_path():
    """Ermittelt den Pfad zur libdvd.ini"""
    return '/opt/disk2iso-dvd/conf/libdvd.ini'

def get_dvd_settings():
    """
    Liest die DVD-Einstellungen aus libdvd.ini [settings]
    """
    try:
        ini_path = get_dvd_ini_path()
        
        settings = {
            "enabled": True,
            "active": True
        }
        
        if os.path.exists(ini_path):
            parser = configparser.ConfigParser()
            parser.read(ini_path)
            
            if parser.has_section('settings'):
                settings['enabled'] = parser.getboolean('settings', 'enabled', fallback=True)
                settings['active'] = parser.getboolean('settings', 'active', fallback=True)
        
        return settings
        
    except Exception as e:
        print(f"Fehler beim Lesen der DVD-Einstellungen: {e}", file=sys.stderr)
        return {
            "enabled": True,
            "active": True
        }

def save_dvd_settings(data):
    """
    Speichert DVD-Einstellungen in libdvd.ini [settings]
    """
    try:
        ini_path = get_dvd_ini_path()
        
        if not os.path.exists(ini_path):
            return False, "INI-Datei nicht gefunden"
        
        parser = configparser.ConfigParser()
        parser.read(ini_path)
        
        if not parser.has_section('settings'):
            parser.add_section('settings')
        
        # Aktualisiere Werte
        if 'active' in data:
            parser.set('settings', 'active', 'true' if data['active'] else 'false')
        
        # Schreibe zurück
        with open(ini_path, 'w') as f:
            parser.write(f)
        
        return True, "Einstellungen gespeichert"
        
    except Exception as e:
        return False, str(e)

@dvd_settings_bp.route('/api/widgets/dvd/settings', methods=['GET'])
def api_dvd_settings_widget():
    """
    Rendert das DVD Settings Widget
    """
    config = get_dvd_settings()
    
    return render_template('widgets/dvd_widget_settings.html',
                         settings=settings,
                         t=t)

@dvd_settings_bp.route('/api/widgets/dvd/settings', methods=['POST'])
def api_save_dvd_settings():
    """
    Speichert DVD-Einstellungen
    """
    try:
        data = request.get_json()
        success, message = save_dvd_settings(data)
        
        if success:
            return jsonify({"success": True, "message": message})
        else:
            return jsonify({"success": False, "error": message}), 400
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

