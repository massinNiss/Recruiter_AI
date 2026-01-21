"""
RecruiterAI - FastAPI REST API
Data & AI Job Recommendation API - Focus Morocco
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn

from job_recommender import JobRecommender
from config import API_HOST, API_PORT, DEFAULT_TOP_K, MAX_TOP_K, PROJECT_NAME, PROJECT_TAGLINE

# Initialize FastAPI application
app = FastAPI(
    title=f"{PROJECT_NAME} API",
    description=f"{PROJECT_TAGLINE} - REST API for job recommendations with Morocco focus 🇲🇦",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Ajouter CORS pour permettre les requêtes depuis un frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialiser le recommender (sera fait au démarrage)
recommender: Optional[JobRecommender] = None


# Modèles Pydantic pour la validation
class CandidateProfile(BaseModel):
    """Profil candidat pour la recommandation"""
    profile_text: str = Field(
        ...,
        description="Description textuelle du profil candidat",
        example="Data Scientist avec 3 ans d'expérience en Machine Learning"
    )
    keywords: Optional[List[str]] = Field(
        None,
        description="Liste de compétences/mots-clés",
        example=["Python", "Machine Learning", "SQL", "TensorFlow"]
    )
    location_preference: Optional[str] = Field(
        None,
        description="Localisation préférée",
        example="Paris"
    )
    contract_type_preference: Optional[str] = Field(
        None,
        description="Type de contrat préféré",
        example="Full-time"
    )
    experience_level: Optional[str] = Field(
        None,
        description="Niveau d'expérience (junior, mid, senior, manager)",
        example="mid"
    )
    top_k: int = Field(
        DEFAULT_TOP_K,
        ge=1,
        le=MAX_TOP_K,
        description="Nombre de recommandations à retourner"
    )
    min_score: float = Field(
        0.0,
        ge=0.0,
        le=1.0,
        description="Score minimum pour filtrer les résultats"
    )


class RecommendationResponse(BaseModel):
    """Réponse avec les recommandations"""
    recommendations: List[dict]
    total_found: int
    search_params: dict


class JobDetailsResponse(BaseModel):
    """Détails complets d'une offre"""
    job: dict


class SimilarJobsResponse(BaseModel):
    """Offres similaires"""
    reference_job: dict
    similar_jobs: List[dict]


class StatsResponse(BaseModel):
    """Statistiques du système"""
    statistics: dict


# Events
@app.on_event("startup")
async def startup_event():
    """Initialize on API startup"""
    global recommender
    print("\n🤖 Starting RecruiterAI API...")
    recommender = JobRecommender()
    print("✅ RecruiterAI API ready to serve requests!\n")


# Endpoints
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint to verify API is running"""
    return {
        "message": "🤖 RecruiterAI API",
        "tagline": PROJECT_TAGLINE,
        "focus": "Morocco 🇲🇦",
        "status": "running",
        "version": "2.0.0",
        "endpoints": {
            "docs": "/docs",
            "recommend": "/api/v1/recommend",
            "recommend_cv": "/api/v1/recommend/cv",
            "job_details": "/api/v1/jobs/{job_id}",
            "similar_jobs": "/api/v1/jobs/{job_id}/similar",
            "statistics": "/api/v1/stats"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Vérification de santé de l'API"""
    return {
        "status": "healthy",
        "recommender_loaded": recommender is not None,
        "total_jobs": len(recommender.jobs_df) if recommender else 0
    }


@app.post("/api/v1/recommend", response_model=RecommendationResponse, tags=["Recommendations"])
async def recommend_jobs(profile: CandidateProfile):
    """
    Recommande des offres d'emploi basées sur un profil candidat
    
    - **profile_text**: Description du profil candidat
    - **keywords**: Liste optionnelle de compétences
    - **location_preference**: Localisation préférée
    - **contract_type_preference**: Type de contrat préféré
    - **experience_level**: Niveau d'expérience
    - **top_k**: Nombre de recommandations (max 50)
    - **min_score**: Score minimum
    """
    if not recommender:
        raise HTTPException(status_code=503, detail="Le système de recommandation n'est pas initialisé")
    
    try:
        recommendations = recommender.recommend(
            candidate_profile=profile.profile_text,
            keywords=profile.keywords,
            location_preference=profile.location_preference,
            contract_type_preference=profile.contract_type_preference,
            experience_level=profile.experience_level,
            top_k=profile.top_k,
            min_score=profile.min_score
        )
        
        return RecommendationResponse(
            recommendations=recommendations,
            total_found=len(recommendations),
            search_params={
                "keywords": profile.keywords,
                "location": profile.location_preference,
                "contract_type": profile.contract_type_preference,
                "experience_level": profile.experience_level,
                "top_k": profile.top_k,
                "min_score": profile.min_score
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la recommandation: {str(e)}")


@app.post("/api/v1/recommend/cv", response_model=RecommendationResponse, tags=["Recommendations"])
async def recommend_from_cv(
    cv_file: UploadFile = File(..., description="Fichier CV (PDF, DOCX, TXT)"),
    keywords: Optional[str] = Query(None, description="Mots-clés additionnels (séparés par des virgules)"),
    location_preference: Optional[str] = Query(None, description="Localisation préférée"),
    contract_type_preference: Optional[str] = Query(None, description="Type de contrat"),
    experience_level: Optional[str] = Query(None, description="Niveau d'expérience"),
    top_k: int = Query(DEFAULT_TOP_K, ge=1, le=MAX_TOP_K, description="Nombre de recommandations"),
    min_score: float = Query(0.0, ge=0.0, le=1.0, description="Score minimum")
):
    """
    Recommande des offres d'emploi basées sur un CV uploadé
    
    - **cv_file**: Fichier CV (formats supportés: PDF, DOCX, TXT)
    - **keywords**: Mots-clés additionnels (optionnel)
    - **location_preference**: Localisation préférée
    - **contract_type_preference**: Type de contrat préféré
    - **experience_level**: Niveau d'expérience
    - **top_k**: Nombre de recommandations
    - **min_score**: Score minimum
    """
    if not recommender:
        raise HTTPException(status_code=503, detail="Le système de recommandation n'est pas initialisé")
    
    # Lire le contenu du fichier
    try:
        cv_bytes = await cv_file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la lecture du fichier: {str(e)}")
    
    # Parser les keywords
    keywords_list = None
    if keywords:
        keywords_list = [k.strip() for k in keywords.split(',') if k.strip()]
    
    # Recommander
    try:
        recommendations = recommender.recommend_from_cv_bytes(
            cv_bytes=cv_bytes,
            cv_filename=cv_file.filename,
            additional_keywords=keywords_list,
            location_preference=location_preference,
            contract_type_preference=contract_type_preference,
            experience_level=experience_level,
            top_k=top_k,
            min_score=min_score
        )
        
        return RecommendationResponse(
            recommendations=recommendations,
            total_found=len(recommendations),
            search_params={
                "cv_filename": cv_file.filename,
                "keywords": keywords_list,
                "location": location_preference,
                "contract_type": contract_type_preference,
                "experience_level": experience_level,
                "top_k": top_k,
                "min_score": min_score
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la recommandation: {str(e)}")


@app.get("/api/v1/jobs/{job_id}", response_model=JobDetailsResponse, tags=["Jobs"])
async def get_job_details(job_id: int):
    """
    Récupère les détails complets d'une offre d'emploi
    
    - **job_id**: ID de l'offre
    """
    if not recommender:
        raise HTTPException(status_code=503, detail="Le système de recommandation n'est pas initialisé")
    
    try:
        job_details = recommender.get_job_details(job_id)
        return JobDetailsResponse(job=job_details)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


@app.get("/api/v1/jobs/{job_id}/similar", response_model=SimilarJobsResponse, tags=["Jobs"])
async def get_similar_jobs(
    job_id: int,
    top_k: int = Query(10, ge=1, le=50, description="Nombre d'offres similaires")
):
    """
    Trouve des offres similaires à une offre donnée
    
    - **job_id**: ID de l'offre de référence
    - **top_k**: Nombre d'offres similaires à retourner
    """
    if not recommender:
        raise HTTPException(status_code=503, detail="Le système de recommandation n'est pas initialisé")
    
    try:
        reference_job = recommender.get_job_details(job_id)
        similar_jobs = recommender.get_similar_jobs(job_id, top_k)
        
        return SimilarJobsResponse(
            reference_job=reference_job,
            similar_jobs=similar_jobs
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


@app.get("/api/v1/stats", response_model=StatsResponse, tags=["Statistics"])
async def get_statistics():
    """
    Retourne des statistiques sur les offres d'emploi
    
    Inclut: total d'offres, entreprises, localisations, compétences les plus demandées, etc.
    """
    if not recommender:
        raise HTTPException(status_code=503, detail="Le système de recommandation n'est pas initialisé")
    
    try:
        stats = recommender.get_statistics()
        return StatsResponse(statistics=stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


# Launch application
if __name__ == "__main__":
    print("\n" + "═"*80)
    print("🤖 RECRUITERAI - DATA & AI JOB RECOMMENDATION API")
    print("═"*80)
    print(f"🌐 Host: {API_HOST}")
    print(f"🔌 Port: {API_PORT}")
    print(f"📚 API Docs: http://localhost:{API_PORT}/docs")
    print(f"🇲🇦 Focus: Morocco")
    print("═"*80 + "\n")
    
    uvicorn.run(
        "api:app",
        host=API_HOST,
        port=API_PORT,
        reload=True,
        log_level="info"
    )
