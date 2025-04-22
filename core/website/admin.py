from django.contrib import admin
from website.models import Contact, NewsLetters

# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    list_display = ('first_name','last_name','email','created_date','phone_number')
    list_filter = ('email',)
    search_fields = ('name','message')
    
    
@admin.register(NewsLetters)
class NewsLettersAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    list_display = ('email','created_date')
    search_fields = ('email',)