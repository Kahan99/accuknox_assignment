import threading
import time

from django.db import transaction
from django.test import TestCase

from core.models import SignalLog, SignalTestModel
from core.rectangle import Rectangle


class DjangoSignalsTests(TestCase):
    """
    Automated unit tests proving all 3 questions on Django Signals.
    """

    def test_question_1_signals_execute_synchronously(self):
        """
        Question 1: Are Django signals executed synchronously or asynchronously by default?
        Proof: Caller initiates save and waits >= 2 seconds for signal handler sleep to complete.
        """
        obj = SignalTestModel(name="Test Q1 Synchronous")
        obj.enable_delay = True

        start_time = time.time()
        obj.save()
        elapsed = time.time() - start_time

        # Total elapsed time must be at least 2.0 seconds
        self.assertGreaterEqual(elapsed, 2.0)
        self.assertTrue(hasattr(obj, '_signal_q1_duration'))
        self.assertGreaterEqual(obj._signal_q1_duration, 2.0)

    def test_question_2_signals_run_in_same_thread(self):
        """
        Question 2: Do Django signals run in the same thread as the caller?
        Proof: Thread ID and Thread Name of the signal handler match caller's exactly.
        """
        caller_thread_id = threading.get_ident()
        caller_thread_name = threading.current_thread().name

        obj = SignalTestModel.objects.create(name="Test Q2 Same Thread")

        self.assertEqual(obj._signal_thread_id, caller_thread_id)
        self.assertEqual(obj._signal_thread_name, caller_thread_name)

    def test_question_3_signals_run_in_same_database_transaction(self):
        """
        Question 3: By default, do Django signals run in the same database transaction as the caller?
        Proof: When the caller's transaction rolls back, records created by the signal handler
        (SignalLog) are rolled back as well.
        """
        test_model_name = "Test Q3 Transaction Rollback"

        try:
            with transaction.atomic():
                SignalTestModel.objects.create(name=test_model_name)
                # Forced exception to trigger transaction rollback
                raise RuntimeError("Forced rollback for testing transaction atomicity")
        except RuntimeError:
            pass

        # Verify that both the parent model and the signal-created log were rolled back
        model_count = SignalTestModel.objects.filter(name=test_model_name).count()
        log_count = SignalLog.objects.filter(message__icontains=test_model_name).count()

        self.assertEqual(model_count, 0, "SignalTestModel should have been rolled back.")
        self.assertEqual(log_count, 0, "SignalLog created in signal handler should have been rolled back.")


class RectangleClassTests(TestCase):
    """
    Automated unit tests for Topic 2: Custom Rectangle Class.
    """

    def test_rectangle_attributes(self):
        """Verify length and width attributes are set properly."""
        rect = Rectangle(length=10, width=5)
        self.assertEqual(rect.length, 10)
        self.assertEqual(rect.width, 5)

    def test_rectangle_iteration_output(self):
        """Verify iteration yields {'length': <val>} first, then {'width': <val>}."""
        rect = Rectangle(10, 5)
        items = list(rect)
        self.assertEqual(items, [{'length': 10}, {'width': 5}])

    def test_rectangle_multiple_iterations(self):
        """Verify that the same Rectangle instance can be iterated over multiple times."""
        rect = Rectangle(20, 15)
        first_iteration = list(rect)
        second_iteration = list(rect)
        third_iteration = [item for item in rect]

        expected = [{'length': 20}, {'width': 15}]
        self.assertEqual(first_iteration, expected)
        self.assertEqual(second_iteration, expected)
        self.assertEqual(third_iteration, expected)

    def test_rectangle_type_validation_rejects_non_integers(self):
        """Verify that non-integer inputs (strings, floats, None) raise TypeError."""
        invalid_inputs = [
            ("10", 5),
            (10, "5"),
            ("10", "5"),
            (10.5, 5),
            (10, 5.2),
            (None, 5),
            (10, None),
            ([10], 5),
            (10, {'width': 5}),
        ]
        for l, w in invalid_inputs:
            with self.subTest(length=l, width=w):
                with self.assertRaises(TypeError):
                    Rectangle(l, w)

    def test_rectangle_type_validation_rejects_booleans(self):
        """
        Verify that boolean values raise TypeError, since bool is an int subclass in Python.
        """
        invalid_bool_inputs = [
            (True, 5),
            (False, 5),
            (10, True),
            (10, False),
            (True, False),
        ]
        for l, w in invalid_bool_inputs:
            with self.subTest(length=l, width=w):
                with self.assertRaises(TypeError):
                    Rectangle(l, w)

    def test_rectangle_repr_and_equality(self):
        """Verify string representation and equality comparison."""
        r1 = Rectangle(10, 5)
        r2 = Rectangle(10, 5)
        r3 = Rectangle(5, 10)

        self.assertEqual(repr(r1), "Rectangle(length=10, width=5)")
        self.assertEqual(r1, r2)
        self.assertNotEqual(r1, r3)
        self.assertNotEqual(r1, "not a rectangle")
