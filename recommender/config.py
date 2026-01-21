"""
RecruiterAI - Configuration centralisée pour le système de recommandation
Data & AI Job Analytics & Recommendation Platform - Focus Morocco
"""
import os
from pathlib import Path

# ============================================================================
# PROJECT BRANDING
# ============================================================================
PROJECT_NAME = "RecruiterAI"
PROJECT_TAGLINE = "Data & AI Job Analytics & Recommendation Platform"
PROJECT_VERSION = "2.0.0"
PROJECT_FOCUS = "Morocco"

# ============================================================================
# FILE PATHS
# ============================================================================
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR
MODEL_DIR = Path(__file__).parent / "data" / "models"
EMBEDDINGS_DIR = Path(__file__).parent / "data" / "embeddings"

# Create directories if needed
MODEL_DIR.mkdir(parents=True, exist_ok=True)
EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

# Gold Layer Data Files
GOLD_DIR = DATA_DIR / "data" / "gold"
FACT_JOBS_PATH = GOLD_DIR / "fact_job_offers.csv"
DIM_COMPANY_PATH = GOLD_DIR / "dim_company.csv"
DIM_LOCATION_PATH = GOLD_DIR / "dim_location.csv"
FACT_SKILLS_PATH = GOLD_DIR / "fact_job_skills.csv"

# Model Artifacts Paths
EMBEDDINGS_PATH = EMBEDDINGS_DIR / "job_embeddings.npy"
JOBS_PROCESSED_PATH = EMBEDDINGS_DIR / "jobs_processed.pkl"
FAISS_INDEX_PATH = EMBEDDINGS_DIR / "faiss_index.bin"

# ============================================================================
# NLP MODEL CONFIGURATION
# ============================================================================
EMBEDDING_MODEL_NAME = "sentence-transformers/distiluse-base-multilingual-cased-v2"
EMBEDDING_DIMENSION = 512
SPACY_MODEL = "fr_core_news_lg"  # Supports French & multilingual

# ============================================================================
# MOROCCO-SPECIFIC LOCATIONS
# ============================================================================
MOROCCO_CITIES = [
    # Major Cities
    'casablanca', 'rabat', 'marrakech', 'marrakesh', 'fes', 'fez',
    'tanger', 'tangier', 'agadir', 'meknes', 'oujda', 'kenitra', 'kénitra',
    
    # Secondary Cities
    'tetouan', 'tétouan', 'salé', 'sale', 'mohammedia', 'el jadida',
    'beni mellal', 'nador', 'khouribga', 'settat', 'safi', 'taza',
    'larache', 'khemisset', 'berrechid', 'taourirt', 'berkane',
    
    # Tech Hubs
    'casablanca technopark', 'rabat technopolis', 'tanger free zone',
    
    # Country identifiers
    'morocco', 'maroc', 'ma'
]

MOROCCO_REGIONS = {
    'Casablanca-Settat': ['casablanca', 'mohammedia', 'el jadida', 'settat', 'berrechid'],
    'Rabat-Salé-Kénitra': ['rabat', 'salé', 'sale', 'kenitra', 'kénitra', 'khemisset'],
    'Marrakech-Safi': ['marrakech', 'marrakesh', 'safi'],
    'Tanger-Tétouan-Al Hoceïma': ['tanger', 'tangier', 'tetouan', 'tétouan', 'larache'],
    'Fès-Meknès': ['fes', 'fez', 'meknes', 'taza'],
    'Souss-Massa': ['agadir'],
    'Oriental': ['oujda', 'nador', 'berkane', 'taourirt'],
    'Béni Mellal-Khénifra': ['beni mellal', 'khouribga']
}

# ============================================================================
# DATA & AI SKILLS (Enhanced for AI Focus)
# ============================================================================
DATA_SKILLS = [
    # ========== AI & Machine Learning (Priority) ==========
    # Generative AI & LLMs
    'Large Language Models', 'LLM', 'GPT', 'GPT-4', 'ChatGPT', 'Claude', 'Gemini', 'Llama',
    'Prompt Engineering', 'LangChain', 'LlamaIndex', 'RAG', 'Retrieval Augmented Generation',
    'Generative AI', 'GenAI', 'Diffusion Models', 'Stable Diffusion', 'DALL-E', 'Midjourney',
    'Fine-tuning', 'RLHF', 'Instruction Tuning', 'LoRA', 'QLoRA',
    
    # Core ML/DL
    'Machine Learning', 'Deep Learning', 'Artificial Intelligence', 'Neural Networks',
    'Reinforcement Learning', 'Transfer Learning', 'Federated Learning',
    'TensorFlow', 'PyTorch', 'Keras', 'JAX', 'Sklearn', 'Scikit-learn',
    'XGBoost', 'LightGBM', 'CatBoost', 'Random Forest', 'Gradient Boosting',
    
    # NLP
    'Natural Language Processing', 'NLP', 'BERT', 'Transformers', 'Hugging Face',
    'Sentiment Analysis', 'Named Entity Recognition', 'Text Classification',
    'Question Answering', 'Text Generation', 'Summarization', 'spaCy', 'NLTK',
    
    # Computer Vision
    'Computer Vision', 'OpenCV', 'YOLO', 'Object Detection', 'Image Classification',
    'Image Segmentation', 'Face Recognition', 'OCR', 'Video Analytics',
    
    # MLOps & Model Deployment
    'MLOps', 'ML Pipeline', 'Model Deployment', 'Model Monitoring', 'Model Serving',
    'MLflow', 'Kubeflow', 'SageMaker', 'Vertex AI', 'Azure ML',
    'Feature Store', 'Model Registry', 'A/B Testing ML', 'Experiment Tracking',
    
    # Vector Databases & Embeddings
    'Vector Database', 'Pinecone', 'Milvus', 'Weaviate', 'Chroma', 'Qdrant',
    'FAISS', 'Embeddings', 'Semantic Search', 'Similarity Search',
    
    # ========== Programming Languages ==========
    'Python', 'R', 'Java', 'Scala', 'Julia', 'C++', 'C#', 'JavaScript', 'TypeScript',
    'Go', 'Rust', 'MATLAB', 'SAS', 'VBA',
    
    # ========== Databases & SQL ==========
    'SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Cassandra', 'DynamoDB',
    'Oracle', 'SQL Server', 'NoSQL', 'Neo4j', 'Elasticsearch', 'SQLite',
    'Snowflake', 'BigQuery', 'Redshift', 'Databricks', 'Teradata', 'Hive',
    
    # ========== Data Engineering & Big Data ==========
    'ETL', 'ELT', 'Data Pipeline', 'Data Warehouse', 'Data Lake', 'Data Mesh',
    'Spark', 'PySpark', 'Hadoop', 'Kafka', 'Flink', 'Airflow', 'Prefect', 'Dagster',
    'dbt', 'Fivetran', 'Talend', 'NiFi', 'Parquet', 'Delta Lake', 'Iceberg',
    'Dask', 'Polars', 'Ray', 'Beam',
    
    # ========== Data Visualization & BI ==========
    'Tableau', 'Power BI', 'Looker', 'Metabase', 'Superset', 'Grafana',
    'D3.js', 'Plotly', 'Matplotlib', 'Seaborn', 'Streamlit', 'Dash',
    
    # ========== Cloud Platforms ==========
    'AWS', 'Azure', 'GCP', 'Google Cloud', 'Cloud Computing',
    'S3', 'EC2', 'Lambda', 'EMR', 'Glue', 'Athena',
    'Azure Data Factory', 'Azure Synapse', 'Azure Databricks',
    'Cloud Functions', 'Cloud Run', 'Dataflow', 'Dataproc',
    
    # ========== DevOps & Infrastructure ==========
    'Git', 'GitHub', 'GitLab', 'Docker', 'Kubernetes', 'Helm',
    'Jenkins', 'CI/CD', 'GitHub Actions', 'Terraform', 'Ansible',
    'Linux', 'Bash', 'Shell',
    
    # ========== Statistics & Analytics ==========
    'Statistics', 'Data Analysis', 'Data Analytics', 'Time Series',
    'Forecasting', 'A/B Testing', 'Hypothesis Testing', 'Exploratory Data Analysis',
    
    # ========== Soft Skills ==========
    'Communication', 'Leadership', 'Problem Solving', 'Teamwork', 'Agile', 'Scrum'
]

# Skill Aliases (Alias: Canonical Name)
SKILL_ALIASES = {
    # AI/ML
    'ai': 'Artificial Intelligence',
    'artificial intelligence': 'Artificial Intelligence',
    'machine learning': 'Machine Learning',
    'ml': 'Machine Learning',
    'dl': 'Deep Learning',
    'deep learning': 'Deep Learning',
    'nlp': 'Natural Language Processing',
    'natural language processing': 'Natural Language Processing',
    'genai': 'Generative AI',
    'generative ai': 'Generative AI',
    'llm': 'Large Language Models',
    'llms': 'Large Language Models',
    'large language models': 'Large Language Models',
    'rag': 'Retrieval Augmented Generation',
    'cv': 'Computer Vision',
    'computer vision': 'Computer Vision',
    
    # Cloud
    'google cloud platform': 'GCP',
    'google cloud': 'GCP',
    'gcp': 'GCP',
    'amazon web services': 'AWS',
    'aws': 'AWS',
    'microsoft azure': 'Azure',
    'azure': 'Azure',
    
    # Tools
    'pyspark': 'Spark',
    'spark': 'Spark',
    'scikit-learn': 'Sklearn',
    'sklearn': 'Sklearn',
    'k8s': 'Kubernetes',
    'tf': 'TensorFlow',
    'tensorflow': 'TensorFlow',
    'hf': 'Hugging Face',
    'huggingface': 'Hugging Face',
    
    # BI
    'bi': 'Business Intelligence',
    'business intelligence': 'Business Intelligence',
    'pbi': 'Power BI',
    'power bi': 'Power BI'
}

# ============================================================================
# EXPERIENCE LEVELS
# ============================================================================
EXPERIENCE_LEVELS = {
    'junior': ['junior', 'entry level', 'entry-level', 'débutant', 'graduate', '0-2 ans', '0-2 years', 'fresher'],
    'mid': ['mid-level', 'intermediate', 'confirmé', '2-5 ans', '3-5 years', '2-5 years', 'experienced'],
    'senior': ['senior', 'expert', 'lead', 'principal', 'staff', '5+ ans', '5+ years', '7+ years', 'specialist'],
    'manager': ['manager', 'head of', 'director', 'vp', 'chief', 'responsable', 'team lead', 'tech lead']
}

# ============================================================================
# SCORING WEIGHTS (Enhanced for Morocco Priority)
# ============================================================================
SCORING_WEIGHTS = {
    'semantic_similarity': 0.30,
    'skills_match': 0.25,
    'location_match': 0.25,        # Increased for Morocco focus
    'morocco_priority': 0.10,      # Bonus for Morocco jobs
    'contract_type_match': 0.05,
    'experience_match': 0.05
}

# ============================================================================
# SEARCH PARAMETERS
# ============================================================================
DEFAULT_TOP_K = 10
MAX_TOP_K = 50

# ============================================================================
# API CONFIGURATION
# ============================================================================
API_HOST = "0.0.0.0"
API_PORT = 8000
API_RELOAD = True
API_TITLE = "RecruiterAI API"
API_DESCRIPTION = "Data & AI Job Recommendation API - Focus Morocco"

# ============================================================================
# LOGGING
# ============================================================================
LOG_LEVEL = "INFO"

# ============================================================================
# UI THEME (For Streamlit)
# ============================================================================
UI_THEME = {
    'primary_color': '#6366F1',      # Indigo
    'secondary_color': '#8B5CF6',    # Purple
    'accent_color': '#10B981',       # Emerald
    'morocco_red': '#C1272D',        # Morocco flag red
    'morocco_green': '#006233',      # Morocco flag green
    'background_dark': '#0F172A',    # Slate 900
    'background_light': '#1E293B',   # Slate 800
    'text_primary': '#F8FAFC',       # Slate 50
    'text_secondary': '#94A3B8',     # Slate 400
}
