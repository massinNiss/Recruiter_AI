
-- models/gold/dim_location.sql
-- Gold layer: Dimension Location
-- RecruiterAI - Enhanced with Morocco Focus

{{ config(
    materialized='table',
    schema='gold',
    tags=['gold', 'dimension'],
    unique_id='location_id',
    meta={'owner': 'recruiter_ai'}
) }}

WITH jobs AS (
    SELECT DISTINCT
        location_cleaned as location_raw
    FROM {{ ref('int_job_title_normalization') }}
    WHERE location_cleaned IS NOT NULL
),

location_parsed AS (
    SELECT
        location_raw,
        -- Extract city (before comma)
        CASE 
            WHEN POSITION(',' IN location_raw) > 0 
            THEN TRIM(SUBSTRING(location_raw, 1, POSITION(',' IN location_raw) - 1))
            ELSE location_raw
        END as city,
        
        -- Extract country (after comma)
        CASE 
            WHEN POSITION(',' IN location_raw) > 0 
            THEN TRIM(SUBSTRING(location_raw, POSITION(',' IN location_raw) + 1))
            ELSE 'Not Specified'
        END as country,
        
        -- Detect if remote
        CASE 
            WHEN LOWER(location_raw) LIKE '%remote%' 
            THEN 'Remote'
            ELSE 'On-site'
        END as work_location_type,
        
        -- Morocco region classification
        CASE 
            WHEN LOWER(location_raw) LIKE '%casablanca%' THEN 'Casablanca-Settat'
            WHEN LOWER(location_raw) LIKE '%rabat%' OR LOWER(location_raw) LIKE '%salé%' OR LOWER(location_raw) LIKE '%sale%' THEN 'Rabat-Salé-Kénitra'
            WHEN LOWER(location_raw) LIKE '%marrakech%' OR LOWER(location_raw) LIKE '%marrakesh%' THEN 'Marrakech-Safi'
            WHEN LOWER(location_raw) LIKE '%tanger%' OR LOWER(location_raw) LIKE '%tangier%' OR LOWER(location_raw) LIKE '%tetouan%' THEN 'Tanger-Tétouan-Al Hoceïma'
            WHEN LOWER(location_raw) LIKE '%fes%' OR LOWER(location_raw) LIKE '%fez%' OR LOWER(location_raw) LIKE '%meknes%' THEN 'Fès-Meknès'
            WHEN LOWER(location_raw) LIKE '%agadir%' THEN 'Souss-Massa'
            WHEN LOWER(location_raw) LIKE '%oujda%' OR LOWER(location_raw) LIKE '%nador%' THEN 'Oriental'
            WHEN LOWER(location_raw) LIKE '%kenitra%' OR LOWER(location_raw) LIKE '%kénitra%' THEN 'Rabat-Salé-Kénitra'
            WHEN LOWER(location_raw) LIKE '%mohammedia%' THEN 'Casablanca-Settat'
            WHEN LOWER(location_raw) LIKE '%el jadida%' THEN 'Casablanca-Settat'
            WHEN LOWER(location_raw) LIKE '%beni mellal%' THEN 'Béni Mellal-Khénifra'
            WHEN LOWER(location_raw) LIKE '%morocco%' OR LOWER(location_raw) LIKE '%maroc%' THEN 'Morocco (General)'
            ELSE NULL
        END as morocco_region,
        
        -- Priority flag for Morocco jobs
        CASE 
            WHEN LOWER(location_raw) LIKE '%morocco%' 
                OR LOWER(location_raw) LIKE '%maroc%'
                OR LOWER(location_raw) LIKE '%casablanca%'
                OR LOWER(location_raw) LIKE '%rabat%'
                OR LOWER(location_raw) LIKE '%marrakech%'
                OR LOWER(location_raw) LIKE '%tanger%'
                OR LOWER(location_raw) LIKE '%fes%'
                OR LOWER(location_raw) LIKE '%agadir%'
                OR LOWER(location_raw) LIKE '%oujda%'
                OR LOWER(location_raw) LIKE '%kenitra%'
                OR LOWER(location_raw) LIKE '%tetouan%'
                OR LOWER(location_raw) LIKE '%meknes%'
                OR LOWER(location_raw) LIKE '%salé%'
                OR LOWER(location_raw) LIKE '%mohammedia%'
            THEN TRUE
            ELSE FALSE
        END as is_morocco
    FROM jobs
),

ranked_locations AS (
    SELECT
        ROW_NUMBER() OVER (ORDER BY is_morocco DESC, location_raw) as location_id,
        location_raw,
        city,
        country,
        work_location_type,
        morocco_region,
        is_morocco,
        NOW() as created_at
    FROM location_parsed
)

SELECT
    location_id,
    location_raw,
    city,
    country,
    work_location_type,
    morocco_region,
    is_morocco,
    created_at
FROM ranked_locations
ORDER BY is_morocco DESC, location_id
