
-- models/silver/int_job_title_normalization.sql
-- Silver layer: Normaliser les intitulés de postes
-- RecruiterAI - Enhanced for Data & AI Job Categories

{{ config(
    materialized='table',
    schema='silver',
    tags=['silver', 'normalization'],
    meta={'owner': 'recruiter_ai'}
) }}

WITH cleaned_jobs AS (
    SELECT * FROM {{ ref('int_jobs_cleaned') }}
),

title_normalized AS (
    SELECT
        *,
        CASE
            -- AI/ML Roles (Priority - Most Specific First)
            WHEN job_title_cleaned LIKE '%llm%' OR job_title_cleaned LIKE '%large language model%' OR job_title_cleaned LIKE '%generative ai%' OR job_title_cleaned LIKE '%genai%' THEN 'GenAI/LLM Engineer'
            WHEN job_title_cleaned LIKE '%nlp%' OR job_title_cleaned LIKE '%natural language processing%' THEN 'NLP Engineer'
            WHEN job_title_cleaned LIKE '%computer vision%' OR job_title_cleaned LIKE '%cv engineer%' OR job_title_cleaned LIKE '%image recognition%' THEN 'Computer Vision Engineer'
            WHEN job_title_cleaned LIKE '%deep learning%' THEN 'Deep Learning Engineer'
            WHEN job_title_cleaned LIKE '%mlops%' OR job_title_cleaned LIKE '%ml ops%' OR job_title_cleaned LIKE '%machine learning ops%' THEN 'MLOps Engineer'
            WHEN job_title_cleaned LIKE '%ai engineer%' OR job_title_cleaned LIKE '%artificial intelligence engineer%' THEN 'AI Engineer'
            WHEN job_title_cleaned LIKE '%ml engineer%' OR job_title_cleaned LIKE '%machine learning engineer%' THEN 'ML Engineer'
            WHEN job_title_cleaned LIKE '%machine learning%' OR job_title_cleaned LIKE '%ml specialist%' THEN 'ML Engineer'
            
            -- Data Science & Analytics Roles
            WHEN job_title_cleaned LIKE '%data scientist%' THEN 'Data Scientist'
            WHEN job_title_cleaned LIKE '%data engineer%' THEN 'Data Engineer'
            WHEN job_title_cleaned LIKE '%data analyst%' THEN 'Data Analyst'
            WHEN job_title_cleaned LIKE '%analytics engineer%' THEN 'Analytics Engineer'
            WHEN job_title_cleaned LIKE '%data architect%' THEN 'Data Architect'
            WHEN job_title_cleaned LIKE '%bi developer%' OR job_title_cleaned LIKE '%business intelligence%' THEN 'BI Developer'
            WHEN job_title_cleaned LIKE '%etl%' OR job_title_cleaned LIKE '%pipeline%' THEN 'ETL/Pipeline Engineer'
            
            ELSE 'Other Data/AI Role'
        END as job_category,
        
        CASE
            WHEN contract_type_cleaned LIKE '%cdi%' OR contract_type_cleaned LIKE '%permanent%' OR contract_type_cleaned LIKE '%full-time%' OR contract_type_cleaned LIKE '%full time%' THEN 'Full-time'
            WHEN contract_type_cleaned LIKE '%cdd%' OR contract_type_cleaned LIKE '%contract%' THEN 'Contract'
            WHEN contract_type_cleaned LIKE '%stage%' OR contract_type_cleaned LIKE '%internship%' OR contract_type_cleaned LIKE '%intern%' THEN 'Internship'
            WHEN contract_type_cleaned LIKE '%freelance%' THEN 'Freelance'
            WHEN contract_type_cleaned LIKE '%part-time%' OR contract_type_cleaned LIKE '%part time%' THEN 'Part-time'
            ELSE 'Not Specified'
        END as contract_type_normalized,
        
        CASE
            WHEN work_type_cleaned LIKE '%remote%' THEN 'Remote'
            WHEN work_type_cleaned LIKE '%hybrid%' THEN 'Hybrid'
            WHEN work_type_cleaned LIKE '%onsite%' OR work_type_cleaned LIKE '%on-site%' OR work_type_cleaned LIKE '%on site%' THEN 'On-site'
            ELSE 'Not Specified'
        END as work_type_normalized
    
    FROM cleaned_jobs
    WHERE dedup_rank = 1  -- Keep only first occurrence (most recent)
)

SELECT * FROM title_normalized
