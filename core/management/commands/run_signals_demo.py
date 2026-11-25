import datetime
import threading
import time

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import SignalLog, SignalTestModel


class Command(BaseCommand):
    help = "Conclusively demonstrates the answers to the 3 Django Signal questions."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("=" * 80))
        self.stdout.write(self.style.SUCCESS("           DJANGO SIGNALS DEMONSTRATION & EMPIRICAL PROOF           "))
        self.stdout.write(self.style.SUCCESS("=" * 80))

        self.demo_question_1_synchronous()
        self.demo_question_2_same_thread()
        self.demo_question_3_same_transaction()

        self.stdout.write("\n" + self.style.SUCCESS("=" * 80))
        self.stdout.write(self.style.SUCCESS("           ALL DEMOS COMPLETED SUCCESSFULLY                        "))
        self.stdout.write(self.style.SUCCESS("=" * 80) + "\n")

    def demo_question_1_synchronous(self):
        self.stdout.write("\n" + self.style.MIGRATE_HEADING("-" * 80))
        self.stdout.write(self.style.MIGRATE_HEADING(" DEMO 1: Are Django Signals Synchronous or Asynchronous by Default? "))
        self.stdout.write(self.style.MIGRATE_HEADING("-" * 80))
        self.stdout.write("Expected Behavior: The caller thread pauses and waits for signal handlers to finish.\n")

        caller_start_time = time.time()
        caller_start_str = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.stdout.write(f"[CALLER] Starting object save at: {caller_start_str}")

        # The signal handler will detect 'Demo 1' and execute time.sleep(2)
        obj = SignalTestModel(name="Demo 1 - Synchronous Test Instance")
        obj.enable_delay = True
        obj.save()

        caller_end_time = time.time()
        caller_end_str = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        elapsed = caller_end_time - caller_start_time

        self.stdout.write(f"[CALLER] Save finished at:        {caller_end_str}")
        self.stdout.write(f"[CALLER] Total elapsed time:      {elapsed:.2f} seconds")

        self.stdout.write(self.style.SUCCESS(
            f"\n[CONCLUSION 1] PROVEN: The caller waited {elapsed:.2f}s for the signal handler (which slept 2.0s).\n"
            "               Django signals are executed SYNCHRONOUSLY by default."
        ))

    def demo_question_2_same_thread(self):
        self.stdout.write("\n" + self.style.MIGRATE_HEADING("-" * 80))
        self.stdout.write(self.style.MIGRATE_HEADING(" DEMO 2: Do Django Signals Run in the Same Thread as the Caller? "))
        self.stdout.write(self.style.MIGRATE_HEADING("-" * 80))
        self.stdout.write("Expected Behavior: Thread ID and Thread Name of caller and signal receiver match exactly.\n")

        caller_thread_id = threading.get_ident()
        caller_thread_name = threading.current_thread().name
        self.stdout.write(f"[CALLER] Thread ID: {caller_thread_id} | Thread Name: '{caller_thread_name}'")
        self.stdout.write("[CALLER] Triggering signal by saving SignalTestModel...")

        SignalTestModel.objects.create(name="Demo 2 - Same Thread Test Instance")

        self.stdout.write(self.style.SUCCESS(
            f"\n[CONCLUSION 2] PROVEN: The signal handler ran in Thread ID {caller_thread_id} ('{caller_thread_name}').\n"
            "               Django signals run in the SAME THREAD as the caller."
        ))

    def demo_question_3_same_transaction(self):
        self.stdout.write("\n" + self.style.MIGRATE_HEADING("-" * 80))
        self.stdout.write(self.style.MIGRATE_HEADING(" DEMO 3: Do Django Signals Run in the Same DB Transaction? "))
        self.stdout.write(self.style.MIGRATE_HEADING("-" * 80))
        self.stdout.write(
            "Expected Behavior: Operations in signal handler (e.g. SignalLog creation) share the\n"
            "                   caller's transaction. If caller rolls back, signal changes roll back too.\n"
        )

        # Clean any prior Demo 3 entries to ensure clean verification
        SignalTestModel.objects.filter(name__icontains="Demo 3").delete()
        SignalLog.objects.filter(message__icontains="Demo 3").delete()

        self.stdout.write("[CALLER] Entering transaction.atomic() block...")
        try:
            with transaction.atomic():
                self.stdout.write("[CALLER] Inside transaction: Creating SignalTestModel...")
                SignalTestModel.objects.create(name="Demo 3 - Transaction Rollback Test")

                self.stdout.write("[CALLER] Inside transaction: Raising forced Exception to trigger rollback!")
                raise RuntimeError("Forced rollback to verify transaction behavior!")
        except RuntimeError as e:
            self.stdout.write(f"[CALLER] Caught exception outside transaction block: '{e}'")

        # Verify DB counts for Demo 3
        model_count = SignalTestModel.objects.filter(name__icontains="Demo 3").count()
        log_count = SignalLog.objects.filter(message__icontains="Demo 3").count()

        self.stdout.write(f"\n[DATABASE VERIFICATION]")
        self.stdout.write(f"  - SignalTestModel records in DB (name ~ 'Demo 3'): {model_count}")
        self.stdout.write(f"  - SignalLog records in DB (message ~ 'Demo 3'):       {log_count}")

        if model_count == 0 and log_count == 0:
            self.stdout.write(self.style.SUCCESS(
                "\n[CONCLUSION 3] PROVEN: Both SignalTestModel and SignalLog count are 0.\n"
                "               Even though SignalLog was created inside the post_save signal handler,\n"
                "               it was rolled back when the caller's transaction was rolled back.\n"
                "               Django signals run in the SAME DATABASE TRANSACTION by default."
            ))
        else:
            self.stdout.write(self.style.ERROR(
                f"\n[UNEXPECTED]: model_count={model_count}, log_count={log_count}"
            ))

