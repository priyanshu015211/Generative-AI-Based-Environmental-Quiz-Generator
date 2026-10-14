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


def get_quiz(topic, preferred_level="Easy", count=3, questions=None, rng=None):
    """Pick quiz items for a topic, preferring the requested difficulty.

    This is static question-bank selection, not generative-AI question creation.
    If a topic has too few items at one level, remaining questions from that topic
    are used to ensure a useful demo quiz.
    """
    source = load_questions() if questions is None else list(questions)
    randomizer = rng or random
    topic_items = [q for q in source if q.get("topic") == topic]
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
