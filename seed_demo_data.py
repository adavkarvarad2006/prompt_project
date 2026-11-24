"""
ExamForge AI - Seed Script
Initializes the database with sample syllabi, approved question papers,
and student test submissions to immediately demonstrate all analytics and adaptive features.
"""
from core.database import Database
from core.models import (
    ExamBlueprint, QuestionPaper, Question, StudentAnswer, 
    BloomsLevel, DifficultyLevel, QuestionType, MarkingStep
)
from data.sample_syllabi import SAMPLE_PROMPT_ENGINEERING_SYLLABUS, SAMPLE_DSA_SYLLABUS
from core.prompt_engine import PromptEngine
from core.llm_client import LLMClient
from core.evaluator import AssessmentEvaluator
import json

def seed():
    print("Seeding database...")
    Database.init_db()
    Database.save_syllabus(SAMPLE_PROMPT_ENGINEERING_SYLLABUS)
    Database.save_syllabus(SAMPLE_DSA_SYLLABUS)

    client = LLMClient(provider="offline")
    
    # 1. Create Teacher Assessment Paper
    bp = ExamBlueprint(
        title="Mid-Term Assessment: Prompt Engineering (PE-302)",
        total_marks=25.0,
        duration_minutes=45,
        instructions=[
            "Answer all questions in the sequence provided.",
            "Marks for each step are allocated according to the rubric.",
            "Write concise, technically sound answers."
        ],
        unit_distribution={1: 33.3, 2: 33.3, 3: 33.3},
        question_type_distribution={"MCQ": 3, "Short": 3, "Long": 1},
        blooms_distribution={"L1_L2": 35, "L3_L4": 50, "L5_L6": 15},
        difficulty_distribution={"Easy": 30, "Medium": 50, "Hard": 20}
    )

    p_data = PromptEngine.build_question_generation_prompt(SAMPLE_PROMPT_ENGINEERING_SYLLABUS, bp)
    raw = client.call_llm(p_data["system_prompt"], p_data["user_prompt"], json_mode=True)
    d = json.loads(raw)
    questions = [Question.from_dict(q) for q in d["questions"]]

    main_paper = QuestionPaper(
        paper_id="QP-PE-MIDTERM",
        syllabus_id=SAMPLE_PROMPT_ENGINEERING_SYLLABUS.syllabus_id,
        title="Mid-Term Assessment: Prompt Engineering (PE-302)",
        course_name=SAMPLE_PROMPT_ENGINEERING_SYLLABUS.subject_name,
        total_marks=25.0,
        duration_minutes=45,
        instructions=bp.instructions,
        questions=questions,
        status="Approved",
        teacher_notes="Curated baseline assessment paper for prompt engineering curriculum.",
        verification_report={
            "is_approved": True,
            "calculated_total_marks": 25.0,
            "marks_consistent": True,
            "syllabus_compliance_score": 98.6,
            "overall_verdict": "Self-check verification passed. 100% syllabus alignment certified."
        }
    )
    Database.save_paper(main_paper)
    print(f"Saved Question Paper: {main_paper.title}")

    # 2. Simulate 3 student submissions to populate Class Learning Analytics
    students = [
        ("1MS22CS045", "Alex Chen"),
        ("1MS22CS089", "Sophia Martinez"),
        ("1MS22CS102", "Rahul Sharma")
    ]

    for sid, sname in students:
        sample_answers = {}
        for idx, q in enumerate(questions):
            if q.question_type == QuestionType.MCQ:
                # Alex makes an intentional mistake on Q2 to demonstrate the adaptive loop
                opt = q.correct_option if (sid != "1MS22CS045" or idx != 1) else "C"
                sample_answers[q.question_id] = StudentAnswer(question_id=q.question_id, selected_option=opt)
            else:
                sample_answers[q.question_id] = StudentAnswer(
                    question_id=q.question_id, 
                    descriptive_response=f"Structured output constraints enforce syntactic conformance and prevent conversational hallucinations."
                )

        eval_res = AssessmentEvaluator.evaluate_submission(
            paper=main_paper,
            answers=sample_answers,
            student_id=sid,
            student_name=sname,
            llm_client=client,
            is_adaptive=False
        )
        print(f"Evaluated submission for {sname}: {eval_res.obtained_marks}/{eval_res.total_marks} ({eval_res.percentage}%)")

    print("Seeding complete! Database is populated with rich demonstration data.")

if __name__ == "__main__":
    seed()
