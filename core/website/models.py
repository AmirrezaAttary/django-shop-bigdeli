from django.db import models
from website.validators import validate_iranian_cellphone_number

# Create your models here.
class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=12, null=True, blank=True, validators=[validate_iranian_cellphone_number])
    message = models.TextField()
    
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']
    def __str__(self):
        return self.email
    
    
class NewsLetters(models.Model):
    email = models.EmailField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']
    def __str__(self):
        return self.email