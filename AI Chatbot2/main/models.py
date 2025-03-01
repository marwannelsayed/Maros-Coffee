from django.db import models

class Size(models.Model):
    name = models.CharField(max_length=10)
    price_multiplier = models.DecimalField(max_digits=3, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only for new instances
            last_size = Size.objects.order_by('-id').first()
            self.id = 1 if not last_size else last_size.id + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Pizza(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=6, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only for new instances
            last_pizza = Pizza.objects.order_by('-id').first()
            self.id = 1 if not last_pizza else last_pizza.id + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Beverage(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only for new instances
            last_beverage = Beverage.objects.order_by('-id').first()
            self.id = 1 if not last_beverage else last_beverage.id + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Order(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    beverage = models.ForeignKey(Beverage, on_delete=models.CASCADE, null=True, blank=True)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only for new instances
            last_order = Order.objects.order_by('-id').first()
            self.id = 1 if not last_order else last_order.id + 1
        # Calculate total price
        self.total_price = self.pizza.base_price * self.size.price_multiplier
        if self.beverage:
            self.total_price += self.beverage.price
        super().save(*args, **kwargs)

class Customer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only for new instances
            last_customer = Customer.objects.order_by('-id').first()
            self.id = 1 if not last_customer else last_customer.id + 1
        super().save(*args, **kwargs)

class ChatMessage(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    is_bot = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
