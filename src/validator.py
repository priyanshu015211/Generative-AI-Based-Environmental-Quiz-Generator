"""Lightweight structural checks for the local question bank."""


def validate_questions(questions):
    valid = []
    seen = set()
    issues = 0
    required = ("topic", "type", "difficulty", "question", "answer")

    for question in questions:
        if not isinstance(question, dict) or any(
            not isinstance(question.get(key), str) or not question[key].strip()
            for key in required
        ):
            issues += 1
            continue

        normalized_question = question["question"].strip().casefold()
        if normalized_question in seen:
            issues += 1
            continue

        options = question.get("options", [])
        if not isinstance(options, list):
            issues += 1
            continue

        if question["type"] == "True/False":
            if question["answer"] not in {"True", "False"}:
                issues += 1
                continue
        elif len(options) < 2 or question["answer"] not in options:
            issues += 1
            continue

        seen.add(normalized_question)
        question.setdefault("explanation", "No explanation supplied.")
        valid.append(question)

    return valid, issues
