from django.views.generic import (
    ListView,
    DetailView,

    )
from shop.models import ProductModel,ProductStatusType,ProductCategoryModel
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
    queryset = ProductModel.objects.filter(status=ProductStatusType.publish.value)
    paginate_by = 9
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_items'] = self.get_queryset().count()
        context["categories"] = ProductCategoryModel.objects.all()
        return context
    
    
class ShopProductDetailView(DetailView):
    template_name = 'shop/product-detail.html'
    queryset = ProductModel.objects.filter(status=ProductStatusType.publish.value)

    
