"""
ExamForge AI - Student Portal Workflow
Covers:
1. Student Profile & Available Assessment Hub
2. Interactive Test-Taking Environment with Timer & Progress
3. AI-Assisted Evaluation, Step-Marking & Misconception Diagnosis
4. Dual-Adaptive Practice Engine ("Forge My Path" Personalized Remediation)
5. Personal Learning Dashboard & Topic Mastery Growth
"""
import streamlit as st
import pandas as pd
import json
import uuid
from typing import Dict, Any, List
from core.models import (
    QuestionPaper, Question, StudentAnswer, QuestionType
)
from core.database import Database
from core.evaluator import AssessmentEvaluator
from core.adaptive_engine import AdaptiveEngine
from core.llm_client import LLMClient
from ui.components import render_stat_row

def render_student_portal(llm_client: LLMClient):
    st.markdown("### 🎒 Student Adaptive Learning Portal")
    st.write("Take syllabus-aligned examinations, receive instant step-wise feedback, and generate personalized remedial practice sets.")

    # Student Identification in sidebar or top bar
    col_id1, col_id2 = st.columns([1, 1])
    with col_id1:
        student_name = st.text_input("Student Name", value="Alex Chen", key="stud_name_input")
    with col_id2:
        student_id = st.text_input("USN / Roll Number", value="1MS22CS045", key="stud_id_input")

    tab1, tab2, tab3 = st.tabs([
        "📝 1. Assessment Center", 
        "🎯 2. Adaptive Remedial Practice ('Forge My Path')", 
        "📈 3. My Topic Mastery & Learning Dashboard"
    ])

    # ---------------- TAB 1: ASSESSMENT CENTER ----------------
    with tab1:
        st.subheader("Available Examinations & Practice Tests")
        papers = Database.get_all_papers(status="Approved")
        
        # Also allow draft papers if no approved paper exists for testing ease
        if not papers:
            all_p = Database.get_all_papers()
            if all_p:
                st.info("No approved papers found yet. Displaying draft papers for demonstration:")
                papers = all_p
            else:
                st.warning("No question papers currently available. Teachers can generate one in the Teacher Portal.")
                return

        paper_options = {p.paper_id: f"{p.title} ({p.total_marks} Marks | {p.duration_minutes} Mins)" for p in papers}
        active_exam_id = st.selectbox(
            "Select an Assessment to Attempt:",
            options=list(paper_options.keys()),
            format_func=lambda x: paper_options[x]
        )

        selected_paper = Database.get_paper(active_exam_id)
        if not selected_paper:
            return

        with st.expander(f"📋 Assessment Details & Instructions ({selected_paper.title})", expanded=True):
            st.write(f"**Course:** {selected_paper.course_name} | **Total Marks:** {selected_paper.total_marks} | **Duration:** {selected_paper.duration_minutes} Minutes")
            st.markdown("**Instructions:**")
            for ins in selected_paper.instructions:
                st.markdown(f"- {ins}")

        st.divider()
        st.markdown(f"#### ✍️ Examination in Progress: {selected_paper.title}")
        
        # Test taking form
        with st.form("exam_attempt_form"):
            user_answers: Dict[str, StudentAnswer] = {}
            
            for idx, q in enumerate(selected_paper.questions, 1):
                q_card_html = (
                    f'<div style="background-color: #1e293b; color: #ffffff; border-left: 5px solid #3b82f6; '
                    f'border-top: 1px solid #334155; border-right: 1px solid #334155; border-bottom: 1px solid #334155; '
                    f'padding: 16px 20px; margin: 18px 0 12px 0; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.3);">'
                    f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">'
                    f'<span style="color: #60a5fa; font-weight: 700; font-size: 15.5px;">Question {idx}</span>'
                    f'<span style="background-color: #334155; color: #cbd5e1; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 600;">{q.marks} Marks &bull; {q.blooms_level.value} &bull; {q.topic_name}</span>'
                    f'</div>'
                    f'<div style="color: #ffffff; font-size: 15.5px; font-weight: 500; line-height: 1.55;">'
                    f'{q.question_text}'
                    f'</div></div>'
                )
                st.markdown(q_card_html, unsafe_allow_html=True)

                if q.question_type == QuestionType.MCQ and q.options:
                    selected_opt = st.radio(
                        f"Select your answer for Q{idx}:",
                        options=q.options,
                        index=None,
                        key=f"mcq_{selected_paper.paper_id}_{q.question_id}"
                    )
                    # Extract single letter
                    opt_letter = selected_opt[0] if selected_opt else ""
                    user_answers[q.question_id] = StudentAnswer(question_id=q.question_id, selected_option=opt_letter)
                else:
                    ans_text = st.text_area(
                        f"Enter your written response for Q{idx}:",
                        placeholder="Write your explanation or step-by-step solution here...",
                        height=100,
                        key=f"desc_{selected_paper.paper_id}_{q.question_id}"
                    )
                    user_answers[q.question_id] = StudentAnswer(question_id=q.question_id, descriptive_response=ans_text)

            submit_exam = st.form_submit_button("🚀 Submit Assessment for AI Evaluation", type="primary", use_container_width=True)

        if submit_exam:
            with st.spinner("AI Evaluating Answers, Awarding Step Marks, and Diagnosing Learning Gaps..."):
                eval_result = AssessmentEvaluator.evaluate_submission(
                    paper=selected_paper,
                    answers=user_answers,
                    student_id=student_id,
                    student_name=student_name,
                    llm_client=llm_client,
                    is_adaptive=False
                )
                st.session_state["latest_evaluation"] = eval_result
                st.success(f"🎉 Exam Evaluated! You scored {eval_result.obtained_marks} / {eval_result.total_marks} ({eval_result.percentage}%)")

        # Display latest evaluation results if available
        if "latest_evaluation" in st.session_state:
            res = st.session_state["latest_evaluation"]
            st.divider()
            st.markdown("### 📊 Assessment Performance & Diagnostic Feedback")
            
            c_s1, c_s2, c_s3 = st.columns(3)
            c_s1.metric("Marks Scored", f"{res.obtained_marks} / {res.total_marks}")
            c_s2.metric("Percentage", f"{res.percentage}%")
            status_text = "Mastery Achieved" if res.percentage >= 75 else "Remediation Recommended"
            c_s3.metric("Status", status_text)

            # Topic breakdown
            st.markdown("#### 🎯 Topic-wise Breakdown")
            t_data = []
            for t_name, s_data in res.topic_scores.items():
                t_data.append({
                    "Topic": t_name,
                    "Scored": s_data.get("scored", 0),
                    "Possible": s_data.get("possible", 0),
                    "Mastery %": f"{s_data.get('percentage', 0)}%"
                })
            st.dataframe(pd.DataFrame(t_data), use_container_width=True, hide_index=True)

            # Strengths, Weaknesses, and Misconceptions
            col_sw1, col_sw2 = st.columns(2)
            with col_sw1:
                st.markdown("##### ✅ Demonstrated Strengths")
                for s in res.strengths:
                    st.markdown(f"- **{s}**")
            with col_sw2:
                st.markdown("##### ⚠️ Needs Focus & Revision")
                for w in res.weaknesses:
                    st.markdown(f"- **{w}**")

            if res.recurring_misconceptions:
                st.markdown("##### 🔍 Identified Misconceptions & Cognitive Gaps")
                for m in res.recurring_misconceptions:
                    st.warning(m)

            # Detailed Question-by-Question Feedback Accordion
            st.markdown("#### 🔍 Question-by-Question Step Evaluation & Model Solution")
            for idx, qe in enumerate(res.question_evaluations, 1):
                # Find matching question
                matching_q = next((q for q in selected_paper.questions if q.question_id == qe.question_id), None)
                color_border = "#10b981" if qe.is_correct else "#ef4444"
                
                with st.expander(f"Q{idx}. [{qe.marks_awarded} / {qe.marks_possible} M] - {qe.topic_name} {'✅ Correct' if qe.is_correct else '❌ Needs Review'}"):
                    if matching_q:
                        st.markdown(f"**Question:** {matching_q.question_text}")
                        if matching_q.options:
                            st.write(f"Options: {', '.join(matching_q.options)}")
                        st.markdown(f"**Expected Model Answer:** {matching_q.model_answer}")
                        st.markdown(f"*Explanation:* {matching_q.explanation}")
                    
                    st.markdown(f"**AI Examiner Feedback:** {qe.feedback}")
                    if qe.step_scores:
                        st.write("**Step Marking Breakdown:**")
                        for step in qe.step_scores:
                            st.caption(f"- {step.get('step')}: **{step.get('awarded')} M** ({step.get('comment')})")

    # ---------------- TAB 2: ADAPTIVE PRACTICE ("FORGE MY PATH") ----------------
    with tab2:
        st.subheader("Dual-Adaptive Remedial Practice ('Forge My Path')")
        st.markdown("""
            > **Proposal Novelty Section 4.2 & Technique 5 (Adaptive Prompting):**  
            > ExamForge AI doesn't just grade you—it automatically adapts. Based on your topic-level 
            > errors and detected misconceptions, it crafts a personalized remedial practice set to help you close learning gaps.
        """)

        # Fetch active syllabus
        syllabi = Database.get_all_syllabi()
        if not syllabi:
            st.info("No syllabus loaded yet.")
            return

        syllabus = syllabi[0]
        masteries = Database.get_student_masteries(student_id)
        
        # Display current weak topics
        weak_topics = [t for t, p in masteries.items() if p < 70.0]
        
        col_ad1, col_ad2 = st.columns([2, 1])
        with col_ad1:
            st.write(f"**Adaptive Learner Profile for {student_name} ({student_id}):**")
            if weak_topics:
                st.warning(f"🎯 Target Remedial Focus Topics: {', '.join(weak_topics)}")
            else:
                st.info("All recorded topics currently meet proficiency threshold! Adaptive engine will challenge you with higher-order synthesis questions.")

        with col_ad2:
            q_count = st.slider("Number of Remedial Practice Questions", min_value=2, max_value=5, value=3)

        if st.button("🔥 Forge My Adaptive Practice Set Now", type="primary", use_container_width=True):
            with st.spinner("Synthesizing Diagnostic Gaps into Adaptive Prompt & Crafting Scaffolding Questions..."):
                adaptive_paper = AdaptiveEngine.generate_adaptive_practice(
                    student_id=student_id,
                    student_name=student_name,
                    syllabus=syllabus,
                    llm_client=llm_client,
                    target_count=q_count
                )
                st.session_state["active_adaptive_paper"] = adaptive_paper
                st.success(f"🎉 Generated Personalized Adaptive Set: '{adaptive_paper.title}'!")

        if "active_adaptive_paper" in st.session_state:
            ad_paper = st.session_state["active_adaptive_paper"]
            st.divider()
            st.markdown(f"### 🎯 Remedial Practice: {ad_paper.title}")
            st.caption(ad_paper.teacher_notes)

            with st.form("adaptive_attempt_form"):
                ad_answers: Dict[str, StudentAnswer] = {}
                for idx, q in enumerate(ad_paper.questions, 1):
                    remedial_card_html = (
                        f'<div style="background-color: #1e293b; color: #ffffff; border-left: 5px solid #f59e0b; '
                        f'border-top: 1px solid #334155; border-right: 1px solid #334155; border-bottom: 1px solid #334155; '
                        f'padding: 16px 20px; margin: 18px 0 12px 0; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.3);">'
                        f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">'
                        f'<span style="color: #fbbf24; font-weight: 700; font-size: 15.5px;">Remedial Question {idx}</span>'
                        f'<span style="background-color: #334155; color: #cbd5e1; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 600;">{q.marks} Marks &bull; {q.blooms_level.value} &bull; {q.topic_name}</span>'
                        f'</div>'
                        f'<div style="color: #ffffff; font-size: 15.5px; font-weight: 500; line-height: 1.55;">'
                        f'{q.question_text}'
                        f'</div></div>'
                    )
                    st.markdown(remedial_card_html, unsafe_allow_html=True)

                    if q.question_type == QuestionType.MCQ and q.options:
                        sel_opt = st.radio(
                            f"Answer for Remedial Q{idx}:",
                            options=q.options,
                            index=None,
                            key=f"ad_mcq_{ad_paper.paper_id}_{q.question_id}"
                        )
                        opt_letter = sel_opt[0] if sel_opt else ""
                        ad_answers[q.question_id] = StudentAnswer(question_id=q.question_id, selected_option=opt_letter)
                    else:
                        ans_text = st.text_area(
                            f"Your Remedial Response for Q{idx}:",
                            placeholder="Write your answer showing your renewed understanding...",
                            height=80,
                            key=f"ad_desc_{ad_paper.paper_id}_{q.question_id}"
                        )
                        ad_answers[q.question_id] = StudentAnswer(question_id=q.question_id, descriptive_response=ans_text)

                submit_adaptive = st.form_submit_button("🚀 Submit Remedial Assessment", type="primary", use_container_width=True)

            if submit_adaptive:
                with st.spinner("Evaluating Remedial Answers and Updating Knowledge Mastery..."):
                    eval_res = AssessmentEvaluator.evaluate_submission(
                        paper=ad_paper,
                        answers=ad_answers,
                        student_id=student_id,
                        student_name=student_name,
                        llm_client=llm_client,
                        is_adaptive=True
                    )
                    st.success(f"🎉 Remedial Practice Completed! Scored {eval_res.obtained_marks} / {eval_res.total_marks} ({eval_res.percentage}%)")
                    st.balloons()
                    st.rerun()

    # ---------------- TAB 3: STUDENT PROGRESS & TOPIC MASTERY ----------------
    with tab3:
        st.subheader("Personal Mastery Growth & Learning Journey")
        masteries = Database.get_student_masteries(student_id)
        submissions = Database.get_submissions_by_student(student_id)

        if not masteries and not submissions:
            st.info("No recorded assessment data yet for this student. Take a test in Tab 1 to track your progress!")
            return

        render_stat_row([
            (len(submissions), "Tests Attempted"),
            (f"{sum(s['percentage'] for s in submissions) / len(submissions):.1f}%" if submissions else "0%", "Average Score"),
            (len([t for t, p in masteries.items() if p >= 75.0]), "Proficient Topics"),
            (len([t for t, p in masteries.items() if p < 70.0]), "Remedial Targets")
        ])

        st.divider()
        col_m1, col_m2 = st.columns([1, 1])
        with col_m1:
            st.markdown("#### 📈 Topic Mastery Chart")
            if masteries:
                m_df = pd.DataFrame([{"Topic": t, "Mastery %": p} for t, p in masteries.items()])
                st.dataframe(m_df, use_container_width=True, hide_index=True)
                st.bar_chart(m_df.set_index("Topic")["Mastery %"])

        with col_m2:
            st.markdown("#### 📜 Test History & Score Trajectory")
            if submissions:
                history_df = pd.DataFrame([{
                    "Date": s["submitted_at"][:10],
                    "Test": s["paper_title"],
                    "Score": f"{s['obtained_marks']}/{s['total_marks']}",
                    "Score %": s["percentage"],
                    "Type": "Adaptive Remedial" if s.get("is_adaptive_practice") else "Standard"
                } for s in submissions])
                st.dataframe(history_df, use_container_width=True, hide_index=True)
                st.line_chart(history_df.set_index("Test")["Score %"])
