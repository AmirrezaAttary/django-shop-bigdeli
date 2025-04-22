from django.shortcuts import render
from django.views.generic import TemplateView,CreateView
from django.contrib import messages
from django.urls import reverse_lazy 
from django.utils.translation import gettext_lazy as _

from website.models import Contact,NewsLetters
from website.forms import ContactForm,NewsletterForm
# Create your views here.

class IndexView(TemplateView):
    template_name = 'website/index.html'
    form_class = NewsletterForm

    
class ContactView(CreateView):
    template_name = 'website/contact.html'
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy('website:contact')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("پیام شما با موفقیت ارسال شد."))
        return response
    
    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, _("لطفاً فرم را به‌درستی تکمیل کنید."))
        return super().form_invalid(form)
    
    
    
class NewsLetterView(CreateView):
    model = NewsLetters
    form_class = NewsletterForm
    success_url = reverse_lazy('website:index')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("ایمیل شما با موفقیت ثبت شد."))
        return response
    
    

class AboutView(TemplateView):
    template_name = 'website/about.html'