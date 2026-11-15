"""Report generation: report cards, class lists, statistics, file export."""
import csv
import os
from datetime import datetime

import results

REPORT_DIR = "reports"


def report_card(student):
    avg = results.average(student)
    grade, remark = results.grade_for(avg)
    line = "=" * 46
    out = [line, "NEW HORIZON - STUDENT REPORT CARD".center(46), line,
           f"Name     : {student.name}",
           f"ID       : {student.student_id}",
           f"Class    : {student.class_name}",
           f"Gender   : {student.gender}",
           f"DOB      : {student.dob}", "-" * 46]
    if not student.has_scores():
        out.append("No scores recorded yet.")
    else:
        for subject, score in student.scores.items():
            out.append(f"{subject:<20}{score:>8.1f}")
        out += ["-" * 46,
                f"{'Total':<20}{results.total(student):>8.1f}",
                f"{'Average':<20}{avg:>8.2f}",
                f"{'Grade':<20}{grade:>8}  ({remark})",
                f"Result entered: {student.date_entered}"]
    out.append(line)
    return "\n".join(out)


def sort_students(students, by="average"):
    """Sort by average (highest first) or by name (A-Z)."""
    if by == "name":
        return sorted(students, key=lambda s: s.name.lower())
    return sorted(students, key=results.average, reverse=True)


def class_list(students, by="average"):
    rows = [f"{'Pos':<5}{'ID':<14}{'Name':<24}{'Total':>8}{'Avg':>8}{'Grade':>7}",
            "-" * 66]
    for pos, s in enumerate(sort_students(students, by), start=1):
        avg = results.average(s)
        rows.append(f"{pos:<5}{s.student_id:<14}{s.name:<24}"
                    f"{results.total(s):>8.1f}{avg:>8.2f}{results.grade_for(avg)[0]:>7}")
    return "\n".join(rows)


def statistics_text(students):
    stats = results.class_statistics(students)
    if stats is None:
        return "No scores recorded yet - no statistics available."
    hi, lo = stats["highest"], stats["lowest"]
    return "\n".join([
        "CLASS STATISTICS", "-" * 40,
        f"Students with results : {stats['count']}",
        f"Highest score         : {hi[0]:.1f} ({hi[1]}, {hi[2]})",
        f"Lowest score          : {lo[0]:.1f} ({lo[1]}, {lo[2]})",
        f"Class average         : {stats['class_average']:.2f}",
        f"Top student           : {stats['top_student'].name} "
        f"({results.average(stats['top_student']):.2f})"])


def save_text_report(students):
    """Write the full class report to reports/ and return the file path."""
    os.makedirs(REPORT_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(REPORT_DIR, f"class_report_{stamp}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("NEW HORIZON - CLASS RESULT REPORT\n")
        f.write(f"Generated: {datetime.now():%Y-%m-%d %H:%M}\n\n")
        f.write(class_list(students) + "\n\n")
        f.write(statistics_text(students) + "\n")
    return path


def export_csv(students):
    os.makedirs(REPORT_DIR, exist_ok=True)
    path = os.path.join(REPORT_DIR, "results.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Class"] + results.SUBJECTS +
                        ["Total", "Average", "Grade"])
        for s in sort_students(students):
            avg = results.average(s)
            writer.writerow([s.student_id, s.name, s.class_name] +
                            [s.scores.get(sub, "") for sub in results.SUBJECTS] +
                            [results.total(s), round(avg, 2), results.grade_for(avg)[0]])
    return path
