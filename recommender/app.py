"""
RecruiterAI - Streamlit Application
Data & AI Job Analytics & Recommendation Platform - Focus Morocco
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from job_recommender import JobRecommender
from cv_parser import CVParser
from config import PROJECT_NAME, PROJECT_TAGLINE, UI_THEME, MOROCCO_CITIES

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title=f"{PROJECT_NAME} - Data & AI Jobs Morocco",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS - MODERN GLASSMORPHISM THEME
# ============================================================================
st.markdown(f"""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Global Styles */
    .stApp {{
        font-family: 'Inter', sans-serif;
    }}
    
    /* Main Header with Gradient */
    .main-header {{
        background: linear-gradient(135deg, {UI_THEME['primary_color']} 0%, {UI_THEME['secondary_color']} 50%, {UI_THEME['morocco_red']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }}
    
    .sub-header {{
        font-size: 1.25rem;
        color: {UI_THEME['text_secondary']};
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }}
    
    /* Morocco Badge */
    .morocco-badge {{
        background: linear-gradient(90deg, {UI_THEME['morocco_red']}, {UI_THEME['morocco_green']});
        color: white;
        padding: 0.4rem 1.2rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(193, 39, 45, 0.3);
    }}
    
    /* Job Card with Glassmorphism */
    .job-card {{
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 20px;
        padding: 1.8rem;
        margin: 1.2rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    
    .job-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, {UI_THEME['primary_color']}, {UI_THEME['secondary_color']});
    }}
    
    .job-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 25px 50px rgba(99, 102, 241, 0.25);
        border-color: {UI_THEME['primary_color']};
    }}
    
    .job-card h3 {{
        color: {UI_THEME['text_primary']};
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }}
    
    .job-card p {{
        color: {UI_THEME['text_secondary']};
        margin: 0.3rem 0;
    }}
    
    /* Score Badge */
    .score-badge {{
        background: linear-gradient(135deg, {UI_THEME['primary_color']}, {UI_THEME['secondary_color']});
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 1rem;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
    }}
    
    /* Morocco Priority Badge */
    .morocco-priority {{
        background: linear-gradient(90deg, {UI_THEME['morocco_red']}, {UI_THEME['morocco_green']});
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: 600;
        font-size: 0.75rem;
        margin-left: 0.5rem;
    }}
    
    /* Skill Tags */
    .skill-tag {{
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2));
        color: {UI_THEME['primary_color']};
        padding: 0.35rem 0.8rem;
        border-radius: 12px;
        margin: 0.2rem;
        display: inline-block;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid rgba(99, 102, 241, 0.3);
        transition: all 0.2s ease;
    }}
    
    .skill-tag:hover {{
        background: {UI_THEME['primary_color']};
        color: white;
        transform: scale(1.05);
    }}
    
    /* AI Skill Tag (Special) */
    .ai-skill-tag {{
        background: linear-gradient(135deg, {UI_THEME['primary_color']}, {UI_THEME['secondary_color']});
        color: white;
        padding: 0.35rem 0.8rem;
        border-radius: 12px;
        margin: 0.2rem;
        display: inline-block;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: 0 2px 10px rgba(99, 102, 241, 0.3);
    }}
    
    /* Metrics Cards */
    .metric-card {{
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.1) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
    }}
    
    .metric-value {{
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, {UI_THEME['primary_color']}, {UI_THEME['secondary_color']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    .metric-label {{
        color: {UI_THEME['text_secondary']};
        font-size: 0.9rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }}
    
    /* Sidebar Styling */
    .css-1d391kg {{
        background: linear-gradient(180deg, {UI_THEME['background_dark']} 0%, {UI_THEME['background_light']} 100%);
    }}
    
    /* Button Styling */
    .stButton > button {{
        background: linear-gradient(135deg, {UI_THEME['primary_color']}, {UI_THEME['secondary_color']});
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5);
    }}
    
    /* Link Styling */
    a {{
        color: {UI_THEME['primary_color']};
        text-decoration: none;
        font-weight: 500;
        transition: color 0.2s ease;
    }}
    
    a:hover {{
        color: {UI_THEME['secondary_color']};
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        padding: 2rem;
        color: {UI_THEME['text_secondary']};
        border-top: 1px solid rgba(99, 102, 241, 0.2);
        margin-top: 3rem;
    }}
    
    .footer-brand {{
        font-size: 1.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, {UI_THEME['primary_color']}, {UI_THEME['secondary_color']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@st.cache_resource
def load_recommender():
    """Load the recommender (cached)"""
    with st.spinner("🤖 Initializing RecruiterAI..."):
        return JobRecommender()

def is_morocco_location(location: str) -> bool:
    """Check if location is in Morocco"""
    if not location:
        return False
    location_lower = location.lower()
    return any(city in location_lower for city in MOROCCO_CITIES)

def get_ai_skills():
    """Return list of AI-related skills for special highlighting"""
    return ['LLM', 'GPT', 'Machine Learning', 'Deep Learning', 'NLP', 'AI', 
            'Artificial Intelligence', 'Neural Networks', 'TensorFlow', 'PyTorch',
            'Computer Vision', 'Generative AI', 'LangChain', 'Transformers', 
            'BERT', 'MLOps', 'RAG', 'Hugging Face']

def display_job_card(job: dict, rank: int):
    """Display a job card with modern styling"""
    is_morocco = is_morocco_location(job.get('location', ''))
    ai_skills = get_ai_skills()
    
    morocco_badge = '<span class="morocco-priority">🇲🇦 Morocco</span>' if is_morocco else ''
    
    # Build skill tags with special styling for AI skills
    skill_tags = ''
    for skill in job.get('skills', [])[:10]:
        if skill in ai_skills:
            skill_tags += f'<span class="ai-skill-tag">🤖 {skill}</span>'
        else:
            skill_tags += f'<span class="skill-tag">{skill}</span>'
    
    st.markdown(f"""
    <div class="job-card">
        <h3>#{rank} {job['title']}</h3>
        <p><strong>🏢 {job['company']}</strong> | 📍 {job['location']} {morocco_badge} | 📋 {job['contract_type']}</p>
        <p>
            <span class="score-badge">⭐ Score: {job['score']:.1%}</span>
            <span style="margin-left: 1rem; color: #94A3B8;">
                ✓ {job['skills_match_count']} skills matched ({job['skills_match_ratio']:.0%})
            </span>
        </p>
        <p style="margin-top: 1rem;"><strong>Required Skills:</strong></p>
        <p>{skill_tags}</p>
        <details style="margin-top: 1rem;">
            <summary style="cursor: pointer; color: #6366F1; font-weight: 600;">📄 View Description</summary>
            <p style="margin-top: 1rem; padding: 1rem; background: rgba(99,102,241,0.1); border-radius: 10px;">
                {job.get('description_preview', 'No description available.')}
            </p>
        </details>
        <p style="margin-top: 1rem;">
            <a href="{job.get('job_url', '#')}" target="_blank" style="
                background: linear-gradient(135deg, #6366F1, #8B5CF6);
                color: white;
                padding: 0.5rem 1.5rem;
                border-radius: 10px;
                text-decoration: none;
                font-weight: 600;
            ">🔗 View Full Offer</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN HEADER
# ============================================================================
st.markdown('<div class="main-header">🤖 RecruiterAI</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">{PROJECT_TAGLINE}</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center;"><span class="morocco-badge">🇲🇦 Focus Morocco</span></div>', unsafe_allow_html=True)

# ============================================================================
# LOAD RECOMMENDER
# ============================================================================
try:
    recommender = load_recommender()
    st.success(f"✅ System loaded: **{len(recommender.jobs_df):,}** job offers available")
except Exception as e:
    st.error(f"❌ Error loading system: {e}")
    st.stop()

# ============================================================================
# SIDEBAR - SEARCH OPTIONS
# ============================================================================
st.sidebar.markdown(f"""
<div style="text-align: center; padding: 1rem;">
    <div style="font-size: 1.5rem; font-weight: 700; color: #6366F1;">🤖 RecruiterAI</div>
    <div style="font-size: 0.85rem; color: #94A3B8;">Find Your Dream AI Job</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.header("🔍 Search Settings")

# Search Mode
search_mode = st.sidebar.radio(
    "Input Method",
    ["✍️ Manual Input", "📄 Upload CV"],
    help="Choose how to provide your profile"
)

# Variables for inputs
profile_text = ""
keywords_list = []
cv_uploaded = False

if search_mode == "✍️ Manual Input":
    st.sidebar.subheader("👤 Your Profile")
    
    profile_text = st.sidebar.text_area(
        "Describe your profile",
        height=150,
        placeholder="Ex: AI Engineer with 3 years of experience in NLP, LLMs, and Python. Looking for opportunities in Morocco..."
    )
    
    keywords_input = st.sidebar.text_input(
        "Skills (comma-separated)",
        placeholder="Python, LLM, LangChain, NLP, TensorFlow..."
    )
    
    if keywords_input:
        keywords_list = [k.strip() for k in keywords_input.split(',') if k.strip()]

else:  # Upload CV
    st.sidebar.subheader("📄 Upload Your CV")
    
    uploaded_file = st.sidebar.file_uploader(
        "Choose a file",
        type=['pdf', 'docx', 'txt'],
        help="Supported formats: PDF, DOCX, TXT"
    )
    
    if uploaded_file:
        cv_uploaded = True
        
        keywords_input = st.sidebar.text_input(
            "Additional skills (optional)",
            placeholder="LLM, Generative AI, Morocco..."
        )
        
        if keywords_input:
            keywords_list = [k.strip() for k in keywords_input.split(',') if k.strip()]

# Filters
st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Filters")

# Location with Morocco options
location_options = [
    "Any Location",
    "🇲🇦 Morocco (Any City)",
    "🇲🇦 Casablanca",
    "🇲🇦 Rabat",
    "🇲🇦 Marrakech",
    "🇲🇦 Tanger",
    "🇲🇦 Fes",
    "🇲🇦 Agadir",
    "Remote",
    "Other (Type Below)"
]

location_select = st.sidebar.selectbox("📍 Location Preference", location_options)

if location_select == "Other (Type Below)":
    location_pref = st.sidebar.text_input("Enter location", placeholder="Ex: Paris, London...")
elif location_select == "Any Location":
    location_pref = None
else:
    location_pref = location_select.replace("🇲🇦 ", "").replace(" (Any City)", "")

contract_type_pref = st.sidebar.selectbox(
    "📋 Contract Type",
    ["All Types", "Full-time", "Part-time", "Contract", "Internship", "Freelance"]
)

experience_level = st.sidebar.selectbox(
    "💼 Experience Level",
    ["Any Level", "Junior", "Mid-Level", "Senior", "Manager/Lead"]
)

top_k = st.sidebar.slider(
    "📊 Number of Results",
    min_value=5,
    max_value=50,
    value=10,
    step=5
)

min_score = st.sidebar.slider(
    "⭐ Minimum Score",
    min_value=0.0,
    max_value=1.0,
    value=0.0,
    step=0.05,
    format="%.0f%%"
)

# Search Button
st.sidebar.markdown("---")
search_button = st.sidebar.button("🚀 Find Jobs", type="primary", use_container_width=True)

# ============================================================================
# MAIN CONTENT
# ============================================================================
if search_button:
    # Validate inputs
    if search_mode == "✍️ Manual Input" and not profile_text and not keywords_list:
        st.warning("⚠️ Please enter a profile description or skills")
        st.stop()
    
    if search_mode == "📄 Upload CV" and not cv_uploaded:
        st.warning("⚠️ Please upload a CV")
        st.stop()
    
    # Run search
    with st.spinner("🔍 Searching for the best matches..."):
        try:
            # Prepare parameters
            contract_type = None if contract_type_pref == "All Types" else contract_type_pref
            exp_level = None if experience_level == "Any Level" else experience_level.lower().replace("-level", "").replace("/lead", "")
            
            if search_mode == "✍️ Manual Input":
                recommendations = recommender.recommend(
                    candidate_profile=profile_text,
                    keywords=keywords_list if keywords_list else None,
                    location_preference=location_pref,
                    contract_type_preference=contract_type,
                    experience_level=exp_level,
                    top_k=top_k,
                    min_score=min_score
                )
            else:
                cv_bytes = uploaded_file.read()
                recommendations = recommender.recommend_from_cv_bytes(
                    cv_bytes=cv_bytes,
                    cv_filename=uploaded_file.name,
                    additional_keywords=keywords_list if keywords_list else None,
                    location_preference=location_pref,
                    contract_type_preference=contract_type,
                    experience_level=exp_level,
                    top_k=top_k,
                    min_score=min_score
                )
            
            # Display results
            if recommendations:
                # Count Morocco jobs
                morocco_count = sum(1 for r in recommendations if is_morocco_location(r.get('location', '')))
                
                st.success(f"🎉 Found **{len(recommendations)}** matching jobs! ({morocco_count} in Morocco 🇲🇦)")
                
                # Tabs for different views
                tab1, tab2, tab3 = st.tabs(["📋 Job Cards", "📊 Table View", "📈 Analytics"])
                
                with tab1:
                    for i, job in enumerate(recommendations, 1):
                        display_job_card(job, i)
                
                with tab2:
                    df_results = pd.DataFrame([{
                        'Rank': i,
                        'Title': job['title'],
                        'Company': job['company'],
                        'Location': job['location'],
                        'Morocco': '🇲🇦' if is_morocco_location(job.get('location', '')) else '',
                        'Contract': job['contract_type'],
                        'Score': f"{job['score']:.1%}",
                        'Skills Matched': job['skills_match_count'],
                        'URL': job.get('job_url', '')
                    } for i, job in enumerate(recommendations, 1)])
                    
                    st.dataframe(
                        df_results,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "URL": st.column_config.LinkColumn("Link", display_text="View")
                        }
                    )
                    
                    # Download button
                    csv = df_results.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Results (CSV)",
                        data=csv,
                        file_name="recruiter_ai_results.csv",
                        mime="text/csv"
                    )
                
                with tab3:
                    st.subheader("📊 Results Analytics")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        avg_score = sum(r['score'] for r in recommendations) / len(recommendations)
                        st.metric("Avg Score", f"{avg_score:.1%}")
                    
                    with col2:
                        avg_skills = sum(r['skills_match_count'] for r in recommendations) / len(recommendations)
                        st.metric("Avg Skills Match", f"{avg_skills:.1f}")
                    
                    with col3:
                        st.metric("Morocco Jobs", f"{morocco_count} 🇲🇦")
                    
                    with col4:
                        unique_companies = len(set(r['company'] for r in recommendations))
                        st.metric("Companies", unique_companies)
                    
                    # Location distribution
                    st.subheader("📍 Location Distribution")
                    location_counts = pd.Series([r['location'] for r in recommendations]).value_counts()
                    st.bar_chart(location_counts)
                    
                    # Top skills
                    st.subheader("🔧 Most Demanded Skills")
                    all_skills = []
                    for r in recommendations:
                        all_skills.extend(r.get('skills', []))
                    
                    if all_skills:
                        from collections import Counter
                        skill_counts = Counter(all_skills)
                        top_skills_df = pd.DataFrame(
                            skill_counts.most_common(15),
                            columns=['Skill', 'Count']
                        )
                        st.bar_chart(top_skills_df.set_index('Skill'))
            
            else:
                st.warning("😕 No jobs found matching your criteria. Try broadening your search.")
        
        except Exception as e:
            st.error(f"❌ Search error: {e}")
            import traceback
            st.code(traceback.format_exc())

else:
    # Initial display (no search yet)
    st.info("👈 Configure your profile in the sidebar and click **Find Jobs** to start!")
    
    # Display global statistics
    st.markdown("---")
    st.subheader("📊 Platform Statistics")
    
    stats = recommender.get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats['total_jobs']:,}</div>
            <div class="metric-label">Total Jobs</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats['unique_companies']:,}</div>
            <div class="metric-label">Companies</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats['unique_locations']:,}</div>
            <div class="metric-label">Locations</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats['avg_skills_per_job']:.1f}</div>
            <div class="metric-label">Avg Skills/Job</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Top skills
    st.markdown("---")
    st.subheader("🔥 Top 10 In-Demand Skills")
    
    top_skills = stats.get('top_10_skills', [])
    if top_skills:
        skills_df = pd.DataFrame(top_skills, columns=['Skill', 'Job Count'])
        st.bar_chart(skills_df.set_index('Skill'))
    
    # Experience distribution
    st.subheader("💼 Experience Level Distribution")
    exp_dist = stats.get('experience_level_distribution', {})
    if exp_dist:
        exp_df = pd.DataFrame(list(exp_dist.items()), columns=['Level', 'Count'])
        st.bar_chart(exp_df.set_index('Level'))

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown(f"""
<div class="footer">
    <div class="footer-brand">🤖 RecruiterAI</div>
    <p>{PROJECT_TAGLINE}</p>
    <p style="font-size: 0.85rem;">Powered by Sentence-BERT, FAISS, and Streamlit | 🇲🇦 Focus Morocco</p>
</div>
""", unsafe_allow_html=True)
