from django.db import models


class BalanceSheet(models.Model):
    variable = models.CharField(max_length=255)
    year = models.IntegerField()
    value = models.CharField(max_length=255)

    class Meta():
        unique_together = ('variable', 'year',)
        db_table = 'balance_sheet'
