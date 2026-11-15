"""Score calculation, grading and class statistics."""
from datetime import datetime

SUBJECTS = ["Mathematics", "English", "Physics", "Chemistry", "Biology"]

# (minimum average, grade, remark) - checked from highest to lowest
GRADE_SCALE = [
    (70, "A", "Excellent"),
    (60, "B", "Very Good"),
    (50, "C", "Good"),
    (45, "D", "Pass"),
    (0,  "F", "Fail"),
]


def valid_score(value):
    """Convert text to a float score between 0 and 100. Raises ValueError."""
    score = float(value)
    if not 0 <= score <= 100:
        raise ValueError("Score must be between 0 and 100.")
    return score


def set_scores(student, scores):
    """Store scores on a student and stamp the date they were entered."""
    student.scores = scores
    student.date_entered = datetime.now().strftime("%Y-%m-%d %H:%M")


def total(student):
    return sum(student.scores.values())


def average(student):
    if not student.scores:
        return 0.0
    return total(student) / len(student.scores)


def grade_for(avg):
    """Return (grade, remark) for an average score."""
    for minimum, grade, remark in GRADE_SCALE:
        if avg >= minimum:
            return grade, remark
    return "F", "Fail"


def class_statistics(students):
    """Return a dict of class stats for students that have scores, or None."""
    scored = [s for s in students if s.has_scores()]
    if not scored:
        return None
    all_scores = [(sc, sub, s.name) for s in scored for sub, sc in s.scores.items()]
    highest = max(all_scores)
    lowest = min(all_scores)
    averages = [average(s) for s in scored]
    return {
        "count": len(scored),
        "highest": highest,          # (score, subject, student name)
        "lowest": lowest,
        "class_average": sum(averages) / len(averages),
        "top_student": max(scored, key=average),
    }
