from django.core.management.base import BaseCommand
import csv
from django.conf import settings
from pathlib import Path
from core.models import Language

class Command(BaseCommand):
    help = "Seed languages from CSV"

    def handle(self, *args, **kwargs):
        seed_languages()
        self.stdout.write(self.style.SUCCESS("Languages seeding completed."))


def seed_languages():
    # If table is empty, we should seed everything
    if Language.objects.exists():
        print("ℹ️  Languages table is not empty. Seeding only missing entries...")

    csv_path = Path(settings.BASE_DIR) / "data" / "languages.csv"
    if not csv_path.exists():
        print("⚠️  languages.csv not found, skipping seeding.")
        return

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        created_count = 0
        for row in reader:
            code = row["language_code"].strip()
            language, created = Language.objects.get_or_create(
                language_code=code,
                defaults={
                    "language_name": row["language_name"].strip(),
                    "language_native_name": row["language_native_name"].strip(),
                    "language_direction": row["language_direction"].strip()
                }
            )
            if created:
                created_count += 1

        if created_count:
            print(f"✅ Seeded {created_count} new languages into the database.")
        else:
            print("ℹ️  No new languages to seed.")
