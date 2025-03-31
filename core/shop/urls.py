from django.urls import path,include
from shop import views

app_name = 'shop'

urlpatterns = [
    path('product/list/',views.ShopProductListView.as_view(),name='product-list'),
    path('product/grid/',views.ShopProductGridView.as_view(),name='product-grid'),

]