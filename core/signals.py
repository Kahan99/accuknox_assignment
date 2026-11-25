import datetime
import threading
import time
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SignalTestModel, SignalLog


# ==============================================================================
# Question 1: Are Django signals executed synchronously or asynchronously by default?
# ==============================================================================
@receiver(post_save, sender=SignalTestModel)
def question_1_sync_handler(sender, instance, created, **kwargs):
    """
    Demonstrates that Django signals run synchronously by default.
    The caller execution is blocked while this handler sleeps for 2 seconds.
    """
    if getattr(instance, 'enable_delay', False) or 'demo 1' in instance.name.lower():
        start_time = datetime.datetime.now()
        print(f"  [Signal - Q1 Sync] Handler started at:  {start_time.strftime('%H:%M:%S.%f')[:-3]}")
        print("  [Signal - Q1 Sync] Sleeping for 2.0 seconds to simulate blocking execution...")
        time.sleep(2)
        end_time = datetime.datetime.now()
        print(f"  [Signal - Q1 Sync] Handler finished at: {end_time.strftime('%H:%M:%S.%f')[:-3]}")
        # Attach execution tracking for programmatic assertions in unit tests
        instance._signal_q1_duration = (end_time - start_time).total_seconds()


# ==============================================================================
# Question 2: Do Django signals run in the same thread as the caller?
# ==============================================================================
@receiver(post_save, sender=SignalTestModel)
def question_2_thread_handler(sender, instance, created, **kwargs):
    """
    Demonstrates that Django signals execute in the exact same thread as the caller.
    """
    thread_id = threading.get_ident()
    thread_name = threading.current_thread().name
    print(f"  [Signal - Q2 Thread] Thread ID: {thread_id} | Thread Name: '{thread_name}'")
    # Attach thread information to instance for programmatic assertions in unit tests
    instance._signal_thread_id = thread_id
    instance._signal_thread_name = thread_name


# ==============================================================================
# Question 3: By default, do Django signals run in the same database transaction as the caller?
# ==============================================================================
@receiver(post_save, sender=SignalTestModel)
def question_3_transaction_handler(sender, instance, created, **kwargs):
    """
    Demonstrates that Django signals execute in the same database transaction.
    Creating a SignalLog record here will be rolled back if the caller's transaction rolls back.
    """
    log_entry = SignalLog.objects.create(message=f"SignalLog entry for '{instance.name}'")
    print(f"  [Signal - Q3 Transaction] Created SignalLog: ID={log_entry.id}, Message='{log_entry.message}'")
    instance._signal_log_id = log_entry.id
