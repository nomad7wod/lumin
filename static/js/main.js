// File upload handling
document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('pdfFile');
    const resultsDiv = document.getElementById('results');
    const loadingDiv = document.getElementById('loading');
    
    if (uploadForm) {
        uploadForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const file = fileInput.files[0];
            if (!file) {
                alert('Por favor selecciona un archivo PDF');
                return;
            }
            
            const formData = new FormData();
            formData.append('file', file);
            
            // Show loading
            loadingDiv.style.display = 'block';
            resultsDiv.style.display = 'none';
            
            try {
                const response = await fetch('http://localhost:5001/api/upload', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    displayResults(data.results);
                } else {
                    alert('Error: ' + (data.error || 'Error procesando el archivo'));
                }
            } catch (error) {
                alert('Error al procesar el archivo: ' + error.message);
            } finally {
                loadingDiv.style.display = 'none';
            }
        });
    }
});

function displayResults(results) {
    const resultsDiv = document.getElementById('results');
    const resultsContent = document.getElementById('resultsContent');
    
    resultsContent.innerHTML = `
        <div class="result-item">
            <strong>Número de Guía:</strong> ${results.nro_guia}
        </div>
        <div class="result-item">
            <strong>Punto de Partida:</strong> ${results.punto_partida}
        </div>
        <div class="result-item">
            <strong>Observaciones:</strong> ${results.observaciones}
        </div>
        <div class="result-item">
            <strong>Conductor:</strong> ${results.conductor}
        </div>
    `;
    
    resultsDiv.style.display = 'block';
}

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
