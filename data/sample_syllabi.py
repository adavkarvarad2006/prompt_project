"""
ExamForge AI - Curated Academic Syllabi
Pre-populated with Course: Prompt Engineering (matching the project proposal)
and standard technical curricula.
"""
from core.models import Syllabus, SyllabusUnit, Topic

SAMPLE_PROMPT_ENGINEERING_SYLLABUS = Syllabus(
    syllabus_id="SYLL-PE-2024",
    subject_name="Prompt Engineering and Generative AI",
    course_code="PE-302",
    department="Computer Science and Artificial Intelligence",
    target_audience="Undergraduate & Postgraduate Engineering Students",
    units=[
        SyllabusUnit(
            unit_number=1,
            title="Foundations of Prompt Engineering and LLM Architectures",
            description="Fundamental principles of autoregressive generation, tokenization, context windows, and instruction tuning.",
            topics=[
                Topic(
                    topic_id="T1.1",
                    title="Prompt Anatomy and Instruction Tuning",
                    subtopics=["System vs User vs Assistant roles", "Context boundaries", "Delimiters and XML tags"],
                    learning_objectives=["Identify components of an effective prompt", "Apply structural delimiters to avoid prompt injection"]
                ),
                Topic(
                    topic_id="T1.2",
                    title="Decoding Parameters and Variance Control",
                    subtopics=["Temperature vs Top-P sampling", "Frequency and Presence penalties", "Logit bias"],
                    learning_objectives=["Explain how temperature alters output entropy", "Tune sampling parameters for deterministic vs creative tasks"]
                ),
                Topic(
                    topic_id="T1.3",
                    title="Zero-Shot vs Few-Shot In-Context Learning",
                    subtopics=["Task demonstrations", "Majority-class bias", "Exemplar ordering effects"],
                    learning_objectives=["Formulate zero-shot and few-shot prompts", "Analyze the impact of biased demonstrations"]
                )
            ]
        ),
        SyllabusUnit(
            unit_number=2,
            title="Advanced Prompting Paradigms and Structured Outputs",
            description="Reasoning scaffolds, reasoning token allocation, output constraint validation, and meta-prompting.",
            topics=[
                Topic(
                    topic_id="T2.1",
                    title="Chain-of-Thought (CoT) and Least-to-Most Prompting",
                    subtopics=["Manual CoT", "Zero-Shot CoT ('Let's think step by step')", "Sub-problem decomposition"],
                    learning_objectives=["Apply Chain-of-Thought for arithmetic and symbolic tasks", "Contrast direct answer extraction with reasoning traces"]
                ),
                Topic(
                    topic_id="T2.2",
                    title="Structured Output Generation and Schema Enforcement",
                    subtopics=["JSON schema prompting", "Pydantic validation", "Grammar-constrained sampling"],
                    learning_objectives=["Construct prompts yielding strictly validated JSON", "Design error recovery loops for malformed LLM responses"]
                ),
                Topic(
                    topic_id="T2.3",
                    title="Role-Based and Persona-Conditioned Prompting",
                    subtopics=["Domain expert framing", "Tone calibration", "Audience-adapted explanations"],
                    learning_objectives=["Implement cognitive persona prompts", "Evaluate the pedagogical impact of Socratic vs direct roles"]
                )
            ]
        ),
        SyllabusUnit(
            unit_number=3,
            title="Prompt Evaluation, Self-Consistency, and Defensive Prompting",
            description="Verification mechanisms, hallucination mitigation, defensive engineering, and automated evaluation.",
            topics=[
                Topic(
                    topic_id="T3.1",
                    title="Self-Consistency, Verification, and Meta-Prompting",
                    subtopics=["Self-reflection passes", "Majority voting across paths", "Automated rubric grading"],
                    learning_objectives=["Implement self-check prompts that verify outputs before finalizing", "Design dual-pass verification workflows"]
                ),
                Topic(
                    topic_id="T3.2",
                    title="Hallucination Mitigation and Grounding",
                    subtopics=["Closed-domain constraints", "Explicit refusal triggers ('If unknown, say...')", "Citation extraction"],
                    learning_objectives=["Formulate prompts that strictly constrain model responses to provided context documents", "Audit outputs for ungrounded claims"]
                ),
                Topic(
                    topic_id="T3.3",
                    title="Adaptive Learning and Dynamic Context Injection",
                    subtopics=["Performance-conditioned prompts", "Socratic diagnostic remediation", "Learner profile injection"],
                    learning_objectives=["Synthesize student diagnostic profiles into targeted remedial prompts", "Build dual-adaptive educational feedback loops"]
                )
            ]
        )
    ]
)

SAMPLE_DSA_SYLLABUS = Syllabus(
    syllabus_id="SYLL-CS-201",
    subject_name="Data Structures and Algorithms",
    course_code="CS-201",
    department="Computer Science and Engineering",
    target_audience="2nd Year B.Tech Students",
    units=[
        SyllabusUnit(
            unit_number=1,
            title="Linear Data Structures and Complexity Analysis",
            description="Arrays, Linked Lists, Stacks, Queues, and Asymptotic Notations.",
            topics=[
                Topic(
                    topic_id="DSA1.1",
                    title="Asymptotic Notations and Recurrences",
                    subtopics=["Big-O, Omega, Theta", "Master Theorem", "Space-Time Tradeoffs"],
                    learning_objectives=["Analyze algorithmic time complexity", "Solve divide-and-conquer recurrence relations"]
                ),
                Topic(
                    topic_id="DSA1.2",
                    title="Stacks, Queues, and Expression Evaluation",
                    subtopics=["Infix to Postfix", "Monotonic Stack", "Circular Queue"],
                    learning_objectives=["Apply stacks for syntax parsing", "Implement queue buffers"]
                )
            ]
        ),
        SyllabusUnit(
            unit_number=2,
            title="Non-Linear Structures: Trees and Graphs",
            description="Binary Search Trees, AVL Trees, Heaps, Graph Traversals, and Shortest Paths.",
            topics=[
                Topic(
                    topic_id="DSA2.1",
                    title="Binary Search Trees and Balanced Trees",
                    subtopics=["BST properties", "AVL rotations", "Heapify and Priority Queues"],
                    learning_objectives=["Perform tree balance operations", "Design priority schedulers with heaps"]
                ),
                Topic(
                    topic_id="DSA2.2",
                    title="Graph Algorithms",
                    subtopics=["BFS/DFS", "Dijkstra's Algorithm", "Minimum Spanning Trees (Kruskal/Prim)"],
                    learning_objectives=["Model real-world networks with graphs", "Compute shortest paths in weighted graphs"]
                )
            ]
        )
    ]
)
