from django.shortcuts import render
from django.views.generic import View
from .models import PaymentModel, PayemntStatusType
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from .zarinpal_client import ZarinPalSandbox
from order.models import OrderModel, OrderStatusType
from django.db import transaction
from shop.models import ProductModel
# Create your views here.


class PaymentVerifyView(View):
    
    def get(self,request,*args,**kwargs):
        authority_id = request.GET.get("Authority")
        status = request.GET.get("Status")
        payment_obj = get_object_or_404(PaymentModel,authority_id=authority_id)
        order = OrderModel.objects.get(payment=payment_obj)
        zarin_pal = ZarinPalSandbox()
        response = zarin_pal.payment_verify(int(payment_obj.amount),payment_obj.authority_id)
        print(response)
        if status == 'OK':
            with transaction.atomic():
                payment_obj.ref_id = response['data']["ref_id"]
                payment_obj.response_code = response['data']["code"]
                payment_obj.status = PayemntStatusType.success.value
                payment_obj.response_json = response
                payment_obj.save()

                order.status = OrderStatusType.success.value
                order.save()

                self.reduce_stock(order)

            return redirect(reverse_lazy("order:completed"))

        else:
            # payment_obj.ref_id = response['data']["ref_id"]
            payment_obj.response_code = response['errors']["code"]
            payment_obj.status = PayemntStatusType.failed.value
            payment_obj.response_json=response
            payment_obj.save()
            order.status = OrderStatusType.failed.value
            order.save()
            return redirect(reverse_lazy("order:failed"))
        
        
    def reduce_stock(self, order):
        """کاهش موجودی محصولات سفارش داده شده پس از پرداخت موفق"""
        for item in order.order_items.all():
            product = item.product
            if product.stock >= item.quantity:
                product.stock -= item.quantity
                product.save()
            else:
                raise ValueError(f"موجودی محصول '{product.title}' کافی نیست.")
