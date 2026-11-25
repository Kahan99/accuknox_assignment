import datetime
import threading
import time

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import SignalLog, SignalTestModel


@receiver(post_save, sender=SignalTestModel)
def sync_check_handler(sender, instance, created, **kwargs):
    # Only sleep when delay is requested so other saves run fast
    if getattr(instance, 'delay', False) or getattr(instance, 'enable_delay', False) or 'demo 1' in instance.name.lower():
        start = datetime.datetime.now()
        print(f"Signal handler started:  {start.strftime('%H:%M:%S')}")
        time.sleep(2)
        end = datetime.datetime.now()
        print(f"Signal handler finished: {end.strftime('%H:%M:%S')}")
        instance._signal_duration = (end - start).total_seconds()


@receiver(post_save, sender=SignalTestModel)
def thread_check_handler(sender, instance, created, **kwargs):
    thread_id = threading.get_ident()
    thread_name = threading.current_thread().name
    print(f"Signal handler thread: {thread_id} ({thread_name})")
    instance._thread_id = thread_id
    instance._thread_name = thread_name


@receiver(post_save, sender=SignalTestModel)
def transaction_check_handler(sender, instance, created, **kwargs):
    log = SignalLog.objects.create(message=f"Log for {instance.name}")
    print(f"Signal created log: '{log.message}' (id={log.id})")
    instance._log_id = log.id
