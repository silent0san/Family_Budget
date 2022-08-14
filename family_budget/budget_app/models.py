from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import uuid


class Budget(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Budget Name', blank=False, null=False, max_length=150)
    created_date = models.DateTimeField('Created Date', default=now, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(User, blank=True, related_name='shared_with')
    total_value = models.DecimalField('Sum', max_digits=9, decimal_places=2, blank=False, null=True, default=0)

    def __str__(self):
        return self.name


class BudgetRecord(models.Model):
    name = models.CharField('Record Name', blank=False, null=False, max_length=150)
    value = models.DecimalField(max_digits=9, decimal_places=2, blank=False, null=False)
    created_date = models.DateTimeField(default=now, editable=False)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
