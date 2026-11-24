"""
ExamForge AI - Project Documentation and Submission Details
Presents the full proposal details matching the 20 Marks Component submission.
"""
import streamlit as st

def render_documentation():
    st.markdown("### 📄 Project Proposal & Academic Submission Details")
    st.markdown("""
        **Project Title:** ExamForge AI: A Dual-Adaptive Intelligent Examination and Personalized Learning Platform Using Prompt Engineering  
        **Course:** Prompt Engineering (20 Marks Component)  
        **Domain:** Education-Based Applications  
    """)

    st.divider()

    with st.expander("📌 1. Introduction & Executive Summary", expanded=True):
        st.markdown("""
        Education increasingly uses digital platforms for teaching, assessment, and performance tracking. 
        However, preparing balanced question papers and providing individual attention to every learner can require 
        significant time and effort from teachers. At the same time, students often receive the same practice material 
        even when their knowledge levels and learning needs differ.

        **ExamForge AI** is a dual-adaptive AI-powered examination and personalized learning platform designed for both 
        teachers and students. Teachers can provide a syllabus, specify assessment requirements, and generate editable 
        question papers with answer keys and marking schemes. Students can take AI-generated practice tests, receive feedback, 
        and get further practice based on their demonstrated strengths and weaknesses. The platform uses **Prompt Engineering** 
        to guide question generation, evaluation, and adaptive recommendations in a structured and context-aware manner.
        """)

    with st.expander("🎯 2. Objectives & Problem Statement", expanded=False):
        st.markdown("""
        #### Problem Statement:
        Teachers commonly spend considerable time converting syllabus content into question papers with appropriate 
        unit coverage, marks distribution, and difficulty levels. Creating answer keys and marking schemes adds to this workload. 
        On the student side, conventional assessments often provide a score but do not consistently identify topic-level 
        learning gaps or adapt subsequent practice to the student's needs.

        #### Key Objectives:
        1. Unified platform with role-based facilities for teachers and students.
        2. Syllabus ingestion and unit/topic/objective extraction.
        3. Syllabus-aligned question paper, answer key, and step-marking scheme generation.
        4. Interactive student assessments with rubric-based step evaluation.
        5. Topic-wise strength, weakness, and recurring misconception analysis.
        6. Performance-driven dual-adaptive practice loops.
        7. Human-in-the-loop review, editing, and teacher approval safeguards.
        """)

    with st.expander("💡 3. Novelty: The Dual-Adaptive Intelligence Engine", expanded=False):
        st.markdown("""
        The core novelty of ExamForge AI is its **Dual-Adaptive Intelligence Engine**, which synchronizes two interconnected workflows:
        
        1. **Teacher-Side Assessment Adaptation:**  
           Constraints (syllabus units, total marks, question formats, Bloom's cognitive taxonomy, and difficulty distribution) 
           condition structured prompts to generate drafts, answer keys, and marking schemes with an automated Self-Check verification audit.
        
        2. **Student-Side Learning Adaptation ("Forge My Path"):**  
           Post-assessment diagnostic analysis detects topic-level gaps and recurring misconceptions. Subsequent practice sets 
           dynamically adjust topic concentration and difficulty with progressive scaffolding.
        
        3. **Shared Learning Analytics:**  
           Bridges student outcomes with teacher insights, revealing cohort-level misconception patterns and topic mastery heatmaps.
        
        4. **Human-in-the-Loop Safeguards:**  
           Generated questions and evaluations remain drafts subject to teacher review and manual refinement.
        """)

    with st.expander("🔬 4. Prompt Engineering Techniques Applied (Section 6)", expanded=True):
        st.markdown("""
        | Technique | Implementation in ExamForge AI |
        |---|---|
        | **1. Role-Based Prompting** | Configurable personas: Senior Academic Examiner, Step-Marking Evaluator, Socratic Diagnostic Tutor, and Independent Quality Assurance Verifier. |
        | **2. Contextual Prompting** | Injects syllabus units, learning outcomes, marks, and student history directly into prompt templates to prevent hallucination. |
        | **3. Few-Shot Prompting** | High-quality exemplars demonstrating step-marking breakdowns and plausible MCQ distractors. |
        | **4. Structured Output Prompting** | Strict JSON schema enforcement ensuring deterministic parsing into database models and UI components. |
        | **5. Adaptive Prompting** | Dynamically synthesizes the student's diagnostic error profile into the prompt to generate personalized remedial sets. |
        | **6. Self-Check / Verification Prompting** | Meta-prompting pass that audits marks summation, syllabus compliance, and question ambiguity before teacher review. |
        """)
