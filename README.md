# 🤖 RecruiterAI

![Status](https://img.shields.io/badge/Status-Active-green) ![Version](https://img.shields.io/badge/Version-2.0-blue) ![Focus](https://img.shields.io/badge/Focus-Morocco%20🇲🇦-red)

**Data & AI Job Analytics & Recommendation Platform**

> 🇲🇦 **Focus Morocco** - Find your dream Data & AI job in Morocco and beyond!

---

## 📚 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [DBT Models](#-dbt-models)
- [Recommendation System](#-recommendation-system)
- [Power BI](#-power-bi)
- [Documentation](#-documentation)
- [License](#-license)

---

## 🎯 About

**RecruiterAI** is a comprehensive Data Engineering & Analytics platform for analyzing and recommending Data & AI job opportunities. It centralizes **131,570+ job offers** from LinkedIn and provides:

1. ✅ Professional analytics structure (Bronze/Silver/Gold layers)
2. ✅ Data transformation with **DBT** (Data Build Tool)
3. ✅ Business insights (skills, trends, geography)
4. ✅ Interactive dashboards with **Power BI**
5. ✅ ML-powered job recommendation system
6. ✅ **Morocco-focused** location prioritization

### Project Constraints
- ✓ **100% Local** (no cloud required)
- ✓ **No Airflow** (Python-based orchestration)
- ✓ **No Docker** (direct execution)
- ✓ **No PostgreSQL** (local files + DuckDB)
- ✓ **DBT Transformation** required
- ✓ **BI with Power BI**

---

## ✨ Features

### 🔍 Job Analytics
- Analyze **131K+ job offers** from LinkedIn
- Track skill demand trends
- Geographic distribution analysis
- Company hiring patterns

### 🤖 AI Job Categories
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
- And more...

### 🇲🇦 Morocco Focus
- Priority filtering for Morocco jobs
- Morocco region classification:
  - Casablanca-Settat
  - Rabat-Salé-Kénitra
  - Marrakech-Safi
  - Tanger-Tétouan-Al Hoceïma
  - Fès-Meknès
  - Souss-Massa
  - Oriental

### 💡 Recommendation System
- Sentence-BERT semantic matching
- FAISS vector search
- CV parsing (PDF, DOCX, TXT)
- Multi-criteria scoring
- Real-time recommendations

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        SOURCE LAYER                             │
│             recruiter_ai_jobs_data.csv (131K rows)              │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────────────┐
│                      BRONZE LAYER                               │
│              (Raw data + basic renaming)                        │
│  • stg_jobs_raw | Materialization: VIEW                        │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────────────┐
│                      SILVER LAYER                               │
│          (Cleaning, Normalization, Enrichment)                 │
│                                                                 │
│  • int_jobs_cleaned                                            │
│  • int_job_title_normalization (AI Categories)                 │
│  • int_skills_extraction                                       │
│  • Materialization: TABLE                                      │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────────────┐
│                      GOLD LAYER                                 │
│             (Analytics-ready + Star Schema)                    │
│                                                                 │
│  Dimensions:                                                   │
│  • dim_time, dim_company, dim_location (Morocco regions),     │
│  • dim_skills                                                  │
│                                                                 │
│  Facts:                                                        │
│  • fact_job_offers, fact_job_skills                            │
│                                                                 │
│  Aggregates:                                                   │
│  • agg_job_offers_by_category_time                             │
│  • agg_skills_demand, agg_location_analysis                    │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────────────┐
│              RECOMMENDATION SYSTEM (Streamlit + API)            │
│                                                                 │
│  • Sentence-BERT embeddings                                    │
│  • FAISS vector index                                          │
│  • CV parsing & profile matching                               │
│  • Morocco priority scoring                                    │
└─────────────────────────────────────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────────────┐
│                    POWER BI (Visualizations)                    │
│                                                                 │
│  • Overview Dashboard                                          │
│  • AI Job Categories Analysis                                  │
│  • Skills Demand                                               │
│  • Morocco Geographic Analysis                                 │
│  • Company Analysis                                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
recruiter-ai/
├── 📄 recruiter_ai_jobs_data.csv        # Source data
├── 📄 README.md                         # This file
├── 🐍 run_pipeline.py                   # Pipeline orchestration
│
├── data/
│   ├── bronze/                          # Raw data layer
│   ├── silver/                          # Cleaned data layer
│   └── gold/                            # Analytics layer (CSV exports)
│       ├── dim_time.csv
│       ├── dim_company.csv
│       ├── dim_location.csv             # With Morocco regions
│       ├── dim_skills.csv
│       ├── fact_job_offers.csv
│       ├── fact_job_skills.csv
│       └── agg_*.csv
│
├── dbt/
│   ├── dbt_project.yml                  # DBT configuration
│   ├── profiles.yml                     # Database connectors
│   ├── recruiter_ai.db                  # DuckDB database
│   └── models/
│       ├── bronze/
│       ├── silver/                      # AI job categories
│       └── gold/                        # Morocco focus
│
├── recommender/
│   ├── app.py                           # Streamlit UI
│   ├── api.py                           # FastAPI endpoints
│   ├── job_recommender.py               # ML recommendation engine
│   ├── cv_parser.py                     # CV parsing
│   ├── config.py                        # Configuration
│   └── data/
│       ├── embeddings/                  # BERT embeddings
│       └── models/                      # Trained models
│
└── dashboards/
    ├── recruiter_ai_dashboard.pbix      # Power BI dashboard
    ├── recruiter_ai_theme.json          # Power BI theme
    └── README.md                        # Power BI guide
```

---

## 🚀 Installation

### Prerequisites

```bash
# Python 3.8+
python --version

# Install packages
pip install dbt-core dbt-duckdb pandas openpyxl

# For recommendation system
pip install sentence-transformers faiss-cpu streamlit fastapi uvicorn python-docx PyPDF2
```

### Steps

1. **Clone/Download the project**
   ```bash
   cd path/to/recruiter-ai
   ```

2. **Install DBT dependencies**
   ```bash
   cd dbt
   dbt deps
   dbt debug
   ```

3. **Verify source data**
   ```bash
   # Ensure recruiter_ai_jobs_data.csv is present
   dir recruiter_ai_jobs_data.csv
   ```

---

## 💻 Usage

### Option 1: Python Pipeline (Recommended)

```bash
# From project root
python run_pipeline.py
```

**This script automatically:**
1. ✓ Checks dependencies
2. ✓ Copies data to Bronze layer
3. ✓ Runs `dbt run`
4. ✓ Executes DBT tests
5. ✓ Exports Gold tables to CSV
6. ✓ Generates final report

### Option 2: Manual DBT Execution

```bash
cd dbt

# Debug
dbt debug

# Run transformations
dbt run

# Run tests (optional)
dbt test

# Generate docs (optional)
dbt docs generate
dbt docs serve
```

### Option 3: Recommendation System

```bash
cd recommender

# Run Streamlit app
streamlit run app.py

# Or run API
uvicorn api:app --reload
```

---

## 📊 DBT Models

### Bronze Layer
| Model | Type | Rows | Description |
|-------|------|------|-------------|
| `stg_jobs_raw` | VIEW | ~131K | Raw CSV data |

### Silver Layer
| Model | Type | Rows | Description |
|-------|------|------|-------------|
| `int_jobs_cleaned` | TABLE | ~131K | Text cleaning + dates |
| `int_job_title_normalization` | TABLE | ~100K | AI job categories |
| `int_skills_extraction` | TABLE | ~500K | Skill extraction |

### Gold Layer - Dimensions
| Model | Type | Rows | Description |
|-------|------|------|-------------|
| `dim_time` | TABLE | ~2K | Date dimension |
| `dim_company` | TABLE | ~5K | Company dimension |
| `dim_location` | TABLE | ~3K | Location + Morocco regions |
| `dim_skills` | TABLE | ~30 | Skills dimension |

### Gold Layer - Facts
| Model | Type | Rows | Description |
|-------|------|------|-------------|
| `fact_job_offers` | TABLE | ~100K | Job offers fact |
| `fact_job_skills` | TABLE | ~500K | Job-skill relationships |

---

## 🤖 Recommendation System

The ML-powered recommendation system uses:

- **Sentence-BERT** for semantic embeddings
- **FAISS** for fast vector search
- **Multi-criteria scoring** with Morocco priority

### Features
- Manual profile input or CV upload
- Morocco location prioritization
- AI skill highlighting
- Experience level filtering
- Contract type filtering

### Running the App

```bash
cd recommender
streamlit run app.py
```

Access at: `http://localhost:8501`

---

## 📈 Power BI

### Import Data

1. Open **Power BI Desktop**
2. **Get Data → Text/CSV**
3. Load tables from `data/gold/`:
   - dim_time.csv
   - dim_company.csv
   - dim_location.csv (includes Morocco regions)
   - dim_skills.csv
   - fact_job_offers.csv
   - fact_job_skills.csv

### Create Relationships

| From | To | Cardinality |
|------|----|-------------|
| fact_job_offers[company_id] | dim_company[company_id] | Many:One |
| fact_job_offers[location_id] | dim_location[location_id] | Many:One |
| fact_job_offers[published_date_id] | dim_time[date_id] | Many:One |
| fact_job_skills[job_offer_id] | fact_job_offers[job_offer_id] | Many:One |
| fact_job_skills[skill_id] | dim_skills[skill_id] | Many:One |

### Recommended Theme

```json
{
  "name": "RecruiterAI Theme",
  "dataColors": ["#6366F1", "#8B5CF6", "#10B981", "#C1272D", "#006233", "#F59E0B"],
  "background": "#0F172A",
  "foreground": "#F8FAFC",
  "tableAccent": "#6366F1"
}
```

---

## 📚 Documentation

See the `dashboards/` folder for detailed Power BI setup instructions.

---

## 🛠️ Maintenance

### Update Data

```bash
# Replace recruiter_ai_jobs_data.csv with new data
# Then run:
python run_pipeline.py
```

### Add New AI Skills

Edit `dbt/models/silver/int_skills_extraction.sql`:
```sql
UNION ALL SELECT 'New AI Skill', 'pattern_regex'
```

### Add New Job Categories

Edit `dbt/models/silver/int_job_title_normalization.sql`:
```sql
WHEN job_title_cleaned LIKE '%new category%' THEN 'New Category Name'
```

---

## 📋 Checklist

- [ ] Install dependencies
- [ ] Verify `recruiter_ai_jobs_data.csv` present
- [ ] Run `python run_pipeline.py`
- [ ] Check CSV files in `data/gold/`
- [ ] Test Streamlit app: `cd recommender && streamlit run app.py`
- [ ] Import data in Power BI
- [ ] Create relationships
- [ ] Build dashboards

---

## 🚀 Future Improvements

- [ ] Real-time job scraping from LinkedIn
- [ ] Enhanced Morocco job sources
- [ ] Mobile app for job alerts
- [ ] Integration with job application systems
- [ ] Advanced ML models for better matching

---

## 📄 License

Personal Project - Free to use

---

## ✨ Author

Massine Niharmine

**RecruiterAI** - Data & AI Job Analytics Platform  
Focus: Morocco 🇲🇦  
Version: 2.0  
Created: January 2026

---

**Need help?** Check the logs in `dbt/logs/` or recommender documentation.

