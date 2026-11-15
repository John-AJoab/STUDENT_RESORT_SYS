"""Student class and input validation helpers."""
import re
from datetime import datetime

ID_PATTERN = re.compile(r"^NH/\d{4}/\d{3}$")   # e.g. NH/2026/001
GENDERS = ("Male", "Female")


def valid_student_id(student_id):
    """Return True if the ID matches the format NH/YYYY/NNN."""
    return bool(ID_PATTERN.match(student_id))


def valid_dob(dob):
    """Return True if dob is a real date in YYYY-MM-DD format."""
    try:
        datetime.strptime(dob, "%Y-%m-%d")
        return True
    except ValueError:
        return False


class Student:
    """Holds one student's details and subject scores."""

    def __init__(self, student_id, name, class_name, gender, dob,
                 scores=None, date_entered=None):
        self.student_id = student_id
        self.name = name
        self.class_name = class_name
        self.gender = gender
        self.dob = dob
        self.scores = scores if scores is not None else {}   # {subject: score}
        self.date_entered = date_entered                      # when scores were recorded

    def has_scores(self):
        return len(self.scores) > 0

    def to_dict(self):
        return {
            "student_id": self.student_id, "name": self.name,
            "class_name": self.class_name, "gender": self.gender,
            "dob": self.dob, "scores": self.scores,
            "date_entered": self.date_entered,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["student_id"], data["name"], data["class_name"],
                   data["gender"], data["dob"], data.get("scores", {}),
                   data.get("date_entered"))

    def __str__(self):
        return (f"{self.student_id:<13} {self.name:<24} {self.class_name:<8} "
                f"{self.gender:<7} {self.dob}")
