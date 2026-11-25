from django.core.management.base import BaseCommand
from core.rectangle import Rectangle


class Command(BaseCommand):
    help = "Demonstrates creating and iterating over a Rectangle instance."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("=" * 70))
        self.stdout.write(self.style.SUCCESS("         TOPIC 2: RECTANGLE CLASS DEMONSTRATION         "))
        self.stdout.write(self.style.SUCCESS("=" * 70) + "\n")

        # 1. Create instance with length 10 and width 5
        rect = Rectangle(length=10, width=5)
        self.stdout.write(f"[INFO] Created instance: {rect}")
        self.stdout.write(f"[INFO] rect.length = {rect.length}, rect.width = {rect.width}\n")

        # 2. Iterate over the instance in a for loop
        self.stdout.write(self.style.MIGRATE_HEADING("--- Iterating over Rectangle(10, 5) with for loop ---"))
        for item in rect:
            self.stdout.write(f"Yielded: {item}")

        # 3. Demonstrate re-iterating over the same instance
        self.stdout.write("\n" + self.style.MIGRATE_HEADING("--- Re-iterating over the same instance ---"))
        for item in rect:
            self.stdout.write(f"Yielded: {item}")

        # 4. Demonstrate conversion to list
        self.stdout.write("\n" + self.style.MIGRATE_HEADING("--- Converting to list ---"))
        rect_list = list(rect)
        self.stdout.write(f"list(rect) -> {rect_list}")

        self.stdout.write("\n" + self.style.SUCCESS("=" * 70))
        self.stdout.write(self.style.SUCCESS("Rectangle demonstration completed successfully!"))
        self.stdout.write(self.style.SUCCESS("=" * 70) + "\n")

