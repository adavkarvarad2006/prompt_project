"""
ExamForge AI - Dual-Adaptive Learning and Recommendation Engine
Generates targeted remedial practice papers calibrated to individual student gaps.
"""
import json
import uuid
from typing import Dict, Any, List, Optional
from core.models import (
    Syllabus, QuestionPaper, Question, ExamSubmissionEvaluation,
    TopicMastery, BloomsLevel, DifficultyLevel, QuestionType, MarkingStep
)
from core.prompt_engine import PromptEngine
from core.llm_client import LLMClient
from core.database import Database

class AdaptiveEngine:
    @classmethod
    def generate_adaptive_practice(
        cls,
        student_id: str,
        student_name: str,
        syllabus: Syllabus,
        llm_client: LLMClient,
        target_count: int = 3
    ) -> QuestionPaper:
        """
        Synthesizes student's topic mastery and recent mistakes into an adaptive prompt,
        invokes the LLM, and produces a personalized remedial practice paper.
        """
        # Fetch student mastery from DB
        masteries = Database.get_student_masteries(student_id)
        
        # Fetch previous submissions to detect recurring misconceptions
        submissions = Database.get_submissions_by_student(student_id)
        
        weak_topics = []
        recurring_misconceptions = []
        
        # Collect weak topics (< 70% mastery)
        for topic, pct in masteries.items():
            if pct < 70.0:
                weak_topics.append(topic)
                
        # Also check recent submissions for errors
        for sub in submissions[:3]:
            for w in sub.get("weaknesses", []):
                if w not in weak_topics:
                    weak_topics.append(w)
            for m in sub.get("recurring_misconceptions", []):
                if m not in recurring_misconceptions:
                    recurring_misconceptions.append(m)

        # Fallback if no weaknesses recorded yet: pick first syllabus topics
        if not weak_topics:
            all_topics = [t.title for u in syllabus.units for t in u.topics]
            weak_topics = all_topics[:2] if all_topics else ["Foundations"]

        # Build adaptive prompt
        prompt_data = PromptEngine.build_adaptive_practice_prompt(
            syllabus=syllabus,
            student_name=student_name,
            weak_topics=weak_topics,
            recurring_misconceptions=recurring_misconceptions,
            current_mastery_scores=masteries,
            target_question_count=target_count
        )

        raw_output = llm_client.call_llm(
            system_prompt=prompt_data["system_prompt"],
            user_prompt=prompt_data["user_prompt"],
            json_mode=True
        )

        Database.log_prompt(
            technique="Adaptive Remedial Prompting",
            context_type="Adaptive Practice Generation",
            system_prompt=prompt_data["system_prompt"],
            user_prompt=prompt_data["user_prompt"],
            response=raw_output
        )

        try:
            parsed = json.loads(raw_output)
            questions = []
            for q_data in parsed.get("questions", []):
                questions.append(Question.from_dict(q_data))

            paper_id = f"ADAPT-{uuid.uuid4().hex[:8].upper()}"
            adaptive_paper = QuestionPaper(
                paper_id=paper_id,
                syllabus_id=syllabus.syllabus_id,
                title=parsed.get("title", f"Adaptive Practice for {student_name}"),
                course_name=parsed.get("course_name", syllabus.subject_name),
                total_marks=float(parsed.get("total_marks", target_count * 2.0)),
                duration_minutes=int(parsed.get("duration_minutes", 15)),
                instructions=parsed.get("instructions", [
                    "Targeted practice set tailored to your recent assessment performance."
                ]),
                questions=questions,
                status="Approved",  # Auto-approved for student personalized practice
                teacher_notes=f"Auto-generated adaptive set addressing weaknesses: {', '.join(weak_topics)}",
                prompt_used=prompt_data["user_prompt"]
            )
            Database.save_paper(adaptive_paper)
            return adaptive_paper

        except Exception as e:
            print(f"[AdaptiveEngine] Error parsing adaptive paper: {e}")
            # Fallback to simulated paper
            sim_json = json.loads(llm_client._simulate_adaptive_practice(prompt_data["user_prompt"]))
            questions = [Question.from_dict(q) for q in sim_json["questions"]]
            paper_id = f"ADAPT-{uuid.uuid4().hex[:8].upper()}"
            fallback_paper = QuestionPaper(
                paper_id=paper_id,
                syllabus_id=syllabus.syllabus_id,
                title=sim_json["title"],
                course_name=sim_json["course_name"],
                total_marks=float(sim_json["total_marks"]),
                duration_minutes=int(sim_json["duration_minutes"]),
                instructions=sim_json["instructions"],
                questions=questions,
                status="Approved",
                teacher_notes=f"Auto-generated adaptive practice for {', '.join(weak_topics)}",
                prompt_used=prompt_data["user_prompt"]
            )
            Database.save_paper(fallback_paper)
            return fallback_paper
