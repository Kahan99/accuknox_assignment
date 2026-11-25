# AccuKnox Django Trainee Assignment

Project containing solutions for the AccuKnox Django Trainee technical assignment.

## Project Structure

```text
AccuKnox/
├── accuknox_assignment/        # Project settings and urls
├── core/
│   ├── management/commands/
│   │   ├── run_signals_demo.py    # Demo for Topic 1 (Signals)
│   │   └── run_rectangle_demo.py  # Demo for Topic 2 (Rectangle)
│   ├── models.py                  # Models for testing signals
│   ├── signals.py                 # post_save signal handlers
│   ├── rectangle.py               # Custom Rectangle class
│   └── tests.py                   # Automated tests for signals & Rectangle
├── manage.py
├── requirements.txt
└── README.md
```

## Setup

1. **Create and activate a virtual environment:**
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

## Running the Demos and Tests

- **Run Signals Demo:**
  ```bash
  python manage.py run_signals_demo
  ```

- **Run Rectangle Demo:**
  ```bash
  python manage.py run_rectangle_demo
  ```

- **Run Tests:**
  ```bash
  python manage.py test
  ```

---

## Answers to Assignment Questions

### Topic 1: Django Signals

1. **Are Django signals executed synchronously or asynchronously by default?**
   - **Answer:** Synchronously.
   - **Explanation:** When `save()` is called, Django executes all registered receiver functions inline on the current call stack before returning control to the caller. In `core/signals.py`, the signal handler sleeps for 2 seconds (`time.sleep(2)`), and the caller blocks and waits the full 2 seconds before continuing.

2. **Do Django signals run in the same thread as the caller?**
   - **Answer:** Yes.
   - **Explanation:** In `core/signals.py`, inspecting `threading.get_ident()` and `threading.current_thread().name` inside the receiver yields the exact same thread ID and name (`MainThread`) as the caller.

3. **By default, do Django signals run in the same database transaction as the caller?**
   - **Answer:** Yes.
   - **Explanation:** Signal handlers participate in the active transaction of the caller. In `core/signals.py`, the receiver creates a `SignalLog` entry. When wrapped in a `transaction.atomic()` block that raises an exception, both the parent model instance and the `SignalLog` created in the signal handler roll back together (count is 0).

### Topic 2: Custom Classes in Python (`Rectangle`)

The `Rectangle` class in `core/rectangle.py`:
- Accepts `length` and `width` as integers.
- Strictly validates types using `type(val) is not int`, raising a `TypeError` for floats, strings, and booleans (since `isinstance(True, int)` is `True` in Python).
- Implements `__iter__` to yield `{'length': self.length}` first and `{'width': self.width}` second.
- Uses a generator in `__iter__` so the instance can be iterated over multiple times.

**Example usage:**
```python
rect = Rectangle(10, 5)

for item in rect:
    print(item)

# Output:
# {'length': 10}
# {'width': 5}
```
