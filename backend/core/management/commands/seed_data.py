from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Product, Warehouse, StockMovement
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusInventory with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexusinventory.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Product.objects.count() == 0:
            for i in range(10):
                Product.objects.create(
                    name=f"Sample Product {i+1}",
                    sku=f"Sample {i+1}",
                    category=f"Sample {i+1}",
                    quantity=random.randint(1, 100),
                    reorder_level=random.randint(1, 100),
                    unit_price=round(random.uniform(1000, 50000), 2),
                    cost_price=round(random.uniform(1000, 50000), 2),
                    status=random.choice(["in_stock", "low_stock", "out_of_stock"]),
                )
            self.stdout.write(self.style.SUCCESS('10 Product records created'))

        if Warehouse.objects.count() == 0:
            for i in range(10):
                Warehouse.objects.create(
                    name=f"Sample Warehouse {i+1}",
                    location=f"Sample {i+1}",
                    capacity=random.randint(1, 100),
                    utilization=round(random.uniform(1000, 50000), 2),
                    manager=f"Sample {i+1}",
                    status=random.choice(["active", "maintenance", "closed"]),
                    contact=f"Sample {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Warehouse records created'))

        if StockMovement.objects.count() == 0:
            for i in range(10):
                StockMovement.objects.create(
                    product_name=f"Sample StockMovement {i+1}",
                    warehouse=f"Sample {i+1}",
                    movement_type=random.choice(["in", "out", "transfer", "adjustment"]),
                    quantity=random.randint(1, 100),
                    reference=f"Sample {i+1}",
                    date=date.today() - timedelta(days=random.randint(0, 90)),
                    notes=f"Sample notes for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 StockMovement records created'))
