from django.core.management.base import BaseCommand
from django.db import transaction

from products.models import Category, Product


class Command(BaseCommand):
    help = 'Add demo products without replacing existing catalog entries.'

    @transaction.atomic
    def handle(self, *args, **options):
        samples = [
            ('A5 Notebook', 'Paper goods',
             'A fresh page for lecture notes, plans, and new ideas.',
             'products/notebook.jpg', 'An open notebook ready for writing'),
            ('Everyday Backpack', 'On the move',
             'Keep your daily study essentials together.',
             'products/backpack.jpg', 'An everyday backpack'),
            ('Desk Lamp', 'Study space',
             'A little light for your next chapter.',
             'products/lamp.jpg', 'A lamp for a study desk'),
        ]
        added = 0
        for name, category_name, description, image, image_alt in samples:
            category, _ = Category.objects.get_or_create(name=category_name)
            if not Product.objects.filter(name=name).exists():
                Product.objects.create(
                    name=name, category=category, description=description,
                    image=image, image_alt=image_alt,
                )
                added += 1
        self.stdout.write(self.style.SUCCESS(f'Added {added} demo products.'))
