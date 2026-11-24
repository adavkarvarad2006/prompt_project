"""
ExamForge AI - UI Styling, Themes, and Visual Component Utilities
"""
import streamlit as st
import pandas as pd
import json

CUSTOM_CSS = """
<style>
/* Clean Academic Header and Modern Typography */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

code, pre {
    font-family: 'JetBrains Mono', monospace !important;
}

.main-header {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border: 1px solid #334155;
    padding: 24px 28px;
    border-radius: 12px;
    margin-bottom: 24px;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
}

.main-header h1 {
    color: #f8fafc !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
    margin: 0 0 6px 0 !important;
    padding: 0 !important;
    letter-spacing: -0.5px;
}

.main-header p {
    color: #94a3b8 !important;
    font-size: 1rem !important;
    margin: 0 !important;
    padding: 0 !important;
}

.badge-tag {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-right: 6px;
    margin-bottom: 6px;
}

/* Badges that work seamlessly in both Light and Dark modes */
.badge-tag {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-right: 6px;
    margin-bottom: 6px;
}

.badge-blue { background-color: rgba(59, 130, 246, 0.15); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.35); }
.badge-green { background-color: rgba(34, 197, 94, 0.15); color: #22c55e; border: 1px solid rgba(34, 197, 94, 0.35); }
.badge-amber { background-color: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.35); }
.badge-purple { background-color: rgba(168, 85, 247, 0.15); color: #a855f7; border: 1px solid rgba(168, 85, 247, 0.35); }
.badge-rose { background-color: rgba(244, 63, 94, 0.15); color: #f43f5e; border: 1px solid rgba(244, 63, 94, 0.35); }

.card-box {
    background-color: var(--secondary-background-color, #ffffff);
    color: var(--text-color, #1e293b);
    border: 1px solid rgba(128, 128, 128, 0.25);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.04);
}

.prompt-box {
    background-color: #0f172a;
    color: #f8fafc;
    border-radius: 10px;
    padding: 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    overflow-x: auto;
    border: 1px solid #334155;
}

.stat-tile {
    text-align: center;
    padding: 16px;
    border-radius: 10px;
    background-color: var(--secondary-background-color, #f8fafc);
    color: var(--text-color, #1e293b);
    border: 1px solid rgba(128, 128, 128, 0.25);
}
.stat-number {
    font-size: 1.8rem;
    font-weight: 700;
    color: #3b82f6;
}
.stat-label {
    font-size: 0.85rem;
    color: var(--text-color, #64748b);
    opacity: 0.85;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
</style>
"""

def render_header(title: str, subtitle: str, badge: str = None):
    st.markdown(CUSTOM_CSS.strip(), unsafe_allow_html=True)
    badge_html = f'<div style="margin-bottom: 8px;"><span class="badge-tag badge-amber">{badge}</span></div>' if badge else ""
    header_html = f'<div class="main-header">{badge_html}<h1>{title}</h1><p>{subtitle}</p></div>'
    st.markdown(header_html, unsafe_allow_html=True)

def render_stat_row(stats: list):
    cols = st.columns(len(stats))
    for col, (num, label) in zip(cols, stats):
        with col:
            tile_html = f'<div class="stat-tile"><div class="stat-number">{num}</div><div class="stat-label">{label}</div></div>'
            st.markdown(tile_html, unsafe_allow_html=True)

def generate_printable_html(paper) -> str:
    """Generates clean, printable HTML for the question paper with marking scheme."""
    q_html = ""
    for idx, q in enumerate(paper.questions, 1):
        options_html = ""
        if q.options:
            options_html = "<div style='margin-left: 20px; margin-top: 8px;'>" + "".join([f"<p style='margin: 4px 0;'>{opt}</p>" for opt in q.options]) + "</div>"
        
        marking_html = ""
        if q.marking_scheme:
            steps = "".join([f"<li>{s.step_description} — <strong>[{s.marks_awarded} M]</strong></li>" for s in q.marking_scheme])
            marking_html = f"<div style='background: #f1f5f9; padding: 10px 14px; border-radius: 6px; margin-top: 8px; font-size: 13px;'><strong>Marking Scheme:</strong><ul style='margin: 4px 0 0 18px;'>{steps}</ul></div>"

        q_html += f"""
        <div style='margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #e2e8f0;'>
            <div style='display: flex; justify-content: space-between;'>
                <strong>Q{idx}. [{q.marks} Marks] ({q.blooms_level})</strong>
                <span style='color: #64748b; font-size: 13px;'>Unit {q.unit_number} | {q.topic_name}</span>
            </div>
            <p style='margin-top: 8px; font-size: 15px;'>{q.question_text}</p>
            {options_html}
            <div style='margin-top: 8px; font-size: 13.5px; color: #1e3a8a;'>
                <strong>Model Answer / Solution:</strong> {q.model_answer}
            </div>
            {marking_html}
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{paper.title}</title>
        <style>
            body {{ font-family: 'Times New Roman', Times, serif; margin: 40px; color: #111827; }}
            .paper-head {{ text-align: center; border-bottom: 2px solid #000; padding-bottom: 12px; margin-bottom: 20px; }}
            .meta-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 14px; }}
            .meta-table td {{ padding: 4px 0; }}
            .instructions {{ background: #f8fafc; border: 1px solid #cbd5e1; padding: 12px; font-size: 13px; margin-bottom: 24px; }}
        </style>
    </head>
    <body>
        <div class="paper-head">
            <h2 style="margin: 0; text-transform: uppercase;">{paper.course_name}</h2>
            <h3 style="margin: 6px 0;">{paper.title}</h3>
            <p style="margin: 0; font-size: 14px;">ExamForge AI Dual-Adaptive Intelligent Examination Platform</p>
        </div>
        <table class="meta-table">
            <tr>
                <td><strong>Max Marks:</strong> {paper.total_marks}</td>
                <td style="text-align: right;"><strong>Duration:</strong> {paper.duration_minutes} Minutes</td>
            </tr>
            <tr>
                <td><strong>Status:</strong> {paper.status}</td>
                <td style="text-align: right;"><strong>Paper ID:</strong> {paper.paper_id}</td>
            </tr>
        </table>
        <div class="instructions">
            <strong>General Instructions:</strong>
            <ul style="margin: 4px 0 0 16px;">
                {"".join([f"<li>{ins}</li>" for ins in paper.instructions])}
            </ul>
        </div>
        <h3>SECTION: ASSESSMENT QUESTIONS & SCHEMES</h3>
        {q_html}
    </body>
    </html>
    """
    return html

def generate_markdown_export(paper) -> str:
    """Generates markdown export string."""
    lines = [
        f"# {paper.course_name}",
        f"## {paper.title}",
        f"**Paper ID:** `{paper.paper_id}` | **Total Marks:** {paper.total_marks} | **Duration:** {paper.duration_minutes} Mins",
        "",
        "### Instructions:",
        *[f"- {i}" for i in paper.instructions],
        "",
        "---",
        "### Questions & Marking Schemes",
        ""
    ]
    for idx, q in enumerate(paper.questions, 1):
        lines.append(f"#### Q{idx}. ({q.marks} Marks) [{q.blooms_level} | {q.difficulty}]")
        lines.append(f"**Topic:** Unit {q.unit_number}: {q.topic_name}")
        lines.append(f"\n{q.question_text}\n")
        if q.options:
            for opt in q.options:
                lines.append(f"- {opt}")
            lines.append(f"\n**Correct Option:** `{q.correct_option}`")
        lines.append(f"\n**Model Solution:**\n{q.model_answer}\n")
        if q.marking_scheme:
            lines.append("**Marking Scheme:**")
            for s in q.marking_scheme:
                lines.append(f"- {s.step_description} (`{s.marks_awarded} M`)")
        lines.append(f"\n*Pedagogical Explanation:* {q.explanation}")
        lines.append("\n---\n")
    return "\n".join(lines)
