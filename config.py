"""
ExamForge AI - Global Configuration & System Metadata
"""

APP_NAME = "ExamForge AI"
APP_SUBTITLE = "A Dual-Adaptive Intelligent Examination and Personalized Learning Platform Using Prompt Engineering"
APP_VERSION = "1.0.0"
COURSE_NAME = "Prompt Engineering"
COMPONENT_MARKS = "20 Marks Component"

# Default blueprint defaults
DEFAULT_EXAM_MARKS = 25.0
DEFAULT_EXAM_DURATION = 45
DEFAULT_PASSING_PERCENTAGE = 60.0
MASTERY_THRESHOLD_PERCENTAGE = 75.0

# Supported LLM models
SUPPORTED_GEMINI_MODELS = [
    "gemini-3-flash-preview",
    "gemini-3.8-flash",
    "gemini-3.1-flash-lite-preview"
]

SUPPORTED_OPENAI_MODELS = [
    "gpt-4o-mini",
    "gpt-4o",
    "llama-3.3-70b-versatile"
]
