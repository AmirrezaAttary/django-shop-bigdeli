from django import forms
from website.models import Contact, NewsLetters


class ContactForm(forms.ModelForm):
    
    class Meta:
        model = Contact
        fields = ['first_name','last_name','message','email','phone_number',] 
        
    def save(self, commit=True):
        instance = super().save(commit=True) 
        if commit:
                instance.save()
        return instance
    
    
class NewsletterForm(forms.ModelForm):
    
    class Meta:
        model = NewsLetters
        fields = ['email',]
        
    def save(self, commit=True):
        instance = super().save(commit=True) 
        if commit:
                instance.save()
        return instance