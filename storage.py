"""Loading and saving student data (JSON)."""
import json
import os

from student import Student

DATA_FILE = os.path.join("data", "students.json")


def load_students(path=DATA_FILE):
    """Load students from JSON. Returns [] if the file is missing or damaged."""
    students = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError:
        print("No data file found yet - starting with an empty system.")
    except json.JSONDecodeError:
        print("Warning: data file is corrupted. Starting empty.")
    else:
        students = [Student.from_dict(item) for item in raw]
        print(f"Loaded {len(students)} student(s) from {path}.")
    return students


def save_students(students, path=DATA_FILE):
    """Save all students to JSON. Returns True on success."""
    try:
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in students], f, indent=4)
        return True
    except OSError as err:
        print(f"Could not save data: {err}")
        return False
    finally:
        pass  # nothing to clean up: 'with' already closed the file
