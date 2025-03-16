from django.db import models

class DrinkType(models.Model):
    drink_type = models.CharField(max_length=100)
    price_small = models.DecimalField(max_digits=5, decimal_places=2)
    price_medium = models.DecimalField(max_digits=5, decimal_places=2)
    price_large = models.DecimalField(max_digits=5, decimal_places=2)
    simple = models.DecimalField(max_digits=5, decimal_places=2)
    double = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return self.drink_type

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
