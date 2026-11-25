from django.core.management.base import BaseCommand
from core.rectangle import Rectangle


class Command(BaseCommand):
    help = "Demonstrates the Rectangle custom class."

    def handle(self, *args, **options):
        print("\n=== Rectangle Class Demo ===")
        rect = Rectangle(10, 5)
        print(f"Created: {rect} (length={rect.length}, width={rect.width})\n")

        print("First iteration:")
        for item in rect:
            print(f"  {item}")

        print("\nSecond iteration:")
        for item in rect:
            print(f"  {item}")

        print(f"\nAs list: {list(rect)}\n")
