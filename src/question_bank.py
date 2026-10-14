"""Question selection from the project's prepared local sample bank."""
import json
import random
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "questions.json"


def load_questions():
    with DATA_PATH.open("r", encoding="utf-8") as file:
        questions = json.load(file)
    if not isinstance(questions, list):
        raise ValueError("Question bank must contain a JSON list.")
    return questions


def get_quiz(topic, preferred_level="Easy", count=3, questions=None, rng=None, question_type=None):
    """Pick questions for one topic and, optionally, one format.

    Questions at the preferred difficulty are selected first; other difficulty
    levels from the same topic and format fill the remaining requested slots.
    This is static question-bank selection, not generative-AI question creation.
    """
    source = load_questions() if questions is None else list(questions)
    randomizer = rng or random
    topic_items = [q for q in source if q.get("topic") == topic]
    if question_type is not None:
        topic_items = [q for q in topic_items if q.get("type") == question_type]
    if not topic_items:
        return []
    preferred = [q for q in topic_items if q.get("difficulty") == preferred_level]
    other = [q for q in topic_items if q.get("difficulty") != preferred_level]
    randomizer.shuffle(preferred)
    randomizer.shuffle(other)
    selected = preferred[:count]
    if len(selected) < count:
        selected.extend(other[: count - len(selected)])
    return selected
