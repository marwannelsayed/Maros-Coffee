from django.db import models

class Order(models.Model):
    # Store pizza, size, and beverage as JSON data instead of foreign keys
    pizza_data = models.JSONField()
    size_data = models.JSONField()
    beverage_data = models.JSONField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only for new instances
            last_order = Order.objects.order_by('-id').first()
            self.id = 1 if not last_order else last_order.id + 1
        # Calculate total price
        self.total_price = float(self.pizza_data.get('base_price', 0)) * float(self.size_data.get('price_multiplier', 1.0))
        if self.beverage_data:
            self.total_price += float(self.beverage_data.get('price', 0))
        super().save(*args, **kwargs)

class Customer(models.Model):
    session_key = models.CharField(max_length=40, primary_key=True)
    customer_id = models.IntegerField(null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.customer_id:
            last_customer = Customer.objects.order_by('-customer_id').first()
            self.customer_id = 1 if not last_customer else last_customer.customer_id + 1
        super().save(*args, **kwargs)
        
    @classmethod
    def get_from_session(cls, session):
        """Get or create a customer based on the session key"""
        session_key = session.session_key
        if not session_key:
            session.save()
            session_key = session.session_key
            
        customer, created = cls.objects.get_or_create(session_key=session_key)
        return customer

class ChatMessage(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    is_bot = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
