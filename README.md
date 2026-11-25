# AccuKnox Django Trainee Technical Assignment

A clean, comprehensive Django project implementing and proving the technical questions for the AccuKnox Django Trainee assessment.

---

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [How to Run & Verify](#how-to-run--verify)
  - [1. Django Signals Demo](#1-django-signals-demo)
  - [2. Custom Rectangle Class Demo](#2-custom-rectangle-class-demo)
  - [3. Automated Unit Tests](#3-automated-unit-tests)
- [Summary of Answers](#summary-of-answers)
  - [Topic 1: Django Signals](#topic-1-django-signals)
  - [Topic 2: Custom Classes in Python (`Rectangle`)](#topic-2-custom-classes-in-python-rectangle)

---

## Overview

This repository contains clean, modular, and fully tested implementations for both parts of the technical assignment:
1. **Topic 1: Django Signals**: Conclusive empirical demonstrations and unit tests answering the 3 core questions regarding synchronicity, threading, and database transaction boundaries.
2. **Topic 2: Custom Python Classes**: A robust `Rectangle` class implementing iterable dimensions (`__iter__`), strict type validation (disallowing non-integers and booleans), and supporting multiple iterations cleanly.

---

## Project Structure

```text
AccuKnox/
│
├── accuknox_assignment/             # Django project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                  # Project settings (core registered in INSTALLED_APPS)
│   ├── urls.py
│   └── wsgi.py
│
├── core/                            # Core Django application
│   ├── management/
│   │   └── commands/
│   │       ├── run_rectangle_demo.py  # Management command: Rectangle demo
│   │       └── run_signals_demo.py    # Management command: Signals demo (Q1, Q2, Q3)
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── apps.py                      # AppConfig connecting signals in ready()
│   ├── models.py                    # SignalTestModel and SignalLog
│   ├── rectangle.py                 # Custom Rectangle class with __iter__
│   ├── signals.py                   # post_save signal receivers for Q1, Q2, Q3
│   └── tests.py                     # 9 automated unit tests for Topic 1 and Topic 2
│
├── .gitignore                       # Git ignore rules (venv, db.sqlite3, cache, etc.)
├── manage.py                        # Django management script
├── README.md                        # Documentation and verification guide
└── requirements.txt                 # Project dependencies
```

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd AccuKnox
```

### 2. Create and Activate Virtual Environment
- **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

---

## How to Run & Verify

### 1. Django Signals Demo
Executes 3 sequential demonstrations proving synchronicity, thread identity, and transaction rollback:
```bash
python manage.py run_signals_demo
```

### 2. Custom Rectangle Class Demo
Demonstrates initializing `Rectangle(10, 5)`, looping through it twice, and list conversion:
```bash
python manage.py run_rectangle_demo
```

### 3. Automated Unit Tests
Runs the full automated test suite (9 test cases covering signals and rectangle):
```bash
python manage.py test
```

---

## Summary of Answers

### Topic 1: Django Signals

#### Question 1: Are Django signals executed synchronously or asynchronously by default?
- **Answer:** **Synchronously.**
- **Proof:**
  - Inside `question_1_sync_handler` in `core/signals.py`, a `time.sleep(2)` delay is introduced during `post_save`.
  - In `run_signals_demo.py` and `test_question_1_signals_execute_synchronously`, the caller records start time before `save()` and end time after `save()` completes.
  - The caller blocks and waits for $\ge 2.0\text{ seconds}$ before resuming execution, proving synchronous execution.

#### Question 2: Do Django signals run in the same thread as the caller?
- **Answer:** **Yes, in the same thread.**
- **Proof:**
  - In `question_2_thread_handler`, the signal receiver logs `threading.get_ident()` and `threading.current_thread().name`.
  - In `run_signals_demo.py` and `test_question_2_signals_run_in_same_thread`, the caller's thread ID and thread name match the signal receiver's thread ID and thread name identically (`MainThread`).

#### Question 3: By default, do Django signals run in the same database transaction as the caller?
- **Answer:** **Yes, in the same database transaction.**
- **Proof:**
  - In `question_3_transaction_handler`, whenever `SignalTestModel` is saved, the receiver creates a `SignalLog` entry in the database.
  - In `run_signals_demo.py` and `test_question_3_signals_run_in_same_database_transaction`, `SignalTestModel.objects.create(...)` is executed inside a `with transaction.atomic():` block, followed immediately by an intentional exception (`raise RuntimeError`).
  - Outside the atomic block, a database query verifies the count of `SignalTestModel` and `SignalLog`. Both counts are `0`, proving that records created by the signal handler reside in the caller's transaction and roll back along with it.

---

### Topic 2: Custom Classes in Python (`Rectangle`)

- **Class Definition (`core/rectangle.py`)**:
  - Initialized with `Rectangle(length: int, width: int)`.
  - Enforces strict integer types using `type(...) is not int`, raising a `TypeError` for floats, strings, and booleans (since in Python, `bool` inherits from `int`).
  - Implements `__iter__(self)` using generator `yield` statements, yielding `{'length': self.length}` first and `{'width': self.width}` second.
  - Supports repeated iterations over the same instance without exhausting state.

- **Sample Output**:
  ```python
  rect = Rectangle(10, 5)

  for item in rect:
      print(item)

  # Output:
  # {'length': 10}
  # {'width': 5}
  ```
