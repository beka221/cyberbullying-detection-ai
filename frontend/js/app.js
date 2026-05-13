/**
 * Cyberbullying Detection AI - Frontend Application
 * Система обнаружения кибербуллинга - фронтенд приложение
 */

const API_BASE_URL = '/api';
const UI = {
    textInput: document.getElementById('textInput'),
    analyzeBtn: document.getElementById('analyzeBtn'),
    clearBtn: document.getElementById('clearBtn'),
    resultsSection: document.getElementById('resultsSection'),
    resultContent: document.getElementById('resultContent'),
    errorSection: document.getElementById('errorSection'),
    errorMessage: document.getElementById('errorMessage'),
    statsContent: document.getElementById('statsContent')
};

// Event Listeners
UI.analyzeBtn.addEventListener('click', analyzeText);
UI.clearBtn.addEventListener('click', clearForm);

// Load statistics on page load
document.addEventListener('DOMContentLoaded', () => {
    loadStatistics();
    setInterval(loadStatistics, 10000); // Update every 10 seconds
});

/**
 * Analyze text for cyberbullying
 * Анализировать текст на кибербуллинг
 */
async function analyzeText() {
    const text = UI.textInput.value.trim();

    // Validation
    if (!text) {
        showError('Please enter text to analyze / Пожалуйста введите текст для анализа');
        return;
    }

    if (text.length > 5000) {
        showError('Text is too long (max 5000 chars) / Текст слишком длинный (макс 5000 символов)');
        return;
    }

    // Show loading state
    UI.analyzeBtn.disabled = true;
    UI.analyzeBtn.innerHTML = '<span class="spinner"></span> Analyzing... / Анализирую...';
    UI.errorSection.style.display = 'none';

    try {
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                language: 'en'
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Analysis failed');
        }

        const result = await response.json();
        displayResults(result);

    } catch (error) {
        console.error('Error:', error);
        showError(`Error: ${error.message}`);
    } finally {
        UI.analyzeBtn.disabled = false;
        UI.analyzeBtn.innerHTML = '<i class="fas fa-play"></i> Analyze / Анализировать';
    }
}

/**
 * Display analysis results
 * Отобразить результаты анализа
 */
function displayResults(result) {
    const isBullying = result.is_cyberbullying;
    const classification = result.classification;
    const severity = result.severity || 'unknown';

    const severityColor = {
        'high': 'danger',
        'medium': 'warning',
        'low': 'info'
    }[severity] || 'secondary';

    const severityLabel = {
        'high': '🔴 High / Высокий',
        'medium': '🟡 Medium / Средний',
        'low': '🟢 Low / Низкий'
    }[severity] || 'Unknown';

    const html = `
        <div class="row">
            <div class="col-md-12 mb-3">
                <h6>Classification Result / Результат классификации:</h6>
                <div>
                    ${isBullying 
                        ? '<span class="result-badge bullying">⚠️ CYBERBULLYING DETECTED / ОБНАРУЖЕН КИБЕРБУЛЛИНГ</span>' 
                        : '<span class="result-badge safe">✓ SAFE / БЕЗОПАСНО</span>'
                    }
                </div>
            </div>

            <div class="col-md-12 mb-3">
                <h6>Category / Категория:</h6>
                <p class="fw-bold text-primary">${classification.label}</p>
            </div>

            <div class="col-md-12 mb-3">
                <h6>Confidence / Уверенность:</h6>
                <p class="fw-bold">${(classification.confidence * 100).toFixed(2)}%</p>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: ${classification.confidence * 100}%; 
                        background-color: ${getConfidenceColor(classification.confidence)};"></div>
                </div>
            </div>

            <div class="col-md-12 mb-3">
                <h6>Severity / Серьезность:</h6>
                <span class="badge bg-${severityColor}">${severityLabel}</span>
            </div>

            <div class="col-md-12">
                <h6>Probabilities / Вероятности:</h6>
                <div class="table-responsive">
                    <table class="table table-sm">
                        <tbody>
                            ${Object.entries(classification.probability)
                                .map(([label, prob]) => `
                                    <tr>
                                        <td>${label}</td>
                                        <td>
                                            <div class="progress">
                                                <div class="progress-bar" style="width: ${prob * 100}%">
                                                    ${(prob * 100).toFixed(1)}%
                                                </div>
                                            </div>
                                        </td>
                                    </tr>
                                `)
                                .join('')
                            }
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    `;

    UI.resultContent.innerHTML = html;
    UI.resultsSection.style.display = 'block';
    UI.errorSection.style.display = 'none';

    // Scroll to results
    UI.resultsSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Get confidence color
 * Получить цвет уверенности
 */
function getConfidenceColor(confidence) {
    if (confidence >= 0.8) return '#dc3545'; // High - Red
    if (confidence >= 0.6) return '#fd7e14'; // Medium - Orange
    return '#ffc107'; // Low - Yellow
}

/**
 * Load statistics
 * Загрузить статистику
 */
async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats?days=7`);

        if (!response.ok) {
            throw new Error('Failed to load statistics');
        }

        const stats = await response.json();
        displayStatistics(stats);

    } catch (error) {
        console.error('Statistics error:', error);
        UI.statsContent.innerHTML = '<p class="text-danger">Failed to load statistics</p>';
    }
}

/**
 * Display statistics
 * Отобразить статистику
 */
function displayStatistics(stats) {
    const html = `
        <div class="stats-container">
            <div class="stat-item mb-3">
                <small class="text-muted">Total Analyses / Всего анализов:</small>
                <h5 class="text-primary fw-bold">${stats.total_analyses}</h5>
            </div>

            <div class="stat-item mb-3">
                <small class="text-muted">Bullying Detected / Обнаружено буллинга:</small>
                <h5 class="text-danger fw-bold">${stats.bullying_detected}</h5>
            </div>

            <div class="stat-item mb-3">
                <small class="text-muted">Detection Rate / Процент обнаружения:</small>
                <h5 class="text-warning fw-bold">${(stats.detection_rate * 100).toFixed(1)}%</h5>
            </div>

            <div class="stat-item mb-3">
                <small class="text-muted">Avg Confidence / Средняя уверенность:</small>
                <h5 class="text-success fw-bold">${(stats.average_confidence * 100).toFixed(1)}%</h5>
            </div>

            <hr>

            <small class="text-muted">Last 7 days / За последние 7 дней</small>
        </div>
    `;

    UI.statsContent.innerHTML = html;
}

/**
 * Clear form
 * Очистить форму
 */
function clearForm() {
    UI.textInput.value = '';
    UI.resultsSection.style.display = 'none';
    UI.errorSection.style.display = 'none';
    UI.textInput.focus();
}

/**
 * Show error
 * Показать ошибку
 */
function showError(message) {
    UI.errorMessage.textContent = message;
    UI.errorSection.style.display = 'block';
    UI.resultsSection.style.display = 'none';
}
