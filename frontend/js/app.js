const API_BASE_URL = '/api';
let probChart = null;

const UI = {
    textInput: document.getElementById('textInput'),
    analyzeBtn: document.getElementById('analyzeBtn'),
    clearBtn: document.getElementById('clearBtn'),
    resultsSection: document.getElementById('resultsSection'),
    errorSection: document.getElementById('errorSection'),
    errorMessage: document.getElementById('errorMessage'),
    statsContent: document.getElementById('statsContent')
};

UI.analyzeBtn.addEventListener('click', analyzeText);
UI.clearBtn.addEventListener('click', clearForm);

document.addEventListener('DOMContentLoaded', () => {
    loadStatistics();
    setInterval(loadStatistics, 15000);
});

async function analyzeText() {
    const text = UI.textInput.value.trim();
    const language = localStorage.getItem('language') || 'en';
    
    if (!text) {
        showError(t('Please enter text'));
        return;
    }
    
    if (text.length > 5000) {
        showError(t('Text is too long'));
        return;
    }
    
    UI.analyzeBtn.disabled = true;
    UI.analyzeBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>' + t('Analyzing...');
    UI.errorSection.style.display = 'none';
    
    try {
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text, language: language })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || t('Analysis failed'));
        }
        
        const result = await response.json();
        displayResults(result);
        
    } catch (error) {
        console.error('Error:', error);
        showError(`Error: ${error.message}`);
    } finally {
        UI.analyzeBtn.disabled = false;
        UI.analyzeBtn.innerHTML = '<i class="fas fa-play"></i> ' + t('Analyze');
    }
}

function displayResults(result) {
    const isBullying = result.is_cyberbullying;
    const classification = result.classification;
    const severity = result.severity;
    
    // Badge
    const badgeClass = isBullying ? 'danger' : 'success';
    const badgeText = isBullying ? '⚠️ CYBERBULLYING' : '✓ SAFE';
    document.getElementById('resultBadge').innerHTML = 
        `<span class="badge bg-${badgeClass} p-3 fs-6">${badgeText}</span>`;
    
    // Label
    document.getElementById('resultLabel').textContent = classification.label;
    
    // Confidence
    const confPercent = (classification.confidence * 100).toFixed(2);
    document.getElementById('resultConfidence').innerHTML = 
        `<div>${confPercent}%</div>
         <div class="progress mt-2" style="height: 8px;">
             <div class="progress-bar" style="width: ${classification.confidence * 100}%;"></div>
         </div>`;
    
    // Severity
    const severityColors = {
        'critical': 'danger',
        'high': 'warning',
        'medium': 'info',
        'low': 'secondary',
        'none': 'success'
    };
    const severityEmoji = {
        'critical': '🔴',
        'high': '🟠',
        'medium': '🟡',
        'low': '🔵',
        'none': '🟢'
    };
    
    document.getElementById('severityBadge').innerHTML = 
        `<span class="badge bg-${severityColors[severity] || 'secondary'} p-3">
            ${severityEmoji[severity]} ${severity.toUpperCase()}
        </span>`;
    
    // Highlighted text
    const highlightedHTML = result.highlighted_text.map(seg => {
        if (seg.highlight) {
            const categoryColor = {
                'harassment': '#ffc107',
                'hate_speech': '#dc3545',
                'threats': '#dc3545',
                'insults': '#fd7e14',
                'exclusion': '#0dcaf0'
            };
            return `<mark style="background-color: ${categoryColor[seg.category] || '#ffff00'}; padding: 2px 4px; border-radius: 3px;">${seg.text}</mark>`;
        }
        return seg.text;
    }).join('');
    
    document.getElementById('highlightedText').innerHTML = 
        `<div class="p-3 bg-light rounded">${highlightedHTML}</div>`;
    
    // Bullying words
    if (result.bullying_words && result.bullying_words.length > 0) {
        document.getElementById('bullyingWordsSection').style.display = 'block';
        const wordsHTML = result.bullying_words.map(w => 
            `<div class="col-md-6">
                <span class="badge bg-danger p-2">${w.word} (${w.category})</span>
            </div>`
        ).join('');
        document.getElementById('bullyingWordsList').innerHTML = wordsHTML;
    } else {
        document.getElementById('bullyingWordsSection').style.display = 'none';
    }
    
    // Explanation
    document.getElementById('explanation').textContent = result.explanation;
    
    // Probability chart
    const ctx = document.getElementById('probChart').getContext('2d');
    
    if (probChart) {
        probChart.destroy();
    }
    
    probChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(classification.probability),
            datasets: [{
                label: 'Probability',
                data: Object.values(classification.probability),
                backgroundColor: [
                    '#198754',
                    '#ffc107',
                    '#dc3545',
                    '#fd7e14',
                    '#dc3545',
                    '#0dcaf0'
                ],
                borderRadius: 5
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 1
                }
            }
        }
    });
    
    UI.resultsSection.style.display = 'block';
    UI.errorSection.style.display = 'none';
    UI.resultsSection.scrollIntoView({ behavior: 'smooth' });
}

async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats?days=7`);
        
        if (!response.ok) throw new Error('Failed to load stats');
        
        const stats = await response.json();
        
        UI.statsContent.innerHTML = `
            <div class="stat-item mb-3">
                <small class="text-muted">Total Analyses:</small>
                <h4 class="text-primary fw-bold">${stats.total_analyses}</h4>
            </div>
            <div class="stat-item mb-3">
                <small class="text-muted">Bullying Detected:</small>
                <h4 class="text-danger fw-bold">${stats.bullying_detected}</h4>
            </div>
            <div class="stat-item mb-3">
                <small class="text-muted">Detection Rate:</small>
                <h4 class="text-warning fw-bold">${(stats.detection_rate * 100).toFixed(1)}%</h4>
            </div>
            <div class="stat-item">
                <small class="text-muted">Avg Confidence:</small>
                <h4 class="text-success fw-bold">${(stats.average_confidence * 100).toFixed(1)}%</h4>
            </div>
            <hr>
            <p class="text-muted"><small>Last 7 days</small></p>
        `;
    } catch (error) {
        console.error('Stats error:', error);
    }
}

function clearForm() {
    UI.textInput.value = '';
    UI.resultsSection.style.display = 'none';
    UI.errorSection.style.display = 'none';
    UI.textInput.focus();
}

function showError(message) {
    UI.errorMessage.textContent = message;
    UI.errorSection.style.display = 'block';
    UI.resultsSection.style.display = 'none';
}
