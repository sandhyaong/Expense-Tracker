from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Expense(models.Model):

    title = models.CharField(max_length=200)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    description = models.TextField(blank=True)

    receipt = models.ImageField(
        upload_to="receipts/",
        null=True,
        blank=True
    )

    STATUS_CHOICES = (
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected')
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title