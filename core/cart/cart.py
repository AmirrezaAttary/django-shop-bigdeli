from shop.models import ProductModel,ProductStatusType
from cart.models import CartModel,CartItemModel

class CartSession:
    def __init__(self, session):
        self.session = session
        self._cart = self.session.setdefault("cart", {"items": []})

    def update_product_quantity(self,product_id,quantity):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                item["quantity"] = int(quantity)
                break
        else:
            return
        self.save()
    
    def remove_product(self,product_id):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                self._cart["items"].remove(item)
                break
        else:
            return
        self.save()
        
    def add_product(self, product_id):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                item["quantity"] += 1
                break
        else:
            new_item = {"product_id": product_id, "quantity": 1}
            self._cart["items"].append(new_item)
        self.save()
        
        
    def clear(self):
        self._cart = self.session["cart"] = {"items": []}
        self.save()

    def get_cart_dict(self):
        return self._cart

    def get_cart_items(self):
        items = []
        updated_cart = []
        changed = False

        for item in list(self._cart["items"]):
            try:
                product = ProductModel.objects.get(id=item["product_id"], status=ProductStatusType.publish.value)
                
                # بررسی موجودی
                if product.stock == 0:
                    changed = True
                    continue

                quantity = min(item["quantity"], product.stock)
                if quantity != item["quantity"]:
                    item["quantity"] = quantity
                    changed = True

                total_price = quantity * product.get_price()

                # فقط برای نمایش
                items.append({
                    "product_id": product.id,
                    "product_obj": product,
                    "quantity": quantity,
                    "total_price": total_price
                })

                # برای ذخیره در session
                updated_cart.append({
                    "product_id": product.id,
                    "quantity": quantity
                })

            except ProductModel.DoesNotExist:
                changed = True
                continue

        if changed:
            self._cart["items"] = updated_cart
            self.save()

        return items

    def has_product(self, product_id):
        count = sum(1 for item in self._cart["items"] if item["product_id"] == product_id)
        return count


    def get_total_payment_amount(self):
        items = self.get_cart_items()
        return sum(item["total_price"] for item in items)

    def get_total_quantity(self):
        items = self.get_cart_items()
        return sum(item["quantity"] for item in items)


    def save(self):
        self.session.modified = True



    def decrease_product_quantity(self, product_id):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                if item["quantity"] > 1:
                    item["quantity"] -= 1
                else:
                    self._cart["items"].remove(item)  # یا می‌تونی فقط quantity رو صفر کنی
                break
        else:
            return  # اگر محصول در سبد نبود کاری نکن
        self.save()



    def increase_product_quantity(self, product_id):
        try:
            product = ProductModel.objects.get(id=product_id, status=ProductStatusType.publish.value)
        except ProductModel.DoesNotExist:
            return

        if product.stock == 0:
            return

        for item in self._cart["items"]:
            if item["product_id"] == product_id:
                if item["quantity"] < product.stock:
                    item["quantity"] += 1
                break
        else:
            # اضافه کردن اگر قبلاً نبود
            self._cart["items"].append({
                "product_id": product_id,
                "quantity": 1
            })

        self.save()
        
        
    def sync_cart_items_from_db(self, user):
        cart, created = CartModel.objects.get_or_create(user=user)
        cart_items = CartItemModel.objects.filter(cart=cart)

        for cart_item in cart_items:
            product = cart_item.product

            if product.stock == 0:
                continue  # محصول بدون موجودی را نادیده بگیر

            quantity = min(cart_item.quantity, product.stock)

            # اگر قبلاً در سبد خرید session بوده، مقدارش را آپدیت کن
            for item in self._cart["items"]:
                if str(product.id) == str(item["product_id"]):
                    item["quantity"] = quantity
                    break
            else:
                # اگر نبود، اضافه‌اش کن
                new_item = {"product_id": str(product.id), "quantity": quantity}
                self._cart["items"].append(new_item)

        self.merge_session_cart_in_db(user)
        self.save()


    def merge_session_cart_in_db(self, user):
        cart, created = CartModel.objects.get_or_create(user=user)

        session_product_ids = []

        for item in self._cart["items"]:
            try:
                product_obj = ProductModel.objects.get(id=item["product_id"], status=ProductStatusType.publish.value)
            except ProductModel.DoesNotExist:
                continue

            if product_obj.stock == 0:
                continue  # از ذخیره محصول بدون موجودی صرف‌نظر کن

            quantity = min(item["quantity"], product_obj.stock)

            cart_item, created = CartItemModel.objects.get_or_create(cart=cart, product=product_obj)
            cart_item.quantity = quantity
            cart_item.save()

            session_product_ids.append(product_obj.id)

        # حذف آیتم‌هایی که در session نیستند یا موجودی ندارند
        CartItemModel.objects.filter(cart=cart).exclude(product__id__in=session_product_ids).delete()
