import threading
import time

from django.db import transaction
from django.test import TestCase

from core.models import SignalLog, SignalTestModel
from core.rectangle import Rectangle


class SignalTests(TestCase):
    def test_sync_execution(self):
        obj = SignalTestModel(name="test_sync")
        obj.delay = True

        start = time.time()
        obj.save()
        elapsed = time.time() - start

        # Receiver sleeps for 2s, so caller must take at least 2s
        self.assertGreaterEqual(elapsed, 2.0)

    def test_same_thread(self):
        caller_tid = threading.get_ident()
        caller_tname = threading.current_thread().name

        obj = SignalTestModel.objects.create(name="test_thread")

        self.assertEqual(obj._thread_id, caller_tid)
        self.assertEqual(obj._thread_name, caller_tname)

    def test_same_transaction(self):
        # Force a rollback inside transaction.atomic()
        try:
            with transaction.atomic():
                SignalTestModel.objects.create(name="test_tx")
                raise RuntimeError("rollback")
        except RuntimeError:
            pass

        # Both the model and the log created in the signal should be rolled back
        self.assertEqual(SignalTestModel.objects.filter(name="test_tx").count(), 0)
        self.assertEqual(SignalLog.objects.filter(message__icontains="test_tx").count(), 0)


class RectangleTests(TestCase):
    def test_iteration(self):
        rect = Rectangle(10, 5)
        self.assertEqual(list(rect), [{'length': 10}, {'width': 5}])

    def test_multiple_iterations(self):
        rect = Rectangle(20, 10)
        self.assertEqual(list(rect), [{'length': 20}, {'width': 10}])
        self.assertEqual(list(rect), [{'length': 20}, {'width': 10}])

    def test_rejects_non_integers(self):
        invalid_values = ["10", 10.5, None, [10], {"w": 5}]
        for val in invalid_values:
            with self.subTest(val=val):
                with self.assertRaises(TypeError):
                    Rectangle(val, 5)
                with self.assertRaises(TypeError):
                    Rectangle(10, val)

    def test_rejects_booleans(self):
        # bool is an int subclass in Python, verify it gets rejected
        with self.assertRaises(TypeError):
            Rectangle(True, 5)
        with self.assertRaises(TypeError):
            Rectangle(10, False)
