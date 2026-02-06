/**
 * Dependencies Widget (4x1) - DVD
 * Zeigt DVD-Video spezifische Tools (dvdbackup, ddrescue)
 * Version: 1.0.0
 */

function loadDvdDependencies() {
    fetch('/api/widgets/dvd/dependencies')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.software) {
                updateDvdDependencies(data.software);
            }
        })
        .catch(error => {
            console.error('Fehler beim Laden der DVD-Dependencies:', error);
            showDvdDependenciesError();
        });
}

function updateDvdDependencies(softwareList) {
    const tbody = document.getElementById('dvd-dependencies-tbody');
    if (!tbody) return;
    
    // DVD-spezifische Tools (aus libdvd.ini [dependencies])
    const dvdTools = [
        { name: 'dvdbackup', display_name: 'dvdbackup' },
        { name: 'genisoimage', display_name: 'genisoimage' },
        { name: 'ddrescue', display_name: 'GNU ddrescue' }
    ];
    
    let html = '';
    
    dvdTools.forEach(tool => {
        const software = softwareList.find(s => s.name === tool.name);
        if (software) {
            html += renderSoftwareRow(tool.display_name, software);
        }
    });
    
    if (html === '') {
        html = '<tr><td colspan="4" style="text-align: center; padding: 20px; color: #999;">Keine Informationen verfügbar</td></tr>';
    }
    
    tbody.innerHTML = html;
}

function showDvdDependenciesError() {
    const tbody = document.getElementById('dvd-dependencies-tbody');
    if (!tbody) return;
    
    tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; padding: 20px; color: #e53e3e;">Fehler beim Laden</td></tr>';
}

// Auto-Load
if (document.getElementById('dvd-dependencies-widget')) {
    loadDvdDependencies();
}
