/**
 * disk2iso - Settings Widget (4x1) - DVD
 * Lädt DVD Einstellungen dynamisch
 */

let dvdSaveTimeout = null;

document.addEventListener('DOMContentLoaded', function() {
    // Lade Widget-Content via AJAX
    fetch('/api/widgets/dvd/settings')
        .then(response => response.text())
        .then(html => {
            const container = document.getElementById('dvd-settings-container');
            if (container) {
                container.innerHTML = html;
                initDvdSettingsWidget();
            }
        })
        .catch(error => console.error('Fehler beim Laden der DVD Settings:', error));
});

function initDvdSettingsWidget() {
    const activeCheckbox = document.getElementById('dvd_active');
    
    if (activeCheckbox) {
        activeCheckbox.addEventListener('change', function() {
            // Speichere Änderungen automatisch
            saveDvdSettings();
        });
    }
}

function saveDvdSettings() {
    // Debounce: Warte 300ms nach letzter Änderung
    if (dvdSaveTimeout) {
        clearTimeout(dvdSaveTimeout);
    }
    
    dvdSaveTimeout = setTimeout(() => {
        saveDvdSettingsNow();
    }, 300);
}

function saveDvdSettingsNow() {
    const active = document.getElementById('dvd_active')?.checked || false;
    
    const data = {
        active: active
    };
    
    fetch('/api/widgets/dvd/settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            showNotification('DVD Einstellungen gespeichert', 'success');
        } else {
            showNotification('Fehler beim Speichern: ' + result.error, 'error');
        }
    })
    .catch(error => {
        console.error('Fehler:', error);
        showNotification('Fehler beim Speichern der Einstellungen', 'error');
    });
}
