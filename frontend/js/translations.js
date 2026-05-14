const translations = {
    en: {
        'Text Analysis': 'Text Analysis',
        'Enter text to analyze:': 'Enter text to analyze:',
        'Max 5000 characters': 'Max 5000 characters',
        'Analyze': 'Analyze',
        'Clear': 'Clear',
        'Analysis Results': 'Analysis Results',
        'Classification:': 'Classification:',
        'Category:': 'Category:',
        'Confidence:': 'Confidence:',
        'Severity Level:': 'Severity Level:',
        'Highlighted Analysis:': 'Highlighted Analysis:',
        'Detected Keywords:': 'Detected Keywords:',
        'Explanation:': 'Explanation:',
        'Classification Probabilities:': 'Classification Probabilities:',
        'Statistics': 'Statistics',
        'Total Analyses:': 'Total Analyses:',
        'Bullying Detected:': 'Bullying Detected:',
        'Detection Rate:': 'Detection Rate:',
        'Avg Confidence:': 'Avg Confidence:',
        'Model Information': 'Model Information',
        'Categories:': 'Categories:',
        'Not Bullying': 'Not Bullying',
        'Harassment': 'Harassment',
        'Hate Speech': 'Hate Speech',
        'Insults': 'Insults',
        'Threats': 'Threats',
        'Exclusion': 'Exclusion',
        'Severity Levels:': 'Severity Levels:',
        'Critical': 'Critical',
        'High': 'High',
        'Medium': 'Medium',
        'Low': 'Low',
        'None': 'None',
        'Diploma Project for 3 Students': 'Diploma Project for 3 Students',
        'Built with FastAPI, ML, and Modern Web Technologies': 'Built with FastAPI, ML, and Modern Web Technologies',
        'Error:': 'Error:',
        'Please enter text': 'Please enter text to analyze',
        'Text is too long': 'Text is too long (max 5000 chars)',
        'Analyzing...': 'Analyzing...',
        'Analysis failed': 'Analysis failed'
    },
    ru: {
        'Text Analysis': 'Анализ текста',
        'Enter text to analyze:': 'Введите текст для анализа:',
        'Max 5000 characters': 'Макс 5000 символов',
        'Analyze': 'Анализировать',
        'Clear': 'Очистить',
        'Analysis Results': 'Результаты анализа',
        'Classification:': 'Классификация:',
        'Category:': 'Категория:',
        'Confidence:': 'Уверенность:',
        'Severity Level:': 'Уровень серьезности:',
        'Highlighted Analysis:': 'Выделенный анализ:',
        'Detected Keywords:': 'Обнаруженные ключевые слова:',
        'Explanation:': 'Объяснение:',
        'Classification Probabilities:': 'Вероятности классификации:',
        'Statistics': 'Статистика',
        'Total Analyses:': 'Всего анализов:',
        'Bullying Detected:': 'Обнаружено буллинга:',
        'Detection Rate:': 'Процент обнаружения:',
        'Avg Confidence:': 'Средняя уверенность:',
        'Model Information': 'Информация о модели',
        'Categories:': 'Категории:',
        'Not Bullying': 'Не буллинг',
        'Harassment': 'Преследование',
        'Hate Speech': 'Речь ненависти',
        'Insults': 'Оскорбления',
        'Threats': 'Угрозы',
        'Exclusion': 'Исключение',
        'Severity Levels:': 'Уровни серьезности:',
        'Critical': 'Критический',
        'High': 'Высокий',
        'Medium': 'Средний',
        'Low': 'Низкий',
        'None': 'Нет',
        'Diploma Project for 3 Students': 'Дипломный проект для 3 студентов',
        'Built with FastAPI, ML, and Modern Web Technologies': 'Разработано с FastAPI, ML и современными веб-технологиями',
        'Error:': 'Ошибка:',
        'Please enter text': 'Пожалуйста, введите текст для анализа',
        'Text is too long': 'Текст слишком длинный (макс 5000 символов)',
        'Analyzing...': 'Анализирую...',
        'Analysis failed': 'Анализ не удался'
    }
};

function t(key) {
    const lang = localStorage.getItem('language') || 'en';
    return translations[lang][key] || key;
}

function updateAllText() {
    document.querySelectorAll('.label-text').forEach(el => {
        const text = el.textContent;
        el.textContent = t(text);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const langButtons = document.querySelectorAll('.lang-btn');
    const savedLang = localStorage.getItem('language') || 'en';
    
    langButtons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.lang === savedLang) {
            btn.classList.add('active');
        }
        
        btn.addEventListener('click', () => {
            localStorage.setItem('language', btn.dataset.lang);
            langButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            updateAllText();
        });
    });
    
    updateAllText();
});
