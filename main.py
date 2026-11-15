"""Student Result Management System - entry point and menu."""
import reports
import results
import storage
from student import Student, GENDERS, valid_dob, valid_student_id


def find_by_id(students, student_id):
    for s in students:
        if s.student_id.lower() == student_id.lower():
            return s
    return None


def ask(prompt, validator=None, error="Invalid input."):
    """Keep asking until the input is non-empty and passes the validator."""
    while True:
        value = input(prompt).strip()
        if value and (validator is None or validator(value)):
            return value
        print(error)


def add_student(students):
    sid = ask("Student ID (e.g. NH/2026/001): ", valid_student_id,
              "Format must be NH/YYYY/NNN, e.g. NH/2026/001.").upper()
    if find_by_id(students, sid):
        print("A student with that ID already exists.")
        return
    name = ask("Full name: ").title()
    class_name = ask("Class/Form (e.g. SS2): ").upper()
    gender = ask("Gender (Male/Female): ", lambda g: g.title() in GENDERS,
                 "Enter Male or Female.").title()
    dob = ask("Date of birth (YYYY-MM-DD): ", valid_dob,
              "Use a real date in YYYY-MM-DD format.")
    students.append(Student(sid, name, class_name, gender, dob))
    print(f"Student {name} added.")


def view_students(students):
    if not students:
        print("No students registered.")
        return
    print(f"{'ID':<13} {'Name':<24} {'Class':<8} {'Gender':<7} DOB")
    print("-" * 64)
    for s in students:
        print(s)


def search_student(students):
    term = input("Enter student ID or name: ").strip().lower()
    matches = [s for s in students
               if term == s.student_id.lower() or term in s.name.lower()]
    if matches:
        for s in matches:
            print(s)
    else:
        print("No match found.")


def pick_student(students):
    s = find_by_id(students, input("Student ID: ").strip())
    if s is None:
        print("Student not found.")
    return s


def update_student(students):
    s = pick_student(students)
    if not s:
        return
    print("Press Enter to keep the current value.")
    s.name = input(f"Name [{s.name}]: ").strip().title() or s.name
    s.class_name = input(f"Class [{s.class_name}]: ").strip().upper() or s.class_name
    g = input(f"Gender [{s.gender}]: ").strip().title()
    if g in GENDERS:
        s.gender = g
    d = input(f"DOB [{s.dob}]: ").strip()
    if d and valid_dob(d):
        s.dob = d
    elif d:
        print("Invalid date ignored.")
    print("Student updated.")


def delete_student(students):
    s = pick_student(students)
    if s and input(f"Delete {s.name}? (y/n): ").strip().lower() == "y":
        students.remove(s)
        print("Student deleted.")


def record_scores(students):
    s = pick_student(students)
    if not s:
        return
    new_scores = {}
    for subject in results.SUBJECTS:
        while True:
            try:
                new_scores[subject] = results.valid_score(
                    input(f"{subject} score (0-100): "))
            except ValueError as err:
                print(f"Invalid: {err if 'between' in str(err) else 'enter a number.'}")
            else:
                break
    results.set_scores(s, new_scores)
    print("Scores saved.")


def update_score(students):
    s = pick_student(students)
    if not s:
        return
    if not s.has_scores():
        print("No scores yet - use 'Record scores' first.")
        return
    for i, sub in enumerate(results.SUBJECTS, 1):
        print(f"{i}. {sub} ({s.scores[sub]})")
    try:
        sub = results.SUBJECTS[int(input("Subject number: ")) - 1]
        s.scores[sub] = results.valid_score(input("New score: "))
    except (ValueError, IndexError) as err:
        print(f"Invalid entry: {err}")
    else:
        results.set_scores(s, s.scores)
        print("Score updated.")


def show_report_card(students):
    s = pick_student(students)
    if s:
        print(reports.report_card(s))


def list_results(students):
    if not students:
        print("No students registered.")
        return
    by = "name" if input("Sort by (1) average or (2) name? ").strip() == "2" else "average"
    print(reports.class_list(students, by))


def main():
    students = storage.load_students()
    actions = {
        "1": ("Add student", add_student),
        "2": ("View all students", view_students),
        "3": ("Search student", search_student),
        "4": ("Update student", update_student),
        "5": ("Delete student", delete_student),
        "6": ("Record scores", record_scores),
        "7": ("Update a score", update_score),
        "8": ("Show report card", show_report_card),
        "9": ("List results (sorted)", list_results),
        "10": ("Class statistics", lambda s: print(reports.statistics_text(s))),
        "11": ("Save text report to file",
               lambda s: print("Saved:", reports.save_text_report(s))),
        "12": ("Export results to CSV",
               lambda s: print("Saved:", reports.export_csv(s))),
    }
    while True:
        print("\n===== STUDENT RESULT MANAGEMENT SYSTEM =====")
        for key, (label, _) in actions.items():
            print(f"{key:>2}. {label}")
        print(" 0. Save and exit")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            if storage.save_students(students):
                print("Data saved. Goodbye!")
            break
        if choice in actions:
            actions[choice][1](students)
            storage.save_students(students)   # auto-save after every action
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
