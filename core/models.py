"""
ExamForge AI - Data Models and Type Definitions
"""
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Dict, Optional, Any
import json
import uuid
from datetime import datetime

class BloomsLevel(str, Enum):
    REMEMBER = "Remember (L1)"
    UNDERSTAND = "Understand (L2)"
    APPLY = "Apply (L3)"
    ANALYZE = "Analyze (L4)"
    EVALUATE = "Evaluate (L5)"
    CREATE = "Create (L6)"

class DifficultyLevel(str, Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

class QuestionType(str, Enum):
    MCQ = "Multiple Choice Question (MCQ)"
    SHORT_ANSWER = "Short Answer (2-3 Marks)"
    LONG_ANSWER = "Long Answer (5-10 Marks)"
    NUMERICAL_OR_CODE = "Numerical / Code Problem"

@dataclass
class Topic:
    topic_id: str
    title: str
    subtopics: List[str] = field(default_factory=list)
    learning_objectives: List[str] = field(default_factory=list)
    difficulty_hint: str = "Medium"

@dataclass
class SyllabusUnit:
    unit_number: int
    title: str
    description: str
    topics: List[Topic] = field(default_factory=list)

@dataclass
class Syllabus:
    syllabus_id: str
    subject_name: str
    course_code: str
    department: str
    target_audience: str
    units: List[SyllabusUnit] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Syllabus":
        units = []
        for u in data.get("units", []):
            topics = [Topic(**t) for t in u.get("topics", [])]
            units.append(SyllabusUnit(
                unit_number=u["unit_number"],
                title=u["title"],
                description=u.get("description", ""),
                topics=topics
            ))
        return cls(
            syllabus_id=data["syllabus_id"],
            subject_name=data["subject_name"],
            course_code=data.get("course_code", ""),
            department=data.get("department", ""),
            target_audience=data.get("target_audience", ""),
            units=units,
            created_at=data.get("created_at", datetime.now().isoformat())
        )

@dataclass
class MarkingStep:
    step_description: str
    marks_awarded: float

@dataclass
class Question:
    question_id: str
    unit_number: int
    topic_name: str
    question_type: QuestionType
    blooms_level: BloomsLevel
    difficulty: DifficultyLevel
    marks: float
    question_text: str
    options: Optional[List[str]] = None  # For MCQs: ["A. ...", "B. ...", ...]
    correct_option: Optional[str] = None  # e.g., "A"
    model_answer: str = ""
    marking_scheme: List[MarkingStep] = field(default_factory=list)
    explanation: str = ""
    concept_tested: str = ""

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["question_type"] = self.question_type.value
        d["blooms_level"] = self.blooms_level.value
        d["difficulty"] = self.difficulty.value
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Question":
        marking_steps = [MarkingStep(**s) for s in data.get("marking_scheme", [])]
        # Handle string enum conversion
        q_type = data.get("question_type")
        for member in QuestionType:
            if member.value == q_type or member.name == q_type:
                q_type = member
                break
        else:
            q_type = QuestionType.SHORT_ANSWER

        blooms = data.get("blooms_level")
        for member in BloomsLevel:
            if member.value == blooms or member.name == blooms:
                blooms = member
                break
        else:
            blooms = BloomsLevel.UNDERSTAND

        diff = data.get("difficulty")
        for member in DifficultyLevel:
            if member.value == diff or member.name == diff:
                diff = member
                break
        else:
            diff = DifficultyLevel.MEDIUM

        return cls(
            question_id=data["question_id"],
            unit_number=data.get("unit_number", 1),
            topic_name=data.get("topic_name", "General"),
            question_type=q_type,
            blooms_level=blooms,
            difficulty=diff,
            marks=float(data.get("marks", 2.0)),
            question_text=data["question_text"],
            options=data.get("options"),
            correct_option=data.get("correct_option"),
            model_answer=data.get("model_answer", ""),
            marking_scheme=marking_steps,
            explanation=data.get("explanation", ""),
            concept_tested=data.get("concept_tested", "")
        )

@dataclass
class ExamBlueprint:
    title: str
    total_marks: float
    duration_minutes: int
    instructions: List[str]
    unit_distribution: Dict[int, float]  # unit_number -> weightage percentage or marks
    question_type_distribution: Dict[str, int]  # QuestionType -> count
    blooms_distribution: Dict[str, int]  # BloomsLevel -> percentage
    difficulty_distribution: Dict[str, int]  # Easy/Med/Hard percentage

@dataclass
class QuestionPaper:
    paper_id: str
    syllabus_id: str
    title: str
    course_name: str
    total_marks: float
    duration_minutes: int
    instructions: List[str]
    questions: List[Question]
    status: str = "Draft"  # Draft, Reviewed, Approved
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    teacher_notes: str = ""
    prompt_used: Optional[str] = None
    verification_report: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["questions"] = [q.to_dict() for q in self.questions]
        return d

@dataclass
class StudentAnswer:
    question_id: str
    selected_option: Optional[str] = None
    descriptive_response: Optional[str] = None

@dataclass
class QuestionEvaluation:
    question_id: str
    topic_name: str
    marks_possible: float
    marks_awarded: float
    is_correct: bool
    step_scores: List[Dict[str, Any]] = field(default_factory=list)
    feedback: str = ""
    conceptual_error_detected: Optional[str] = None
    misconception_type: Optional[str] = None

@dataclass
class ExamSubmissionEvaluation:
    submission_id: str
    student_id: str
    student_name: str
    paper_id: str
    paper_title: str
    total_marks: float
    obtained_marks: float
    percentage: float
    question_evaluations: List[QuestionEvaluation]
    topic_scores: Dict[str, Dict[str, float]]  # topic -> {scored, possible, percentage}
    strengths: List[str]
    weaknesses: List[str]
    recurring_misconceptions: List[str]
    recommendations: List[str]
    submitted_at: str = field(default_factory=lambda: datetime.now().isoformat())
    is_adaptive_practice: bool = False

@dataclass
class TopicMastery:
    student_id: str
    topic_name: str
    total_attempted: int = 0
    total_correct: int = 0
    mastery_percentage: float = 0.0
    recent_difficulty: str = "Medium"
    identified_gaps: List[str] = field(default_factory=list)
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())
