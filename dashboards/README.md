# 📊 RecruiterAI - Power BI Dashboard

Data & AI Job Analytics & Recommendation Platform - Focus Morocco 🇲🇦

This folder contains the Power BI dashboard for visualizing Data & AI job market trends.

## 📸 Dashboard Preview

![Dashboard Power BI](dashboard_preview.png)

## 📁 Files

### `recruiter_ai_dashboard.pbix`
The Power BI file containing all dashboards, reports, and visualizations.


---

## ✨ Dashboard Features

The dashboard provides comprehensive analysis of Data & AI job offers:

### 📊 Views Available
- **Overview** - Key metrics, KPIs, and trends
- **AI Job Categories** - Distribution of AI/ML/Data roles
- **Skills Demand** - Top skills and trends
- **Morocco Analysis** - Focus on Morocco job market 🇲🇦
- **Geographic Distribution** - Global job locations
- **Company Analysis** - Top hiring companies

### 🇲🇦 Morocco-Specific Features
- Morocco region filter
- Morocco priority indicator
- Regional breakdown:
  - Draa Tafilalt (Tinghir)
  - Casablanca-Settat
  - Rabat-Salé-Kénitra
  - Marrakech-Safi
  - Tanger-Tétouan-Al Hoceïma
  - Fès-Meknès
  - Souss-Massa

---

## 🎨 RecruiterAI Theme

### Recommended Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Primary (Indigo) | `#6366F1` | Main accent |
| Secondary (Purple) | `#8B5CF6` | Secondary elements |
| Accent (Emerald) | `#10B981` | Success/positive |
| Morocco Red | `#C1272D` | Morocco highlight |
| Morocco Green | `#006233` | Morocco highlight |
| Warning (Amber) | `#F59E0B` | Warnings |

### Power BI Theme JSON

Save this as `recruiter_ai_theme.json` and import in Power BI:

```json
{
  "name": "RecruiterAI Theme",
  "dataColors": [
    "#6366F1",
    "#8B5CF6",
    "#10B981",
    "#C1272D",
    "#006233",
    "#F59E0B",
    "#EC4899",
    "#14B8A6",
    "#F97316",
    "#06B6D4"
  ],
  "background": "#0F172A",
  "foreground": "#F8FAFC",
  "tableAccent": "#6366F1",
  "visualStyles": {
    "*": {
      "*": {
        "background": [{"color": {"solid": {"color": "#1E293B"}}}],
        "foreground": [{"color": {"solid": {"color": "#F8FAFC"}}}],
        "border": [{"color": {"solid": {"color": "#334155"}}}]
      }
    }
  }
}
```

### How to Apply Theme
1. Open Power BI Desktop
2. Go to **View** → **Themes** → **Browse for themes**
3. Select the `recruiter_ai_theme.json` file
4. Apply to your report

---

## 🚀 Getting Started

### Step 1: Import Data

1. Open **Power BI Desktop** (free download: https://powerbi.microsoft.com/)
2. Click **Get Data** → **Text/CSV**
3. Navigate to `data/gold/` folder
4. Import tables in this order:
   - `dim_time.csv`
   - `dim_company.csv`
   - `dim_location.csv` ← **Contains Morocco regions!**
   - `dim_skills.csv`
   - `fact_job_offers.csv`
   - `fact_job_skills.csv`

### Step 2: Create Relationships

Navigate to **Model View** and create these relationships:

| From Table | From Column | To Table | To Column | Type |
|------------|-------------|----------|-----------|------|
| fact_job_offers | company_id | dim_company | company_id | Many:1 |
| fact_job_offers | location_id | dim_location | location_id | Many:1 |
| fact_job_offers | published_date_id | dim_time | date_id | Many:1 |
| fact_job_skills | job_offer_id | fact_job_offers | job_offer_id | Many:1 |
| fact_job_skills | skill_id | dim_skills | skill_id | Many:1 |

### Step 3: Create Key Measures

Add these DAX measures:

```dax
// Total Job Offers
Total Jobs = COUNTROWS(fact_job_offers)

// Morocco Jobs
Morocco Jobs = 
CALCULATE(
    COUNTROWS(fact_job_offers),
    dim_location[is_morocco] = TRUE
)

// Morocco Job Percentage
Morocco Job % = 
DIVIDE([Morocco Jobs], [Total Jobs], 0)

// AI/ML Jobs
AI ML Jobs = 
CALCULATE(
    COUNTROWS(fact_job_offers),
    fact_job_offers[job_category] IN {
        "AI Engineer", "ML Engineer", "GenAI/LLM Engineer",
        "NLP Engineer", "Deep Learning Engineer", "MLOps Engineer",
        "Computer Vision Engineer"
    }
)

// Average Skills per Job
Avg Skills per Job = 
DIVIDE(
    COUNTROWS(fact_job_skills),
    COUNTROWS(fact_job_offers),
    0
)
```

---

## 📈 Recommended Visualizations

### Page 1: Overview
- **Card Visuals**: Total Jobs, Morocco Jobs, AI Jobs, Companies
- **Line Chart**: Jobs over time
- **Donut Chart**: Job categories distribution
- **Map**: Geographic distribution

### Page 2: AI Job Categories
- **Bar Chart**: Jobs by AI category
- **Treemap**: Skills for each category
- **Matrix**: Category × Experience level

### Page 3: Morocco Focus 🇲🇦
- **Filled Map**: Morocco regions
- **Bar Chart**: Jobs by Morocco region
- **Table**: Top Morocco companies
- **Slicer**: Morocco region filter

### Page 4: Skills Analysis
- **Bar Chart**: Top 20 skills
- **Word Cloud**: Skill frequency
- **Heatmap**: Skills × Job category

### Page 5: Company Analysis
- **Table**: Top hiring companies
- **Bar Chart**: Company × Job count
- **Scatter**: Company size vs job count

---

## 🔄 Data Refresh

To update the dashboard with new data:

1. Run the DBT pipeline:
   ```bash
   python run_pipeline.py
   ```

2. In Power BI Desktop:
   - Click **Refresh** button
   - Or go to **Home** → **Refresh**

3. For scheduled refresh (Power BI Service):
   - Publish to Power BI Service
   - Configure data gateway
   - Set up scheduled refresh

---

## 📊 Sample KPIs

Target KPIs for the dashboard:

| KPI | Description | Target |
|-----|-------------|--------|
| Total Jobs | Total job offers | 100K+ |
| Morocco % | Jobs in Morocco | Track |
| AI/ML % | AI/ML related jobs | 40%+ |
| Top Skills | Most demanded skill | Python |
| Avg Skills/Job | Skills per offer | 5-10 |

---

## 🛠️ Troubleshooting

### Data not loading?
- Ensure CSV files exist in `data/gold/`
- Run `python run_pipeline.py` to generate files
- Check file paths in Power BI queries

### Relationships not working?
- Verify column names match exactly
- Check for null values in key columns
- Ensure proper cardinality (Many:1)

### Morocco filter not working?
- Verify `is_morocco` column exists in `dim_location.csv`
- Check for boolean TRUE/FALSE values
- Refresh data model

---

## 📞 Support

For issues with the data pipeline, check:
- `dbt/logs/` for DBT logs
- `recommender/` for ML system docs

---

**RecruiterAI** - Data & AI Job Analytics Platform  
Focus: Morocco 🇲🇦  
Version: 2.0

Happy analyzing! 📊🚀
