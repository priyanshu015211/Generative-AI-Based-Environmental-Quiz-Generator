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


def test_get_quiz_filters_by_one_question_format():
    selected = get_quiz("Climate Change", "Easy", 1, questions=sample_items(), question_type="MCQ")
    assert len(selected) == 1
    assert all(item["type"] == "MCQ" for item in selected)


def test_get_quiz_can_select_four_or_five_items_from_a_full_format_pool():
    full_pool = [
        {"topic": "Climate Change", "type": "MCQ", "difficulty": "Easy",
         "question": f"Question {i}", "options": ["A", "B"], "answer": "A"}
        for i in range(5)
    ]
    assert len(get_quiz("Climate Change", "Easy", 4, questions=full_pool, question_type="MCQ")) == 4
    assert len(get_quiz("Climate Change", "Easy", 5, questions=full_pool, question_type="MCQ")) == 5


def test_real_question_bank_supports_three_four_and_five_for_every_format():
    from src.question_bank import load_questions

    topics = {item["topic"] for item in load_questions()}
    formats = {"MCQ", "True/False", "Scenario-based"}
    for topic in topics:
        for question_type in formats:
            for count in (3, 4, 5):
                selected = get_quiz(
                    topic, "Easy", count, question_type=question_type
                )
                assert len(selected) == count
                assert all(item["topic"] == topic for item in selected)
                assert all(item["type"] == question_type for item in selected)
