from django.urls import path,include
from website import views

app_name = 'website'

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('contact/',views.ContactView.as_view(),name='contact'),
    path('newslatter/',views.NewsLetterView.as_view(),name='newslatter'),
    path('about/',views.AboutView.as_view(),name='about'),
]