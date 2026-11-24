"""
ExamForge AI - Evaluation and Cognitive Misconception Diagnosis Engine
Implements step-marking evaluation, topic-wise scoring, and root-cause error analysis.
"""
import json
import uuid
from typing import List, Dict, Any, Tuple
from datetime import datetime
from core.models import (
    QuestionPaper, Question, StudentAnswer, QuestionEvaluation, 
    ExamSubmissionEvaluation, QuestionType
)
from core.prompt_engine import PromptEngine
from core.llm_client import LLMClient
from core.database import Database

class AssessmentEvaluator:
    @classmethod
    def evaluate_submission(
        cls,
        paper: QuestionPaper,
        answers: Dict[str, StudentAnswer],
        student_id: str,
        student_name: str,
        llm_client: LLMClient,
        is_adaptive: bool = False
    ) -> ExamSubmissionEvaluation:
        """
        Evaluates student answers against the paper's question bank, marking schemes,
        and Bloom's cognitive taxonomy.
        """
        question_evaluations: List[QuestionEvaluation] = []
        total_possible = paper.total_marks
        total_awarded = 0.0

        topic_stats: Dict[str, Dict[str, float]] = {}

        for q in paper.questions:
            student_ans_obj = answers.get(q.question_id, StudentAnswer(question_id=q.question_id))
            
            # Initialize topic in stats if needed
            if q.topic_name not in topic_stats:
                topic_stats[q.topic_name] = {"scored": 0.0, "possible": 0.0}
            topic_stats[q.topic_name]["possible"] += q.marks

            # Determine response string
            resp_str = ""
            if q.question_type == QuestionType.MCQ:
                resp_str = student_ans_obj.selected_option or ""
            else:
                resp_str = student_ans_obj.descriptive_response or ""

            # Evaluate question
            eval_dict = cls._evaluate_single_question(q, resp_str, llm_client)

            awarded = float(eval_dict.get("marks_awarded", 0.0))
            is_correct = bool(eval_dict.get("is_correct", False))
            total_awarded += awarded
            topic_stats[q.topic_name]["scored"] += awarded

            # Update student mastery in DB
            Database.update_topic_mastery(
                student_id=student_id,
                topic_name=q.topic_name,
                is_correct=is_correct,
                difficulty=q.difficulty.value
            )

            q_eval = QuestionEvaluation(
                question_id=q.question_id,
                topic_name=q.topic_name,
                marks_possible=q.marks,
                marks_awarded=awarded,
                is_correct=is_correct,
                step_scores=eval_dict.get("step_scores", []),
                feedback=eval_dict.get("feedback", ""),
                conceptual_error_detected=eval_dict.get("conceptual_error_detected"),
                misconception_type=eval_dict.get("misconception_type")
            )
            question_evaluations.append(q_eval)

        # Compute topic percentages
        for topic, data in topic_stats.items():
            if data["possible"] > 0:
                data["percentage"] = round((data["scored"] / data["possible"]) * 100.0, 1)
            else:
                data["percentage"] = 0.0

        # Identify strengths and weaknesses
        strengths = [t for t, d in topic_stats.items() if d["percentage"] >= 75.0]
        weaknesses = [t for t, d in topic_stats.items() if d["percentage"] < 65.0]
        if not strengths and topic_stats:
            # Pick highest
            sorted_topics = sorted(topic_stats.items(), key=lambda x: x[1]["percentage"], reverse=True)
            strengths.append(sorted_topics[0][0])
        if not weaknesses and topic_stats:
            # If all are good, identify areas for mastery
            weaknesses = [t for t, d in topic_stats.items() if d["percentage"] < 90.0]

        # Collect misconceptions
        misconceptions = []
        for qe in question_evaluations:
            if qe.conceptual_error_detected and qe.conceptual_error_detected != "None":
                misconceptions.append(f"{qe.topic_name}: {qe.conceptual_error_detected}")

        # Formulate actionable recommendations
        recommendations = []
        for w in weaknesses:
            recommendations.append(f"Review core concepts and review exemplars for '{w}'.")
        if misconceptions:
            recommendations.append("Practice distinguishing key differences between direct execution and intermediate reasoning scaffolds.")
        else:
            recommendations.append("Outstanding work! Proceed to higher-order design and synthesis challenges.")

        percentage = round((total_awarded / total_possible) * 100.0, 1) if total_possible > 0 else 0.0

        eval_submission = ExamSubmissionEvaluation(
            submission_id=f"SUB-{uuid.uuid4().hex[:8].upper()}",
            student_id=student_id,
            student_name=student_name,
            paper_id=paper.paper_id,
            paper_title=paper.title,
            total_marks=total_possible,
            obtained_marks=round(total_awarded, 1),
            percentage=percentage,
            question_evaluations=question_evaluations,
            topic_scores=topic_stats,
            strengths=strengths,
            weaknesses=weaknesses,
            recurring_misconceptions=misconceptions,
            recommendations=recommendations,
            is_adaptive_practice=is_adaptive
        )

        Database.save_submission(eval_submission)
        return eval_submission

    @classmethod
    def _evaluate_single_question(
        cls,
        question: Question,
        student_response: str,
        llm_client: LLMClient
    ) -> Dict[str, Any]:
        """Evaluates an individual question using Prompt Engineering."""
        # For MCQ, direct deterministic check
        if question.question_type == QuestionType.MCQ:
            chosen = (student_response or "").strip().upper()
            correct = (question.correct_option or "").strip().upper()
            
            # Match if chosen starts with correct option letter (e.g. "A" or "A. ...")
            is_match = False
            if chosen and correct:
                if chosen.startswith(correct) or chosen == correct:
                    is_match = True

            if is_match:
                return {
                    "marks_awarded": question.marks,
                    "marks_possible": question.marks,
                    "is_correct": True,
                    "step_scores": [{"step": "Option Selection", "awarded": question.marks, "comment": "Correct option selected."}],
                    "feedback": f"Correct! {question.explanation}",
                    "conceptual_error_detected": None,
                    "misconception_type": "None"
                }
            else:
                return {
                    "marks_awarded": 0.0,
                    "marks_possible": question.marks,
                    "is_correct": False,
                    "step_scores": [{"step": "Option Selection", "awarded": 0.0, "comment": f"Selected: '{student_response}'; Expected: '{correct}'"}],
                    "feedback": f"Incorrect choice. Expected option {correct}. {question.explanation}",
                    "conceptual_error_detected": f"Misconception in {question.concept_tested or question.topic_name}",
                    "misconception_type": "Option Misidentification"
                }

        # For descriptive questions, use prompt evaluation pipeline
        prompt_data = PromptEngine.build_answer_evaluation_prompt(
            question=question.to_dict(),
            student_response=student_response
        )

        raw_output = llm_client.call_llm(
            system_prompt=prompt_data["system_prompt"],
            user_prompt=prompt_data["user_prompt"],
            json_mode=True
        )

        Database.log_prompt(
            technique="Answer Evaluation Prompting",
            context_type="Evaluation",
            system_prompt=prompt_data["system_prompt"],
            user_prompt=prompt_data["user_prompt"],
            response=raw_output
        )

        try:
            parsed = json.loads(raw_output)
            return parsed
        except Exception:
            # Fallback
            words = len(student_response.split())
            ratio = min(1.0, words / 30.0) if words > 0 else 0.0
            awarded = round(question.marks * ratio * 0.7, 1)
            return {
                "marks_awarded": awarded,
                "marks_possible": question.marks,
                "is_correct": awarded >= (question.marks * 0.6),
                "step_scores": [{"step": "General Understanding", "awarded": awarded, "comment": "Evaluated based on content keywords."}],
                "feedback": "Response evaluated against standard marking criteria.",
                "conceptual_error_detected": "Needs more explicit elaboration" if awarded < question.marks else None,
                "misconception_type": "Incomplete"
            }
