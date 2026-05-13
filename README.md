# Cyberbullying Detection and Classification System

## 🎯 Overview

An AI-powered system for **early detection and classification of cyberbullying** in text content using machine learning and natural language processing techniques.

**Built for:** 3-person diploma project  
**Technologies:** Python, FastAPI, React, scikit-learn, NLTK  
**Status:** Production-ready 🚀

---

## 📊 Features

✅ **Real-time Text Analysis** - Detect cyberbullying in seconds  
✅ **Multi-category Classification** - Identify type of bullying  
✅ **REST API** - Easy integration with any platform  
✅ **Web Dashboard** - User-friendly interface for analysis  
✅ **Database Storage** - Track all analyzed texts  
✅ **Performance Metrics** - Detailed statistics  

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip or conda
- VS Code (recommended)

### Installation

1. **Clone the project**
```bash
git clone https://github.com/beka221/cyberbullying-detection-ai.git
cd cyberbullying-detection-ai
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download NLTK data**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

5. **Create required directories**
```bash
mkdir -p data/models logs
```

6. **Start the backend server**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

7. **Open in browser**
```
http://localhost:8000
```

---

## 📚 Usage

### Via Web Interface
1. Go to `http://localhost:8000`
2. Paste text to analyze
3. Click "Analyze"
4. View results with classification and confidence

### Via API
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here"}'
```

---

## 👥 Team Roles (3-person team)

| Role | Responsibilities |
|------|------------------|
| **Person 1: ML Engineer** | Data prep, model training, API backend |
| **Person 2: Frontend Dev** | Web UI, dashboard, visualizations |
| **Person 3: QA/Integration** | Testing, documentation, deployment |

---

## 📈 Model Performance

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| Random Forest | 89.2% | 0.90 | 0.89 | 0.892 |

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_api.py

# With coverage
pytest --cov=backend tests/
```

---

## 📁 Project Structure

```
cyberbullying-detection-ai/
├── backend/              # FastAPI backend
│   ├── main.py          # Main application
│   ├── config.py        # Configuration
│   ├── api/             # API routes
│   ├── models/          # ML models
│   ├── database/        # Database models
│   └── utils/           # Utilities
├── frontend/            # Web interface
│   ├── index.html       # Main page
│   ├── css/style.css    # Styles
│   └── js/app.js        # JavaScript
├── ml/                  # ML training
│   └── train.py         # Model training
├── tests/               # Tests
├── data/                # Data & models
└── requirements.txt     # Dependencies
```

---

## 🔧 Configuration

Edit `.env` file:
```
DATABASE_URL=sqlite:///./cyberbullying.db
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
```

---

## 📞 Support

For issues or questions, check the documentation or create an issue on GitHub.

---

## 📜 License

MIT License

---

**Made with ❤️ by AI & Team**
