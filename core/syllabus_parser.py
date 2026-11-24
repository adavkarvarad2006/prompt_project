"""
ExamForge AI - Syllabus Parser and Text Extraction Engine
Handles raw text, Markdown, JSON, and document inputs to extract Units, Topics, and Objectives.
"""
import re
import json
import uuid
from typing import Dict, Any, List
from core.models import Syllabus, SyllabusUnit, Topic

class SyllabusParser:
    @classmethod
    def parse_text_syllabus(
        cls, 
        raw_text: str, 
        subject_name: str, 
        course_code: str = "", 
        department: str = "", 
        target_audience: str = ""
    ) -> Syllabus:
        """
        Extracts structured Units and Topics from raw syllabus text using
        hierarchical pattern recognition.
        """
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        units: List[SyllabusUnit] = []
        current_unit: SyllabusUnit = None
        current_topic: Topic = None
        unit_counter = 1

        for line in lines:
            # Check for Unit header: e.g. "Unit 1: Foundations", "MODULE 1 - Basics", "CHAPTER 1:"
            unit_match = re.search(r'^(?:unit|module|chapter|part)\s*([0-9ivxlcdm]+)[:.\-–]\s*(.*)$', line, re.IGNORECASE)
            if unit_match:
                u_num = unit_counter
                try:
                    u_num = int(unit_match.group(1))
                except ValueError:
                    u_num = unit_counter
                u_title = unit_match.group(2).strip() or f"Unit {u_num}"
                current_unit = SyllabusUnit(unit_number=u_num, title=u_title, description="", topics=[])
                units.append(current_unit)
                unit_counter += 1
                current_topic = None
                continue

            # If no unit header was found yet, create a default Unit 1
            if not current_unit:
                current_unit = SyllabusUnit(unit_number=1, title="Core Curriculum", description="", topics=[])
                units.append(current_unit)

            # Check for Topic header: bullet points, numbered items, "Topic:", etc.
            topic_match = re.search(r'^(?:[-*•]|\d+\.\d+|\d+\))\s*(.*)$', line)
            if topic_match:
                t_title = topic_match.group(1).strip()
                if len(t_title) > 3:
                    # Split subtopics if separated by commas or semicolons
                    subtopics = []
                    if ":" in t_title:
                        parts = t_title.split(":", 1)
                        t_main = parts[0].strip()
                        subtopics = [s.strip() for s in re.split(r'[,;]', parts[1]) if s.strip()]
                        t_title = t_main
                    
                    current_topic = Topic(
                        topic_id=f"T{current_unit.unit_number}.{len(current_unit.topics)+1}",
                        title=t_title,
                        subtopics=subtopics,
                        learning_objectives=[f"Understand and apply concepts of {t_title}"]
                    )
                    current_unit.topics.append(current_topic)
                    continue

            # Fallback: append as description or subtopic
            if current_topic:
                current_topic.subtopics.append(line)
            elif current_unit:
                if current_unit.description:
                    current_unit.description += " " + line
                else:
                    current_unit.description = line

        # Final cleanup: ensure each unit has at least one topic
        for u in units:
            if not u.topics:
                u.topics.append(Topic(
                    topic_id=f"T{u.unit_number}.1",
                    title=u.title,
                    subtopics=[],
                    learning_objectives=[f"Master foundational concepts in {u.title}"]
                ))

        return Syllabus(
            syllabus_id=f"SYLL-{uuid.uuid4().hex[:8].upper()}",
            subject_name=subject_name,
            course_code=course_code,
            department=department,
            target_audience=target_audience,
            units=units
        )
