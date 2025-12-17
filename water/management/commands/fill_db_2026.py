import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from water.models import WaterAssay


class Command(BaseCommand):
    help = 'Импорт начальных анализов воды из файла 2026.csv (address;customer;дд.мм.гггг)'

    def handle(self, *args, **options):
        # Путь к файлу — рядом с manage.py или в корне проекта
        csv_file_path = os.path.join(settings.BASE_DIR, 'water', 'management', 'commands', '2026.csv')

        if not os.path.exists(csv_file_path):
            self.stdout.write(
                self.style.ERROR(f'Файл {csv_file_path} не найден!')
            )
            return

        created_count = 0
        skipped_count = 0
        error_count = 0

        with open(csv_file_path, encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            for row_num, row in enumerate(reader, start=1):
                if len(row) < 3:
                    self.stdout.write(
                        self.style.WARNING(f'Строка {row_num}: недостаточно колонок — пропуск')
                    )
                    skipped_count += 1
                    continue

                address, customer, date_str = [cell.strip() for cell in row[:3]]

                if not all([address, customer, date_str]):
                    self.stdout.write(
                        self.style.WARNING(f'Строка {row_num}: пустые значения — пропуск')
                    )
                    skipped_count += 1
                    continue

                # Парсим дату дд.мм.гггг
                try:
                    conclusion_date = datetime.strptime(date_str, '%d.%m.%Y').date()
                except ValueError:
                    self.stdout.write(
                        self.style.ERROR(f'Строка {row_num}: неверный формат даты "{date_str}"')
                    )
                    error_count += 1
                    continue

                # Проверяем, нет ли уже такого же объекта (избегаем дубликатов)
                if WaterAssay.objects.filter(
                    address=address,
                    customer=customer,
                    conclusion_date=conclusion_date
                ).exists():
                    skipped_count += 1
                    continue

                # Создаём объект
                WaterAssay.objects.create(
                    address=address,
                    customer=customer,
                    conclusion_date=conclusion_date
                )
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Импорт завершён: создано {created_count} записей, '
                f'пропущено {skipped_count}, ошибок {error_count}'
            )
        )