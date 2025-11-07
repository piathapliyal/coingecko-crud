from django.db import models

class Coin(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20, unique=True)
    coingecko_id = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. 'bitcoin', 'ethereum'")

    price = models.DecimalField(max_digits=18, decimal_places=8, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"
