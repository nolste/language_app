from app.db.models.question import Question


def grade_answer(question: Question, submitted: str) -> tuple[float, bool, dict]:
    """
    Returns:
        score (0-1)
        is_correct
        feedback
    """

    correct = (submitted.strip().lower() ==
               question.correct_answer.strip().lower() if question.correct_answer else None)

    if correct:
        return 1.0, True, {"message": "Correct"}

    # simple fallback (MVP partial credit heuristic)
    score = 0.0

    feedback = {
        "message": "Incorrect",
        "expected": question.correct_answer,
    }

    return score, False, feedback
