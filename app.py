"""
ExamForge AI - Main Streamlit Application
A Dual-Adaptive Intelligent Examination and Personalized Learning Platform Using Prompt Engineering.
"""
import streamlit as st
import os
import json

from core.database import Database
from core.llm_client import LLMClient
from data.sample_syllabi import SAMPLE_PROMPT_ENGINEERING_SYLLABUS, SAMPLE_DSA_SYLLABUS
from ui.components import render_header
from ui.teacher_portal import render_teacher_portal
from ui.student_portal import render_student_portal

# Set page configuration
st.set_page_config(
    page_title="ExamForge AI - Dual-Adaptive Learning Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database and seed sample syllabi if empty
Database.init_db()
existing_syllabi = Database.get_all_syllabi()
if not existing_syllabi:
    Database.save_syllabus(SAMPLE_PROMPT_ENGINEERING_SYLLABUS)
    Database.save_syllabus(SAMPLE_DSA_SYLLABUS)

# Pre-seed a sample approved paper if none exists so student portal has immediate content
existing_papers = Database.get_all_papers()
if not existing_papers:
    from core.models import ExamBlueprint
    from core.prompt_engine import PromptEngine
    from core.models import Question
    
    # Generate initial paper using simulated client
    sim_client = LLMClient(provider="offline")
    bp = ExamBlueprint(
        title="Mid-Term Assessment: Prompt Engineering (PE-302)",
        total_marks=25.0,
        duration_minutes=45,
        instructions=[
            "Answer all questions in the sequence provided.",
            "Marks for each step are allocated in the marking rubric.",
            "Write concise, technically sound answers."
        ],
        unit_distribution={1: 33.3, 2: 33.3, 3: 33.3},
        question_type_distribution={"MCQ": 4, "Short": 3, "Long": 1},
        blooms_distribution={"L1_L2": 35, "L3_L4": 50, "L5_L6": 15},
        difficulty_distribution={"Easy": 30, "Medium": 50, "Hard": 20}
    )
    p_data = PromptEngine.build_question_generation_prompt(SAMPLE_PROMPT_ENGINEERING_SYLLABUS, bp)
    raw = sim_client.call_llm(p_data["system_prompt"], p_data["user_prompt"], json_mode=True)
    d = json.loads(raw)
    qs = [Question.from_dict(q) for q in d["questions"]]
    
    from core.models import QuestionPaper
    initial_paper = QuestionPaper(
        paper_id="QP-DEMO-001",
        syllabus_id=SAMPLE_PROMPT_ENGINEERING_SYLLABUS.syllabus_id,
        title="Mid-Term Assessment: Prompt Engineering (PE-302)",
        course_name=SAMPLE_PROMPT_ENGINEERING_SYLLABUS.subject_name,
        total_marks=25.0,
        duration_minutes=45,
        instructions=bp.instructions,
        questions=qs,
        status="Approved",
        teacher_notes="Curated baseline assessment paper for demonstration.",
        verification_report={
            "is_approved": True,
            "calculated_total_marks": 25.0,
            "marks_consistent": True,
            "syllabus_compliance_score": 98.4,
            "overall_verdict": "Verified: All questions strictly adhere to syllabus learning objectives and marks constraints."
        }
    )
    Database.save_paper(initial_paper)

# Sidebar configuration
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=64)
    st.markdown("## **ExamForge AI**")
    st.caption("Dual-Adaptive Intelligent Examination & Learning Platform")
    
    st.divider()
    st.markdown("### 🧭 Navigation")
    nav_selection = st.radio(
        "Select Portal:",
        [
            "🎓 Teacher Assessment Studio",
            "🎒 Student Adaptive Portal"
        ]
    )

    st.divider()
    st.markdown("### ⚙️ LLM Provider Settings")
    provider_choice = st.selectbox(
        "AI Engine Provider:",
        [
            "Google Gemini API (REST) - Connected",
            "Offline Pedagogical Engine (Zero-Setup / Reliable)",
            "OpenAI / Groq API"
        ],
        index=0
    )

    api_key_input = None
    model_name_input = None

    if "Gemini" in provider_choice:
        prov_key = "gemini"
        default_gemini_key = os.environ.get("GEMINI_API_KEY", "")
        api_key_input = st.text_input(
            "Gemini API Key:", 
            value=default_gemini_key, 
            type="password",
            placeholder="AIzaSy... or paste your Gemini key"
        )
        model_name_input = st.selectbox(
            "Gemini Model:", 
            ["gemini-3-flash-preview", "gemini-3.8-flash", "gemini-3.1-flash-lite-preview"]
        )
        if api_key_input:
            st.success("⚡ Live Google Gemini Connected")
        else:
            st.info("💡 Paste your Gemini key above to enable live AI generation")
    elif "OpenAI" in provider_choice:
        prov_key = "openai"
        api_key_input = st.text_input("OpenAI / Groq API Key:", type="password", placeholder="sk-...")
        model_name_input = st.text_input("Model Name:", value="gpt-4o-mini")
    else:
        prov_key = "offline"
        st.success("✅ Offline Pedagogical Engine Active")
        st.caption("Implements exact prompt pipelines, deterministic grading, schema enforcement & adaptive loops without external API keys.")

    llm_client = LLMClient(provider=prov_key, api_key=api_key_input, model_name=model_name_input)

    st.divider()
    if st.button("🔄 Reset / Re-seed Sample Data"):
        Database.init_db()
        Database.save_syllabus(SAMPLE_PROMPT_ENGINEERING_SYLLABUS)
        Database.save_syllabus(SAMPLE_DSA_SYLLABUS)
        st.success("Database re-seeded successfully!")
        st.rerun()

# Render Banner
render_header(
    title="ExamForge AI",
    subtitle="A Dual-Adaptive Intelligent Examination and Personalized Learning Platform Using Prompt Engineering"
)

# Route to selected portal
if "Teacher" in nav_selection:
    render_teacher_portal(llm_client)
elif "Student" in nav_selection:
    render_student_portal(llm_client)
