from django.views.generic import (
    ListView,
    DetailView,
    View
    )
from shop.models import ProductModel,ProductStatusType,ProductCategoryModel,WishlistProductModel
from django.core.exceptions import FieldError
from cart.cart import CartSession
from django.http import JsonResponse
# Create your views here.

class ShopProductListView(ListView):
    template_name = 'shop/product-list.html'
    queryset = ProductModel.objects.filter(status=ProductStatusType.publish.value)
    paginate_by = 9
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_items'] = self.get_queryset().count()
        return context
    
    
class ShopProductGridView(ListView):
    template_name = 'shop/product-grid.html'
    paginate_by = 9


    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size',self.paginate_by)
    
    def get_queryset(self):
        queryset = ProductModel.objects.filter(status=ProductStatusType.publish.value)
        search_q=self.request.GET.get('q')
        if search_q:
            queryset = queryset.filter(title__icontains=search_q)
        category_id=self.request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(category__id=category_id)

        if min_price:= self.request.GET.get('min_price'):
            queryset = queryset.filter(price__gte=min_price)

        if max_price:= self.request.GET.get('max_price'):
            queryset = queryset.filter(price__lte=max_price)

        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_items'] = self.get_queryset().count()
        context["wishlist_items"] = WishlistProductModel.objects.filter(user=self.request.user).values_list("product__id",flat=True)
        context["categories"] = ProductCategoryModel.objects.all()
        return context
    
    
class ShopProductDetailView(DetailView):
    template_name = 'shop/product-detail.html'
    queryset = ProductModel.objects.filter(status=ProductStatusType.publish.value)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        cart_item = self.request.session.get('cart', {'items': []})
        

        quantity = 1

        for item in cart_item.get('items', []):
            if item['product_id'] == str(product.id):
                quantity = item.get('quantity', 1)
                break

        context['in_cart'] = quantity > 1 or any(item['product_id'] == str(product.id) for item in cart_item.get('items', []))
        context['quantity'] = quantity
        context["is_wished"] = WishlistProductModel.objects.filter(user=self.request.user,product__id=self.get_object().id).exists()
        return context
    

class ShopProductRemoveOneQuantityView(View):

    def post(self,request,*args,**kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        cart.decrease_product_quantity(product_id)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)

        return JsonResponse({"cart":cart.get_cart_dict()})


class ShopProductAddOneQuantityView(View):

    def post(self,request,*args,**kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        cart.increase_product_quantity(product_id)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)

        return JsonResponse({"cart":cart.get_cart_dict()})