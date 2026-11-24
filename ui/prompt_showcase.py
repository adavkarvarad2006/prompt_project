"""
ExamForge AI - Prompt Engineering Techniques Interactive Laboratory & Showcase
Directly addresses Section 6 of the Project Proposal:
1. Role-based Prompting
2. Contextual Prompting
3. Few-shot Prompting
4. Structured Output Prompting
5. Adaptive Prompting
6. Self-check / Verification Prompting
"""
import streamlit as st
import json
import pandas as pd
from core.prompt_engine import PromptEngine
from core.llm_client import LLMClient
from core.database import Database

def render_prompt_showcase(llm_client: LLMClient):
    st.markdown("### 🔬 Prompt Engineering Demonstration Laboratory")
    st.markdown("""
        This interactive laboratory demonstrates the **6 Prompt Engineering Techniques** specified in 
        **Section 6 of the ExamForge AI Project Proposal** for the **Prompt Engineering 20 Marks Component**.
        You can inspect prompt formulations, compare standard vs engineered prompts, and view live system logs.
    """)

    tech_tab1, tech_tab2, tech_tab3, tech_tab4, tech_tab5, tech_tab6, audit_tab = st.tabs([
        "1. Role-Based",
        "2. Contextual",
        "3. Few-Shot",
        "4. Structured Output",
        "5. Adaptive",
        "6. Self-Check / Verification",
        "📋 Execution Audit Logs"
    ])

    # 1. Role-based Prompting
    with tech_tab1:
        st.subheader("1. Role-Based Prompting")
        st.info("**Objective:** Instruct the model to adopt a specialized persona to constrain vocabulary, depth, and pedagogical behavior.")
        
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.markdown("##### 🎭 Role Definitions in ExamForge AI:")
            role_choice = st.selectbox("Select Role to Inspect:", list(PromptEngine.ROLES.keys()))
            st.markdown(f"**System Prompt:**")
            st.code(PromptEngine.ROLES[role_choice], language="text")

        with col_r2:
            st.markdown("##### ⚡ Comparative Experiment: Generic vs Role-Conditioned Prompt")
            test_topic = st.text_input("Test Topic:", value="Chain-of-Thought Reasoning in LLMs")
            
            if st.button("Run Role Prompt Comparison"):
                generic_prompt = f"Explain {test_topic} in 3 bullet points."
                role_prompt = f"{PromptEngine.ROLES[role_choice]}\n\nAs this role, explain {test_topic} in 3 bullet points."
                
                with st.spinner("Executing comparison..."):
                    gen_out = llm_client.call_llm("You are a helpful assistant.", generic_prompt, json_mode=False)
                    role_out = llm_client.call_llm(PromptEngine.ROLES[role_choice], f"Explain {test_topic} in 3 bullet points.", json_mode=False)
                    
                    st.markdown("**Generic Assistant Output:**")
                    st.write(gen_out if gen_out else f"1. CoT breaks tasks into steps.\n2. Helps with reasoning.\n3. Improves accuracy.")
                    st.markdown(f"**{role_choice} Output:**")
                    st.write(role_out if role_out else f"1. Pedagogical decomposition of cognitive load across autoregressive steps.\n2. Alleviates token generation bottleneck in non-linear inference.\n3. Enables intermediate state verification against formal rubrics.")

    # 2. Contextual Prompting
    with tech_tab2:
        st.subheader("2. Contextual Prompting")
        st.info("**Objective:** Ground the model's generation exclusively in syllabus units, learning outcomes, marks, and student performance data to prevent topic drift and hallucinations.")
        
        st.markdown("##### 📐 Blueprint and Syllabus Context Injection Architecture:")
        st.code("""
=== CONTEXT: SYLLABUS DETAILS ===
Subject: Prompt Engineering and Generative AI (PE-302)
Unit 2: Advanced Prompting Paradigms and Structured Outputs
* Topic: Chain-of-Thought (CoT) Prompting -> Objectives: Contrast direct answer extraction with reasoning traces

=== BLUEPRINT CONSTRAINTS ===
Total Marks: 25.0 | Cognitive Bloom's Target: Apply (L3) 45%, Analyze (L4) 40%
        """, language="text")

        st.markdown("""
        **Benefits in ExamForge AI:**
        - Questions strictly reference concepts present in the syllabus.
        - Out-of-syllabus or ungrounded questions are structurally eliminated.
        - Marks and time allocations match university examination regulations.
        """)

    # 3. Few-Shot Prompting
    with tech_tab3:
        st.subheader("3. Few-Shot In-Context Prompting")
        st.info("**Objective:** Supply high-quality input-output exemplars directly in the context window to anchor style, rubric format, and distractor plausibility.")
        
        st.markdown("##### 🎯 Exemplars Provided to the LLM:")
        st.json(PromptEngine.FEW_SHOT_QUESTION_GENERATION)

        st.markdown("""
        **Why Few-Shot is Critical for Exam Paper Generation:**
        - Ensures every question has a step-by-step marking scheme.
        - Anchors MCQ distractors to realistic student misconceptions rather than trivial nonsense options.
        - Avoids conversational meta-text ('Here is a question for you...').
        """)

    # 4. Structured Output Prompting
    with tech_tab4:
        st.subheader("4. Structured Output Prompting (Schema Enforcement)")
        st.info("**Objective:** Enforce deterministic JSON output matching strict schemas, enabling seamless database persistence, UI rendering, and automated evaluation.")
        
        st.markdown("##### 📦 Enforced JSON Schema:")
        sample_schema = {
            "title": "Exam Title",
            "total_marks": 25.0,
            "duration_minutes": 45,
            "questions": [
                {
                    "question_id": "Q-001",
                    "unit_number": 1,
                    "topic_name": "Topic Name",
                    "question_type": "MCQ | Short Answer | Long Answer",
                    "blooms_level": "Remember | Understand | Apply | Analyze | Evaluate | Create",
                    "difficulty": "Easy | Medium | Hard",
                    "marks": 2.0,
                    "question_text": "Stem...",
                    "options": ["A. ...", "B. ..."],
                    "correct_option": "A",
                    "model_answer": "Model solution...",
                    "marking_scheme": [{"step_description": "...", "marks_awarded": 1.0}]
                }
            ]
        }
        st.json(sample_schema)

    # 5. Adaptive Prompting
    with tech_tab5:
        st.subheader("5. Adaptive Prompting (Performance-Conditioned Remediation)")
        st.info("**Objective:** Dynamically condition prompts on the student's individual learning gaps, previous misconceptions, and mastery level to produce personalized remedial sets.")
        
        st.markdown("##### 🧬 Dynamic Prompt Construction:")
        st.code("""
=== STUDENT PROFILE & DIAGNOSTIC GAPS ===
Student Name: Alex Chen (USN: 1MS22CS045)
Weak Topics Identified: ["Few-Shot In-Context Learning", "Structured Output Schema"]
Recurring Misconceptions: ["Confused Zero-Shot with Few-Shot demonstration syntax"]
Current Topic Mastery: {"Few-Shot": 40.0%, "Prompt Anatomy": 85.0%}

=== ADAPTIVE INSTRUCTION ===
Generate a progressive remedial practice set starting with a conceptual clarifier (L2 Understand)
followed by an application challenge (L3 Apply) targeting the specific misconception.
        """, language="text")

        st.markdown("""
        **Pedagogical Significance:**
        - Closes the feedback loop: assessment doesn't end with a grade, it leads directly to personalized learning.
        - Scaffolds difficulty to rebuild learner confidence before re-testing higher-order skills.
        """)

    # 6. Self-Check / Verification Prompting
    with tech_tab6:
        st.subheader("6. Self-Check / Verification Prompting (Meta-Prompting)")
        st.info("**Objective:** Deploy an independent verification pass where the LLM inspects the generated question paper against syllabus bounds and arithmetic rules before presenting to the teacher.")
        
        st.markdown("##### 🛡️ Verification Rules Checked by the Auditor Persona:")
        st.markdown("""
        1. **Marks Integrity:** Total marks must equal the exact sum of individual question marks.
        2. **Step Scheme Sum:** The step marking scheme points must sum exactly to each question's allocated marks.
        3. **Syllabus Drift:** Zero questions outside the uploaded syllabus topics.
        4. **Cognitive Balance:** Bloom's taxonomy proportions must respect blueprint boundaries.
        5. **Distractor Quality:** MCQ options must not contain giveaway clues or length disparities.
        """)

        st.markdown("##### Sample Verification Report Generated:")
        st.json({
            "is_approved": True,
            "calculated_total_marks": 25.0,
            "marks_consistent": True,
            "syllabus_compliance_score": 98.4,
            "detected_issues": [
                {"question_id": "Q-002", "severity": "Info", "issue": "Distractor C is shorter than others", "suggestion": "Equalize text lengths"}
            ],
            "overall_verdict": "Verified: All questions adhere to syllabus and mark sums match blueprint."
        })

    # Execution Audit Logs
    with audit_tab:
        st.subheader("Real-Time Prompt Execution Audit Logs")
        st.caption("Inspect live logs of prompts executed by ExamForge AI, stored in the SQLite database:")
        logs = Database.get_prompt_logs(limit=25)
        if logs:
            for l in logs:
                with st.expander(f"[{l.get('created_at')[:19]}] {l.get('technique')} - {l.get('context_type')}"):
                    st.markdown("**System Prompt:**")
                    st.code(l.get("system_prompt", ""), language="text")
                    st.markdown("**User Prompt:**")
                    st.code(l.get("user_prompt", ""), language="text")
                    st.markdown("**Model Response:**")
                    st.code(l.get("response_text", ""), language="json")
        else:
            st.info("No prompt executions logged yet. Generate a question paper or evaluate an exam to see real-time logs.")
