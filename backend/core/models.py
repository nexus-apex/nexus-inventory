from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=255, blank=True, default="")
    category = models.CharField(max_length=255, blank=True, default="")
    quantity = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=[("in_stock", "In Stock"), ("low_stock", "Low Stock"), ("out_of_stock", "Out of Stock")], default="in_stock")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, default="")
    capacity = models.IntegerField(default=0)
    utilization = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    manager = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("maintenance", "Maintenance"), ("closed", "Closed")], default="active")
    contact = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class StockMovement(models.Model):
    product_name = models.CharField(max_length=255)
    warehouse = models.CharField(max_length=255, blank=True, default="")
    movement_type = models.CharField(max_length=50, choices=[("in", "In"), ("out", "Out"), ("transfer", "Transfer"), ("adjustment", "Adjustment")], default="in")
    quantity = models.IntegerField(default=0)
    reference = models.CharField(max_length=255, blank=True, default="")
    date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.product_name
