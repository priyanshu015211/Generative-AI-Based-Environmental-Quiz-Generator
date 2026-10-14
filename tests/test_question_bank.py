from src.question_bank import get_quiz
from src.validator import validate_questions


def sample_items():
    return [
        {"topic": "Climate Change", "type": "MCQ", "difficulty": "Easy", "question": "Which gas?", "options": ["CO2", "O2"], "answer": "CO2"},
        {"topic": "Climate Change", "type": "MCQ", "difficulty": "Hard", "question": "What reduces emissions?", "options": ["Efficiency", "Waste"], "answer": "Efficiency"},
        {"topic": "Biodiversity", "type": "True/False", "difficulty": "Easy", "question": "Life varies across ecosystems.", "options": [], "answer": "True"},
    ]


def test_get_quiz_filters_by_topic_and_count():
    selected = get_quiz("Climate Change", "Easy", 2, questions=sample_items())
    assert len(selected) == 2
    assert all(item["topic"] == "Climate Change" for item in selected)


def test_preferred_difficulty_is_selected_first():
    selected = get_quiz("Climate Change", "Hard", 1, questions=sample_items())
    assert selected[0]["difficulty"] == "Hard"


def test_validator_filters_duplicate_and_keeps_valid_question():
    item = sample_items()[0]
    valid, issues = validate_questions([item, item])
    assert len(valid) == 1
    assert issues == 1


def test_validator_rejects_invalid_mcq_answer():
    item = sample_items()[0].copy()
    item["answer"] = "Not an option"
    valid, issues = validate_questions([item])
    assert valid == []
    assert issues == 1
