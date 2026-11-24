"""
ExamForge AI - Prompt Engineering Core Engine
Implements the 6 Core Prompt Engineering Techniques:
1. Role-based Prompting
2. Contextual Prompting
3. Few-shot Prompting
4. Structured Output Prompting
5. Adaptive Prompting
6. Self-Check / Verification Prompting
"""
from typing import Dict, List, Any, Optional
import json
from core.models import (
    Syllabus, SyllabusUnit, Topic, BloomsLevel, DifficultyLevel, 
    QuestionType, ExamBlueprint, TopicMastery
)

class PromptEngine:
    """
    Central orchestrator for crafting pedagogical, syllabus-aware prompts
    using proven Prompt Engineering paradigms.
    """

    # 1. ROLE DEFINITIONS (Role-Based Prompting)
    ROLES = {
        "EXAMINER": (
            "You are a Senior Academic Examiner and Curriculum Assessment Specialist with over 15 years "
            "of experience in University and Board Examination design. Your expertise is in crafting "
            "rigorous, unambiguous, syllabus-aligned questions with precise marking rubrics adhering to "
            "Bloom's Revised Taxonomy."
        ),
        "TUTOR": (
            "You are an Empathetic Adaptive Socratic Tutor and Cognitive Learning Coach. Your goal is to identify "
            "conceptual misconceptions, explain fundamental principles without just giving away answers, "
            "and design targeted remedial challenges that scaffold student mastery from novice to proficient."
        ),
        "EVALUATOR": (
            "You are an Objective Academic Moderator and Step-Marking Evaluator. You assess student answers "
            "strictly against predefined step marking criteria, awarding partial credit for valid reasoning, "
            "identifying exact keywords missing, and diagnosing the root cognitive error or misconception."
        ),
        "VERIFIER": (
            "You are an Independent Quality Assurance Auditor and Syllabus Compliance Verifier for higher education. "
            "You meticulously inspect draft question papers to detect topic drift, mark calculation errors, "
            "duplicate stems, answer ambiguity, and violations of Bloom's distribution."
        )
    }

    # 3. FEW-SHOT EXEMPLARS (Few-Shot Prompting)
    FEW_SHOT_QUESTION_GENERATION = [
        {
            "context": "Subject: Prompt Engineering | Unit: Advanced Prompting Techniques | Bloom: Apply (L3) | Marks: 5",
            "desired_output": {
                "question_id": "EX-FEW-001",
                "unit_number": 2,
                "topic_name": "Few-Shot Prompting and In-Context Learning",
                "question_type": "Short Answer (2-3 Marks)",
                "blooms_level": "Apply (L3)",
                "difficulty": "Medium",
                "marks": 5.0,
                "question_text": "A customer support team wants an LLM to categorize incoming emails into: 'Billing', 'Technical Bug', and 'General Inquiry'. Write a Few-Shot prompt template containing 2 balanced exemplars that ensures deterministic classification.",
                "model_answer": "System: You are an email classifier. Output ONLY the category name.\nUser: Email: 'I was charged twice for invoice #4421'\nAssistant: Billing\nUser: Email: 'The export button throws a 500 server error'\nAssistant: Technical Bug\nUser: Email: {input_email}\nAssistant:",
                "marking_scheme": [
                    {"step_description": "Clear role/task instruction specifying constrained output", "marks_awarded": 1.5},
                    {"step_description": "At least 2 accurate, non-conflicting exemplars covering distinct classes", "marks_awarded": 2.0},
                    {"step_description": "Clean placeholder delimiter formatting for target test input", "marks_awarded": 1.5}
                ],
                "explanation": "Few-shot prompting provides demonstrations that establish format and semantic boundaries for the LLM without parameter fine-tuning.",
                "concept_tested": "In-context demonstration construction and class balance"
            }
        },
        {
            "context": "Subject: Computer Science | Topic: Binary Search Trees | Bloom: Analyze (L4) | Marks: 2",
            "desired_output": {
                "question_id": "EX-FEW-002",
                "unit_number": 1,
                "topic_name": "Binary Search Trees",
                "question_type": "Multiple Choice Question (MCQ)",
                "blooms_level": "Analyze (L4)",
                "difficulty": "Medium",
                "marks": 2.0,
                "question_text": "Consider inserting the sequence [50, 30, 70, 20, 40, 60, 80] into an empty Binary Search Tree. What is the height of the resulting tree (assuming root is at height 0), and what is the in-order predecessor of node 50?",
                "options": [
                    "A. Height: 2; In-order predecessor: 40",
                    "B. Height: 3; In-order predecessor: 30",
                    "C. Height: 2; In-order predecessor: 60",
                    "D. Height: 3; In-order predecessor: 40"
                ],
                "correct_option": "A",
                "model_answer": "Option A. The tree is balanced with 3 levels (height 0, 1, 2). The maximum value in the left subtree of 50 is node 40.",
                "marking_scheme": [
                    {"step_description": "Correct identification of tree height = 2 and predecessor = 40", "marks_awarded": 2.0}
                ],
                "explanation": "Left subtree has 30, with children 20 and 40. Right subtree has 70, with children 60 and 80. Max depth from root is 2 edges. In-order predecessor is the rightmost element in the left subtree (40).",
                "concept_tested": "BST height computation and in-order traversal properties"
            }
        }
    ]

    FEW_SHOT_EVALUATION = [
        {
            "question": "Explain the difference between Zero-Shot and Few-Shot prompting with an example for each (4 Marks).",
            "marking_scheme": [
                {"step_description": "Correct definition of Zero-Shot prompting", "marks_awarded": 1.0},
                {"step_description": "Valid Zero-Shot example", "marks_awarded": 1.0},
                {"step_description": "Correct definition of Few-Shot prompting", "marks_awarded": 1.0},
                {"step_description": "Valid Few-Shot example showing input-output pairs", "marks_awarded": 1.0}
            ],
            "student_answer": "Zero-shot is when you ask the AI to do a task without giving examples, like 'Translate hello to French'. Few shot is when you give some examples before the query so it learns the pattern.",
            "evaluation_result": {
                "marks_awarded": 3.0,
                "marks_possible": 4.0,
                "is_correct": False,
                "step_scores": [
                    {"step": "Definition of Zero-Shot", "awarded": 1.0, "comment": "Accurate definition provided."},
                    {"step": "Zero-Shot example", "awarded": 1.0, "comment": "Valid translation example provided."},
                    {"step": "Definition of Few-Shot", "awarded": 1.0, "comment": "Correctly states examples are given to demonstrate pattern."},
                    {"step": "Few-Shot example", "awarded": 0.0, "comment": "Missing explicit exemplar input-output pair."}
                ],
                "feedback": "Great conceptual understanding! However, you did not write out a concrete Few-Shot example with input-output demonstrations as requested.",
                "conceptual_error_detected": "Omission of illustrative example in dual-part question",
                "misconception_type": "Incomplete Demonstration"
            }
        }
    ]

    @classmethod
    def build_question_generation_prompt(
        cls, 
        syllabus: Syllabus, 
        blueprint: ExamBlueprint,
        selected_units: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        Builds a comprehensive prompt using:
        - Role-based prompting (Academic Examiner)
        - Contextual prompting (Syllabus text, unit titles, objectives)
        - Few-shot prompting (Exemplar JSON items)
        - Structured output prompting (Strict JSON schema specifications)
        """
        role_text = cls.ROLES["EXAMINER"]
        
        # Build contextual syllabus summary
        context_lines = [
            f"Subject: {syllabus.subject_name} ({syllabus.course_code})",
            f"Department: {syllabus.department} | Target Audience: {syllabus.target_audience}",
            "\nSyllabus Units and Learning Objectives:"
        ]
        
        for unit in syllabus.units:
            if selected_units and unit.unit_number not in selected_units:
                continue
            context_lines.append(f"--- UNIT {unit.unit_number}: {unit.title} ---")
            context_lines.append(f"Summary: {unit.description}")
            for topic in unit.topics:
                subtopics_str = ", ".join(topic.subtopics) if topic.subtopics else "N/A"
                objs_str = "; ".join(topic.learning_objectives) if topic.learning_objectives else "General mastery"
                context_lines.append(f"  * Topic: {topic.title} (Subtopics: {subtopics_str}) -> Objectives: {objs_str}")

        syllabus_context = "\n".join(context_lines)

        blueprint_specs = [
            f"Total Paper Marks: {blueprint.total_marks}",
            f"Time Duration: {blueprint.duration_minutes} Minutes",
            f"General Instructions: {'; '.join(blueprint.instructions)}",
            f"Difficulty Split: {json.dumps(blueprint.difficulty_distribution)}",
            f"Cognitive Bloom's Split: {json.dumps(blueprint.blooms_distribution)}",
            f"Question Type Breakdown: {json.dumps(blueprint.question_type_distribution)}"
        ]
        blueprint_context = "\n".join(blueprint_specs)

        system_prompt = f"""{role_text}

You must construct an academically rigorous, authentic, and perfectly aligned question paper based SOLELY on the provided syllabus and blueprint constraints.

RULES:
1. Every question MUST directly map to a listed unit, topic, and learning objective.
2. Provide precise, actionable Step Marking Schemes with fractional mark allocations summing exactly to the question's marks.
3. For Multiple Choice Questions, provide exactly 4 options labeled A, B, C, D, with plausible distractors reflecting common student misconceptions.
4. Provide comprehensive model answers and pedagogical explanations.
5. You MUST return strictly valid JSON matching the schema outlined below.
"""

        user_prompt = f"""=== CONTEXT: SYLLABUS DETAILS ===
{syllabus_context}

=== BLUEPRINT SPECIFICATIONS ===
{blueprint_context}

=== FEW-SHOT EXEMPLAR OUTPUT FORMAT ===
{json.dumps(cls.FEW_SHOT_QUESTION_GENERATION, indent=2)}

=== REQUIRED JSON OUTPUT SCHEMA ===
Produce a JSON object with this exact structure:
{{
  "title": "{blueprint.title}",
  "course_name": "{syllabus.subject_name}",
  "total_marks": {blueprint.total_marks},
  "duration_minutes": {blueprint.duration_minutes},
  "instructions": {json.dumps(blueprint.instructions)},
  "questions": [
    {{
      "question_id": "Q-001",
      "unit_number": 1,
      "topic_name": "Topic Name Here",
      "question_type": "Multiple Choice Question (MCQ) | Short Answer (2-3 Marks) | Long Answer (5-10 Marks) | Numerical / Code Problem",
      "blooms_level": "Remember (L1) | Understand (L2) | Apply (L3) | Analyze (L4) | Evaluate (L5) | Create (L6)",
      "difficulty": "Easy | Medium | Hard",
      "marks": 2.0,
      "question_text": "Detailed question text...",
      "options": ["A. Option 1", "B. Option 2", "C. Option 3", "D. Option 4"],
      "correct_option": "A",
      "model_answer": "Complete expected answer...",
      "marking_scheme": [
        {{"step_description": "First step / point", "marks_awarded": 1.0}},
        {{"step_description": "Second step / point", "marks_awarded": 1.0}}
      ],
      "explanation": "Pedagogical explanation of why this answer is correct...",
      "concept_tested": "Core concept tested"
    }}
  ]
}}
"""
        return {
            "technique": "Role-Based + Contextual + Few-Shot + Structured Output",
            "system_prompt": system_prompt,
            "user_prompt": user_prompt
        }

    @classmethod
    def build_self_check_verification_prompt(cls, draft_paper_json: Dict[str, Any], syllabus: Syllabus) -> Dict[str, Any]:
        """
        Builds the 6th technique: Self-Check / Verification Prompting (Meta-Prompting).
        The model acts as an auditor checking:
        - Marks summation equality
        - Syllabus alignment & topic drift
        - No duplicate questions
        - Distractor quality
        - Bloom's distribution adherence
        """
        role_text = cls.ROLES["VERIFIER"]
        
        system_prompt = f"""{role_text}

Your job is to perform a rigorous Self-Check and Verification Audit on a draft question paper.
Inspect every question against the syllabus and the rules below:
1. MARKS INTEGRITY: Does the sum of question marks match total_marks? Do marking_scheme step marks sum to each question's marks?
2. SYLLABUS ADHERENCE: Does any question test out-of-syllabus content?
3. DUPLICATION: Are any questions or tested concepts redundant?
4. CLARITY: Are question stems clear, unambiguous, and grammatically impeccable?
5. ANSWER KEYS: Are MCQ keys accurate and model answers thorough?
"""

        user_prompt = f"""=== DRAFT QUESTION PAPER FOR VERIFICATION ===
{json.dumps(draft_paper_json, indent=2)}

=== AUTHORITATIVE SYLLABUS TOPICS ===
Subject: {syllabus.subject_name}
Topics: {[t.title for u in syllabus.units for t in u.topics]}

=== VERIFICATION OUTPUT SCHEMA ===
Respond with a JSON object:
{{
  "is_approved": true or false,
  "calculated_total_marks": 25.0,
  "marks_consistent": true,
  "syllabus_compliance_score": 98.5,
  "detected_issues": [
    {{"question_id": "Q-003", "severity": "Warning | Error", "issue": "Description of issue", "suggestion": "Fix suggestion"}}
  ],
  "blooms_audit": {{"L1_L2_percentage": 40, "L3_L4_percentage": 50, "L5_L6_percentage": 10}},
  "overall_verdict": "Clear summary of audit findings and certification for teacher approval."
}}
"""
        return {
            "technique": "Self-Check / Verification Prompting (Meta-Prompting)",
            "system_prompt": system_prompt,
            "user_prompt": user_prompt
        }

    @classmethod
    def build_answer_evaluation_prompt(
        cls,
        question: Dict[str, Any],
        student_response: str
    ) -> Dict[str, Any]:
        """
        Builds prompt for evaluating subjective or MCQ student responses.
        Uses:
        - Role-based (Step-Marking Evaluator)
        - Contextual (Question, Model Answer, Rubric)
        - Few-Shot (Grading exemplar)
        - Structured Output
        """
        role_text = cls.ROLES["EVALUATOR"]
        
        system_prompt = f"""{role_text}

You must evaluate a student's answer against the given model answer and step marking scheme.
Award marks strictly according to demonstrated understanding.
Award partial credit wherever valid intermediate reasoning is present.
Diagnose any conceptual misconception or knowledge gap.
"""

        user_prompt = f"""=== QUESTION DETAILS ===
Question Text: {question.get('question_text')}
Question Type: {question.get('question_type')}
Marks Possible: {question.get('marks')}
Model Answer: {question.get('model_answer')}
Marking Scheme Steps: {json.dumps(question.get('marking_scheme', []), indent=2)}
Concept Tested: {question.get('concept_tested')}

=== STUDENT SUBMITTED RESPONSE ===
"{student_response}"

=== FEW-SHOT EVALUATION EXEMPLAR ===
{json.dumps(cls.FEW_SHOT_EVALUATION[0], indent=2)}

=== REQUIRED JSON EVALUATION SCHEMA ===
{{
  "marks_awarded": 2.5,
  "marks_possible": {question.get('marks')},
  "is_correct": true or false,
  "step_scores": [
    {{"step": "Step description", "awarded": 1.0, "comment": "Feedback on this step"}}
  ],
  "feedback": "Constructive, supportive feedback for the student...",
  "conceptual_error_detected": "Brief description of any fundamental gap or null",
  "misconception_type": "None | Syntax Error | Logic Flaw | Missing Prerequisite | Incomplete Explanation"
}}
"""
        return {
            "technique": "Role-Based + Contextual + Few-Shot Evaluation Prompting",
            "system_prompt": system_prompt,
            "user_prompt": user_prompt
        }

    @classmethod
    def build_adaptive_practice_prompt(
        cls,
        syllabus: Syllabus,
        student_name: str,
        weak_topics: List[str],
        recurring_misconceptions: List[str],
        current_mastery_scores: Dict[str, float],
        target_question_count: int = 5
    ) -> Dict[str, Any]:
        """
        Builds the 5th technique: Adaptive Prompting.
        Injects student-specific learning gaps, historical errors, and current mastery
        to create a tailored remedial practice challenge with progressive scaffolding.
        """
        role_text = cls.ROLES["TUTOR"]

        system_prompt = f"""{role_text}

You are designing an Adaptive Personalized Practice Set specifically calibrated for a student's demonstrated learning gaps.
The student has taken an assessment and struggled with specific topics and misconceptions.

YOUR PEDAGOGICAL GOAL:
1. Target the identified weak topics directly.
2. Provide progressive scaffolding: start with a conceptual clarifier (Medium/Easy) to build confidence, followed by application/analysis questions targeting the misconception.
3. Every question must include a rich Socratic explanation that deconstructs the misconception.
"""

        user_prompt = f"""=== STUDENT PROFILE & DIAGNOSTIC GAPS ===
Student Name: {student_name}
Weak Topics Identified: {json.dumps(weak_topics)}
Recurring Misconceptions: {json.dumps(recurring_misconceptions)}
Current Topic Mastery Percentages: {json.dumps(current_mastery_scores)}
Number of Target Remedial Questions: {target_question_count}

=== SYLLABUS TOPICS REFERENCE ===
Subject: {syllabus.subject_name}
Available Units: {[(u.unit_number, u.title) for u in syllabus.units]}

=== ADAPTIVE PROMPT INSTRUCTION ===
Generate a remedial practice set containing {target_question_count} questions.
Focus 80% of questions on the weak topics: {', '.join(weak_topics) if weak_topics else 'Core Syllabus Topics'}.
Format as strict JSON:
{{
  "title": "Adaptive Remedial Practice for {student_name}",
  "course_name": "{syllabus.subject_name}",
  "total_marks": {target_question_count * 2.0},
  "duration_minutes": {target_question_count * 3},
  "instructions": [
    "This personalized test has been tailored to help you master your specific learning gaps.",
    "Read each question carefully; detailed explanations will be provided upon submission."
  ],
  "questions": [
    {{
      "question_id": "ADAPT-001",
      "unit_number": 1,
      "topic_name": "Targeted Weak Topic",
      "question_type": "Multiple Choice Question (MCQ) | Short Answer (2-3 Marks)",
      "blooms_level": "Understand (L2) | Apply (L3) | Analyze (L4)",
      "difficulty": "Easy | Medium",
      "marks": 2.0,
      "question_text": "Targeted question addressing the specific misconception...",
      "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
      "correct_option": "A",
      "model_answer": "Model solution...",
      "marking_scheme": [{{"step_description": "Concept application", "marks_awarded": 2.0}}],
      "explanation": "Socratic clarification explaining why the typical misconception is incorrect...",
      "concept_tested": "Specific remedial concept"
    }}
  ]
}}
"""
        return {
            "technique": "Adaptive Prompting (Performance-Conditioned Remediation)",
            "system_prompt": system_prompt,
            "user_prompt": user_prompt
        }
