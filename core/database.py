"""
ExamForge AI - SQLite Persistence Layer
Stores Syllabi, Question Papers, Student Submissions, Topic Mastery Profiles, and Audit Logs.
"""
import sqlite3
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from core.models import Syllabus, QuestionPaper, ExamSubmissionEvaluation, TopicMastery

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "examforge.db")

class Database:
    @staticmethod
    def get_connection():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def init_db(cls):
        """Initializes tables if they do not exist."""
        conn = cls.get_connection()
        cursor = conn.cursor()
        
        # Syllabi table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS syllabi (
                syllabus_id TEXT PRIMARY KEY,
                subject_name TEXT NOT NULL,
                course_code TEXT,
                department TEXT,
                data_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        # Question Papers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS question_papers (
                paper_id TEXT PRIMARY KEY,
                syllabus_id TEXT NOT NULL,
                title TEXT NOT NULL,
                total_marks REAL NOT NULL,
                duration_minutes INTEGER NOT NULL,
                status TEXT NOT NULL,
                data_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (syllabus_id) REFERENCES syllabi (syllabus_id)
            )
        """)

        # Student Submissions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_submissions (
                submission_id TEXT PRIMARY KEY,
                student_id TEXT NOT NULL,
                student_name TEXT NOT NULL,
                paper_id TEXT NOT NULL,
                total_marks REAL NOT NULL,
                obtained_marks REAL NOT NULL,
                percentage REAL NOT NULL,
                is_adaptive_practice INTEGER NOT NULL,
                data_json TEXT NOT NULL,
                submitted_at TEXT NOT NULL
            )
        """)

        # Student Topic Mastery table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_mastery (
                student_id TEXT NOT NULL,
                topic_name TEXT NOT NULL,
                attempted INTEGER NOT NULL,
                correct INTEGER NOT NULL,
                mastery_percentage REAL NOT NULL,
                recent_difficulty TEXT NOT NULL,
                last_updated TEXT NOT NULL,
                PRIMARY KEY (student_id, topic_name)
            )
        """)

        # Prompt Audit Logs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prompt_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                technique TEXT NOT NULL,
                context_type TEXT NOT NULL,
                system_prompt TEXT,
                user_prompt TEXT,
                response_text TEXT,
                created_at TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    # --- Syllabus Operations ---
    @classmethod
    def save_syllabus(cls, syllabus: Syllabus):
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO syllabi (syllabus_id, subject_name, course_code, department, data_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            syllabus.syllabus_id,
            syllabus.subject_name,
            syllabus.course_code,
            syllabus.department,
            json.dumps(syllabus.to_dict()),
            syllabus.created_at
        ))
        conn.commit()
        conn.close()

    @classmethod
    def get_all_syllabi(cls) -> List[Syllabus]:
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT data_json FROM syllabi ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [Syllabus.from_dict(json.loads(r["data_json"])) for r in rows]

    @classmethod
    def get_syllabus(cls, syllabus_id: str) -> Optional[Syllabus]:
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT data_json FROM syllabi WHERE syllabus_id = ?", (syllabus_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Syllabus.from_dict(json.loads(row["data_json"]))
        return None

    # --- Question Paper Operations ---
    @classmethod
    def save_paper(cls, paper: QuestionPaper):
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO question_papers (paper_id, syllabus_id, title, total_marks, duration_minutes, status, data_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            paper.paper_id,
            paper.syllabus_id,
            paper.title,
            paper.total_marks,
            paper.duration_minutes,
            paper.status,
            json.dumps(paper.to_dict()),
            paper.created_at
        ))
        conn.commit()
        conn.close()

    @classmethod
    def get_paper(cls, paper_id: str) -> Optional[QuestionPaper]:
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT data_json FROM question_papers WHERE paper_id = ?", (paper_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
        d = json.loads(row["data_json"])
        from core.models import Question
        questions = [Question.from_dict(q) for q in d.get("questions", [])]
        return QuestionPaper(
            paper_id=d["paper_id"],
            syllabus_id=d["syllabus_id"],
            title=d["title"],
            course_name=d.get("course_name", ""),
            total_marks=d["total_marks"],
            duration_minutes=d["duration_minutes"],
            instructions=d.get("instructions", []),
            questions=questions,
            status=d.get("status", "Draft"),
            created_at=d.get("created_at", datetime.now().isoformat()),
            teacher_notes=d.get("teacher_notes", ""),
            prompt_used=d.get("prompt_used"),
            verification_report=d.get("verification_report")
        )

    @classmethod
    def get_all_papers(cls, status: Optional[str] = None) -> List[QuestionPaper]:
        conn = cls.get_connection()
        cursor = conn.cursor()
        if status:
            cursor.execute("SELECT paper_id FROM question_papers WHERE status = ? ORDER BY created_at DESC", (status,))
        else:
            cursor.execute("SELECT paper_id FROM question_papers ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        papers = []
        for r in rows:
            p = cls.get_paper(r["paper_id"])
            if p:
                papers.append(p)
        return papers

    @classmethod
    def update_paper_status(cls, paper_id: str, new_status: str):
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE question_papers SET status = ? WHERE paper_id = ?", (new_status, paper_id))
        # Also update json
        cursor.execute("SELECT data_json FROM question_papers WHERE paper_id = ?", (paper_id,))
        row = cursor.fetchone()
        if row:
            d = json.loads(row["data_json"])
            d["status"] = new_status
            cursor.execute("UPDATE question_papers SET data_json = ? WHERE paper_id = ?", (json.dumps(d), paper_id))
        conn.commit()
        conn.close()

    # --- Student Submissions & Evaluations ---
    @classmethod
    def save_submission(cls, eval_result: ExamSubmissionEvaluation):
        conn = cls.get_connection()
        cursor = conn.cursor()
        from dataclasses import asdict
        cursor.execute("""
            INSERT OR REPLACE INTO student_submissions 
            (submission_id, student_id, student_name, paper_id, total_marks, obtained_marks, percentage, is_adaptive_practice, data_json, submitted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            eval_result.submission_id,
            eval_result.student_id,
            eval_result.student_name,
            eval_result.paper_id,
            eval_result.total_marks,
            eval_result.obtained_marks,
            eval_result.percentage,
            1 if eval_result.is_adaptive_practice else 0,
            json.dumps(asdict(eval_result)),
            eval_result.submitted_at
        ))
        conn.commit()
        conn.close()

    @classmethod
    def get_submissions_by_student(cls, student_id: str) -> List[Dict[str, Any]]:
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT data_json FROM student_submissions WHERE student_id = ? ORDER BY submitted_at DESC", (student_id,))
        rows = cursor.fetchall()
        conn.close()
        return [json.loads(r["data_json"]) for r in rows]

    @classmethod
    def get_all_submissions(cls) -> List[Dict[str, Any]]:
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT data_json FROM student_submissions ORDER BY submitted_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [json.loads(r["data_json"]) for r in rows]

    # --- Topic Mastery Operations ---
    @classmethod
    def update_topic_mastery(cls, student_id: str, topic_name: str, is_correct: bool, difficulty: str):
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT attempted, correct FROM student_mastery WHERE student_id = ? AND topic_name = ?
        """, (student_id, topic_name))
        row = cursor.fetchone()
        
        if row:
            attempted = row["attempted"] + 1
            correct = row["correct"] + (1 if is_correct else 0)
        else:
            attempted = 1
            correct = 1 if is_correct else 0
            
        pct = round((correct / attempted) * 100.0, 1)
        now = datetime.now().isoformat()
        
        cursor.execute("""
            INSERT OR REPLACE INTO student_mastery (student_id, topic_name, attempted, correct, mastery_percentage, recent_difficulty, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (student_id, topic_name, attempted, correct, pct, difficulty, now))
        conn.commit()
        conn.close()

    @classmethod
    def get_student_masteries(cls, student_id: str) -> Dict[str, float]:
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT topic_name, mastery_percentage FROM student_mastery WHERE student_id = ?
        """, (student_id,))
        rows = cursor.fetchall()
        conn.close()
        return {r["topic_name"]: r["mastery_percentage"] for r in rows}

    # --- Prompt Audit Logging ---
    @classmethod
    def log_prompt(cls, technique: str, context_type: str, system_prompt: str, user_prompt: str, response: str):
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO prompt_logs (technique, context_type, system_prompt, user_prompt, response_text, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (technique, context_type, system_prompt, user_prompt, response, datetime.now().isoformat()))
        conn.commit()
        conn.close()

    @classmethod
    def get_prompt_logs(cls, limit: int = 20) -> List[Dict[str, Any]]:
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM prompt_logs ORDER BY created_at DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]
