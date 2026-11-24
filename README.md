# ExamForge AI ⚡
### A Dual-Adaptive Intelligent Examination and Personalized Learning Platform Using Prompt Engineering

> **Course:** Prompt Engineering (20 Marks Component)  
> **Domain:** Education-Based Applications  
> **Platform:** Python 3.10+ / Streamlit / SQLite / Multi-Provider LLM Integration  

---

## 📖 Executive Summary
**ExamForge AI** is an intelligent, dual-adaptive assessment and learning platform engineered for both educators and students. Rather than acting as a simple, generic quiz maker, ExamForge AI connects two continuous, intelligent feedback loops:
1. **Teacher-Side Assessment Adaptation:** Automatically translates raw syllabus text and pedagogical blueprints (Bloom's Taxonomy, difficulty distribution, and mark allocations) into academically rigorous question papers, complete with step-by-step marking schemes and an AI Self-Check verification audit.
2. **Student-Side Learning Adaptation ("Forge My Path"):** Analyzes student submissions to diagnose topic-level learning gaps and recurring cognitive misconceptions. It dynamically conditions prompt generation on the student's error history to produce progressive, remedial practice challenges.

The entire system is powered by **6 structured Prompt Engineering techniques** explicitly detailed in Section 6 of the project proposal.

---

## 🚀 Key Features

### 🎓 1. Teacher Assessment Studio
- **Syllabus Ingestion & Topic Extraction:** Input raw syllabus outlines or choose from pre-loaded academic curricula (*Prompt Engineering PE-302*, *Data Structures & Algorithms CS-201*). The parser automatically extracts Units, Topics, Subtopics, and Learning Objectives.
- **Assessment Blueprint & Prompt Inspector:** Configure total marks, duration, question format splits (MCQ, Short Answer, Long Answer), difficulty levels (Easy, Medium, Hard), and Bloom's Revised Taxonomy levels (Remember, Understand, Apply, Analyze, Evaluate, Create). Inspect the live, underlying system and contextual prompts before execution.
- **Human-in-the-Loop Review & Approval:** Generated papers are presented as drafts. Teachers can edit question stems, adjust marks, refine model solutions, and inspect the AI Verification Audit before approving the paper for students.
- **Multi-Format Export:** Export approved examination papers to **Print-Ready HTML / PDF**, **Markdown (.md)**, or **JSON**.
- **Class Learning Analytics:** Visualize cohort-wide topic mastery heatmaps, average scores, and common recurring misconceptions across all students.

### 🎒 2. Student Adaptive Learning Portal
- **Interactive Assessment Hub:** Take assigned or self-practice exams with a clean testing interface featuring timers, question status indicators, and clear inputs for both objective and descriptive responses.
- **AI Step-Marking & Misconception Diagnosis:** Descriptive answers are evaluated using step-wise marking rubrics. The system awards partial credit for intermediate reasoning, points out missing key concepts, and highlights root-cause misconceptions.
- **"Forge My Path" Dual-Adaptive Practice:** A single click analyzes the student's weak topics and triggers an **Adaptive Prompt** that generates a tailored remedial practice set with progressive scaffolding.
- **Personal Learning Dashboard:** View topic mastery growth, test score history, and targeted study recommendations.

### 🔬 3. Prompt Engineering Demonstration Laboratory
A dedicated laboratory demonstrating the 6 Prompt Engineering techniques from Section 6 of the proposal:
1. **Role-Based Prompting:** Domain personas (*Senior Academic Examiner*, *Objective Step-Marking Evaluator*, *Socratic Diagnostic Tutor*, *Independent QA Auditor*).
2. **Contextual Prompting:** Injects syllabus units, objectives, and blueprint bounds directly into the context window to prevent hallucinations and topic drift.
3. **Few-Shot Prompting:** In-context exemplars illustrating ideal question phrasing, balanced distractors, and fractional mark rubrics.
4. **Structured Output Prompting:** Enforced JSON schemas ensuring programmatic integrity and seamless UI rendering.
5. **Adaptive Prompting:** Injects student-specific weakness vectors and misconception histories into prompt generation for tailored remediation.
6. **Self-Check / Verification Prompting (Meta-Prompting):** An audit pass verifying that mark totals match, syllabus compliance is satisfied, and no duplicate stems exist.
- **Live Audit Logs:** Inspect real-time logs of every system prompt, user prompt, and model response stored in the local SQLite database.

---

## 🛠️ Architecture & Tech Stack

```
prompt_project/
├── app.py                      # Main Streamlit application and navigation
├── config.py                   # Platform constants & styling
├── requirements.txt            # Minimal dependencies (streamlit, pandas, requests)
├── core/
│   ├── __init__.py
│   ├── models.py               # Data models (Syllabus, Question, Paper, Evaluation)
│   ├── database.py             # SQLite persistence (syllabi, papers, submissions, mastery)
│   ├── prompt_engine.py        # Implementation of the 6 Prompt Engineering techniques
│   ├── llm_client.py           # Multi-provider client (Gemini REST, OpenAI, Offline Engine)
│   ├── syllabus_parser.py      # Syllabus unit/topic extractor
│   ├── evaluator.py            # Step-marking evaluation & misconception diagnosis
│   └── adaptive_engine.py      # Dual-adaptive student recommendation engine
├── data/
│   └── sample_syllabi.py       # Curated course syllabi (PE-302, CS-201)
└── ui/
    ├── __init__.py
    ├── components.py           # UI themes, cards, printable HTML & Markdown exporters
    ├── teacher_portal.py       # Teacher assessment studio & analytics
    ├── student_portal.py       # Student quiz, evaluation & adaptive practice
    ├── prompt_showcase.py      # Interactive Prompt Engineering showcase
    └── documentation_tab.py    # Project proposal view & details
```

### Supported LLM Providers:
- **Offline High-Fidelity Pedagogical Engine (Default):** Zero configuration required. Runs 100% reliably offline without external API keys or network latency, using deterministic prompt evaluation and parsing.
- **Google Gemini API:** Connect via your `GEMINI_API_KEY` (Gemini 2.0 Flash / 1.5 Flash).
- **OpenAI / Groq API:** Connect via standard OpenAI-compatible endpoints (`gpt-4o-mini`, `llama-3.3-70b-versatile`).

---

## 💻 How to Run

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Launch the Application
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 🎯 Verification and Demonstration Checklist

| Feature | Proposal Section | Verification Steps in ExamForge AI |
|---|---|---|
| **Syllabus Analysis** | Section 5 | Open **Teacher Studio > 1. Syllabus & Units**, inspect *Prompt Engineering (PE-302)* or paste a custom curriculum. |
| **Question Paper Generation** | Section 4.1 & 5 | In **2. Blueprint & Prompt Generator**, configure marks and difficulty, inspect live prompts, and click **Generate**. |
| **Self-Check Verification** | Section 4.4 & 6 | In **3. Review & Approve Papers**, view the *AI Verification Audit Report* verifying marks and syllabus compliance. |
| **Human Review & Edit** | Section 3 & 4.4 | Expand any question in Tab 3, edit marks or wording, save changes, and export to **Print-Ready HTML / Markdown**. |
| **Student Assessment** | Section 5 | Switch to **Student Adaptive Portal > 1. Assessment Center**, take an exam, and submit for evaluation. |
| **Step-Marking Feedback** | Section 4.2 | View the instant evaluation with step-marking breakdown and diagnosed misconceptions. |
| **Dual-Adaptive Practice** | Section 4.2 & 6 | Go to **2. Adaptive Remedial Practice**, click **Forge My Adaptive Practice Set Now**, and attempt the personalized quiz. |
| **Shared Class Analytics** | Section 4.3 | Return to **Teacher Studio > 4. Class Learning Analytics** to view class-level mastery and recurring misconceptions. |
| **Prompt Engineering Showcase** | Section 6 | Navigate to **Prompt Engineering Lab** to interactively test all 6 prompt techniques. |

---

## 📝 Academic Submission Note
Developed for the **Prompt Engineering 20 Marks Component**.  
*Domain:* Education-Based Applications  
*Project:* **ExamForge AI - A Dual-Adaptive Intelligent Examination and Personalized Learning Platform Using Prompt Engineering**
