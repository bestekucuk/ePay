from django.db import models
#from django.contrib.auth.models import User
from account.models import CustomUser

class Transaction(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_transactions')
    sender_email = models.CharField(max_length=255, null=True, blank=True)
    receiver_email = models.CharField(max_length=255)
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_transactions', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.sender_email:
            self.sender_email = self.sender.email
        if self.receiver_email:
            try:
                self.receiver = CustomUser.objects.get(email=self.receiver_email)
            except CustomUser.DoesNotExist:
                pass
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.sender.username} -> {self.receiver_email} | Amount: {self.amount} | Date: {self.transaction_date}"
