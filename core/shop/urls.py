from django.urls import path,re_path
from shop import views

app_name = 'shop'

urlpatterns = [
    path('product/list/',views.ShopProductListView.as_view(),name='product-list'),
    path('product/grid/',views.ShopProductGridView.as_view(),name='product-grid'),
    re_path(r"product/(?P<slug>[-\w]+)/detail/",views.ShopProductDetailView.as_view(),name='product-detail'),
    path('product/remove/one/quantity/',views.ShopProductRemoveOneQuantityView.as_view(),name='product-remove-one-quantity'),
    path('product/remove/add/quantity/',views.ShopProductAddOneQuantityView.as_view(),name='product-add-one-quantity'),
    path("add-or-remove-wishlist/",views.AddOrRemoveWishlistView.as_view(),name="add-or-remove-wishlist")

]