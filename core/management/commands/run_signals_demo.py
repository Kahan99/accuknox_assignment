import datetime
import threading
import time

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import SignalLog, SignalTestModel


class Command(BaseCommand):
    help = "Demonstrates Django signals behavior (sync vs async, threading, transactions)."

    def handle(self, *args, **options):
        # 1. Sync vs Async
        print("\n=== Question 1: Synchronous vs Asynchronous ===")
        print("Caller initiating save...")
        start_time = time.time()
        obj = SignalTestModel(name="Demo 1")
        obj.delay = True
        obj.save()
        elapsed = time.time() - start_time
        print(f"Caller finished. Elapsed time: {elapsed:.2f}s")
        print("Conclusion: Caller blocked for 2s while the signal slept, proving signals run synchronously.\n")

        # 2. Threading
        print("=== Question 2: Thread Execution ===")
        caller_tid = threading.get_ident()
        caller_tname = threading.current_thread().name
        print(f"Caller thread: {caller_tid} ({caller_tname})")
        SignalTestModel.objects.create(name="Demo 2")
        print("Conclusion: Caller and signal handler report the same thread ID and name.\n")

        # 3. Database Transactions
        print("=== Question 3: Database Transactions ===")
        SignalTestModel.objects.filter(name__icontains="Demo 3").delete()
        SignalLog.objects.filter(message__icontains="Demo 3").delete()

        print("Creating record inside transaction.atomic(), then triggering a rollback...")
        try:
            with transaction.atomic():
                SignalTestModel.objects.create(name="Demo 3")
                raise RuntimeError("Forced rollback")
        except RuntimeError:
            print("Caught exception outside atomic block.")

        model_count = SignalTestModel.objects.filter(name__icontains="Demo 3").count()
        log_count = SignalLog.objects.filter(message__icontains="Demo 3").count()
        print(f"Records in DB: SignalTestModel={model_count}, SignalLog={log_count}")
        print("Conclusion: The log created inside the signal handler was rolled back with the caller's transaction.\n")
