# Student Result Management System

A menu-driven Python application for New Horizon that registers students,
records scores, calculates grades and generates reports.

**Author:** Akinlamilo John Oliwarantimi
**Matric No:** 24/Sci01/025
**Department:** Computer Science
**Course:** Introduction to Python Programming

## Features
- Add, view, search, update and delete students
- Record scores for 5 subjects (Mathematics, English, Physics, Chemistry, Biology)
- Total, average and grade (A-F) with the date each result was entered
- Individual report cards
- Class list sorted by average or name, with class statistics
- Save a text report and export results to CSV
- Data saved automatically to `data/students.json` and loaded on startup

## Grading scale
| Average | Grade |
|---|---|
| 70-100 | A |
| 60-69 | B |
| 50-59 | C |
| 45-49 | D |
| 0-44 | F |

## How to run
1. Install Python 3.8 or newer.
2. Clone or download this repository.
3. In a terminal, open the project folder and run:
   ```
   python main.py
   ```
Student IDs use the format `NH/YYYY/NNN` (e.g. `NH/2026/001`). Dates use `YYYY-MM-DD`.

## Project structure
```
main.py      # entry point and menu
student.py   # Student class and validation (regex, dates)
results.py   # score calculation and grading
storage.py   # load/save JSON
reports.py   # report cards, lists, statistics, file export
data/        # students.json (created automatically)
reports/     # generated reports (created automatically)
```

## Python concepts used
Variables and type conversion, if/elif/else, for and while loops, lists, tuples
and dictionaries, functions, sorting (`sorted` with `key`), exception handling
(try/except/else/finally), JSON and CSV file handling, multiple modules, OOP
(`Student` class), `datetime`, standard library (`os`, `json`, `csv`, `re`,
`datetime`) and regular expressions.
