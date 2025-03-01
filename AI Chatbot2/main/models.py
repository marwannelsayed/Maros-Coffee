from django.db import models

class Size(models.Model):
    name = models.CharField(max_length=10)
    price_multiplier = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return self.name

class Pizza(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class Beverage(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    beverage = models.ForeignKey(Beverage, on_delete=models.CASCADE, null=True, blank=True)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate total price
        self.total_price = self.pizza.base_price * self.size.price_multiplier
        if self.beverage:
            self.total_price += self.beverage.price
        super().save(*args, **kwargs)
