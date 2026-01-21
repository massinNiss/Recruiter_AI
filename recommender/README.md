# 🤖 RecruiterAI - Recommendation System

**AI-Powered Job Recommendation Engine**  
Focus: Data & AI Jobs in Morocco 🇲🇦

---

## 📋 Overview

The RecruiterAI Recommendation System uses advanced NLP and machine learning to match candidates with relevant Data & AI job opportunities. It features:

- **Sentence-BERT** for semantic text embeddings
- **FAISS** for lightning-fast vector similarity search
- **Multi-criteria scoring** with Morocco location priority
- **CV Parsing** for automatic profile extraction

---

## ✨ Features

### 🔍 Search Methods
- **Manual Profile Input**: Describe your skills and experience
- **CV Upload**: Upload PDF, DOCX, or TXT resumes

### 🎯 Smart Matching
- Semantic similarity using transformer embeddings
- Skill-based matching with AI skill highlighting
- Experience level filtering
- Contract type preferences

### 🇲🇦 Morocco Focus
- Priority scoring for Morocco-based jobs
- Morocco city quick-select filters
- Region-specific recommendations
- Morocco job highlighting in results

### 💡 AI Job Categories
- AI Engineer
- ML Engineer
- GenAI/LLM Engineer
- NLP Engineer
- Computer Vision Engineer
- Deep Learning Engineer
- MLOps Engineer
- Data Scientist
- Data Engineer
- Data Analyst

---

## 🚀 Quick Start

### Prerequisites

```bash
pip install -r requirements.txt
```

Required packages:
- `sentence-transformers` - BERT embeddings
- `faiss-cpu` - Vector search
- `streamlit` - Web UI
- `fastapi` - REST API
- `uvicorn` - ASGI server
- `pandas` - Data handling
- `python-docx` - DOCX parsing
- `PyPDF2` - PDF parsing
- `spacy` - NLP processing

### Run Streamlit App

```bash
cd recommender
streamlit run app.py
```

Access at: **http://localhost:8501**

### Run API Server

```bash
cd recommender
uvicorn api:app --reload --port 8000
```

API docs at: **http://localhost:8000/docs**

---

## 📁 Project Structure

```
recommender/
├── app.py                    # Streamlit UI application
├── api.py                    # FastAPI REST endpoints
├── job_recommender.py        # Core recommendation engine
├── cv_parser.py              # CV/Resume parsing
├── data_preprocessing.py     # Data preprocessing
├── config.py                 # Configuration & settings
├── requirements.txt          # Dependencies
├── README.md                 # This file
│
├── assets/                   # UI assets
│
└── data/
    ├── embeddings/           # Pre-computed embeddings
    │   ├── job_embeddings.npy
    │   ├── jobs_processed.pkl
    │   └── faiss_index.bin
    └── models/               # Trained models
```

---

## 🎨 UI Features

### Modern Design
- Glassmorphism design aesthetic
- Gradient color scheme (Indigo → Purple)
- Morocco flag colors accent
- Responsive layout
- Dark mode optimized

### Job Cards
- Score badge with percentage
- Morocco priority indicator 🇲🇦
- AI skill highlighting
- Expandable descriptions
- Direct apply links

### Analytics
- Search result statistics
- Location distribution charts
- Skill demand analysis
- Company diversity metrics

---

## 🔧 Configuration

Edit `config.py` to customize:

### Morocco Cities
```python
MOROCCO_CITIES = [
    'casablanca', 'rabat', 'marrakech', 'fes',
    'tanger', 'agadir', 'meknes', 'oujda', ...
]
```

### Scoring Weights
```python
SCORING_WEIGHTS = {
    'semantic_similarity': 0.30,
    'skills_match': 0.25,
    'location_match': 0.25,
    'morocco_priority': 0.10,
    'contract_type_match': 0.05,
    'experience_match': 0.05
}
```

### AI Skills
```python
DATA_SKILLS = [
    'Large Language Models', 'LLM', 'GPT',
    'Machine Learning', 'Deep Learning',
    'Natural Language Processing', 'NLP',
    ...
]
```

---

## 📡 API Endpoints

### `POST /recommend`
Get job recommendations for a candidate profile.

```json
{
  "profile": "AI Engineer with 3 years of NLP experience",
  "keywords": ["Python", "LLM", "NLP"],
  "location_preference": "Morocco",
  "top_k": 10
}
```

### `POST /recommend-from-cv`
Upload CV and get recommendations.

### `GET /jobs/{job_id}`
Get details for a specific job.

### `GET /statistics`
Get platform statistics.

### `GET /health`
Health check endpoint.

---

## 🧠 How It Works

### 1. Embedding Generation
- Job descriptions are encoded using Sentence-BERT
- Multilingual model supports English, French, Arabic

### 2. Index Building
- FAISS index stores job embeddings
- Enables sub-millisecond similarity search

### 3. Candidate Matching
```
Candidate Profile → BERT Embedding → FAISS Search → Top K Jobs
                                          ↓
                                  Multi-Criteria Scoring
                                          ↓
                                  Morocco Priority Boost
                                          ↓
                                  Ranked Recommendations
```

### 4. Scoring Formula
```
Final Score = 
    (semantic_similarity × 0.30) +
    (skills_match × 0.25) +
    (location_match × 0.25) +
    (morocco_priority × 0.10) +
    (contract_type_match × 0.05) +
    (experience_match × 0.05)
```

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| Jobs Indexed | 100K+ |
| Query Time | < 100ms |
| Embedding Dim | 512 |
| Index Type | FAISS Flat |

---

## 🛠️ Development

### Rebuild Embeddings
```python
from job_recommender import JobRecommender
recommender = JobRecommender(force_reload=True)
```

### Add New Skills
Edit `config.py` → `DATA_SKILLS` list

### Test Installation
```bash
python test_installation.py
```

---

## 📝 Example Usage

### Python API
```python
from job_recommender import JobRecommender

# Initialize
recommender = JobRecommender()

# Get recommendations
results = recommender.recommend(
    candidate_profile="AI Engineer with LLM expertise",
    keywords=["Python", "LangChain", "NLP"],
    location_preference="Morocco",
    top_k=10
)

for job in results:
    print(f"{job['title']} at {job['company']} - Score: {job['score']:.2%}")
```

### From CV
```python
results = recommender.recommend_from_cv_file(
    cv_path="path/to/cv.pdf",
    location_preference="Casablanca"
)
```

---

## 🇲🇦 Morocco Priority

Jobs in Morocco receive a scoring boost:

1. **Location Detection**: Matches Morocco cities/keywords
2. **Priority Flag**: `is_morocco` in location dimension
3. **Score Boost**: +10% via `morocco_priority` weight
4. **UI Highlight**: 🇲🇦 badge on Morocco jobs

---

## 📞 Support

For issues:
1. Check `config.py` settings
2. Verify data files exist in `data/gold/`
3. Run `python test_installation.py`
4. Check DBT pipeline output

---

**RecruiterAI** - Data & AI Job Recommendation  
Focus: Morocco 🇲🇦  
Version: 2.0

Happy job hunting (MSN)! 🚀
