from django.db import models
from customer.models import BaseModel, CustomUser
from product.models import Book

class Cart(BaseModel):
    custom_user_id = models.OneToOneField(CustomUser, related_name='cart_to_cu', on_delete = models.CASCADE)
    book_id = models.ManyToManyField(Book, blank=True)


class WishList(BaseModel):
    custom_user_id = models.ForeignKey(CustomUser, related_name='wishlist_to_cu', on_delete = models.CASCADE)
    book_id = models.ManyToManyField(Book, blank=True)


class Payment(BaseModel):
    payment_method = models.CharField(max_length=150)


class Order(BaseModel):
    book_id = models.ManyToManyField(Book, blank=True)
    user_id = models.ForeignKey(CustomUser, related_name='order_to_cu', on_delete = models.CASCADE)
    payment_id = models.OneToOneField(Payment, related_name='order_to_payment', on_delete = models.CASCADE)


class ReturnItem(BaseModel):
    order_id = models.OneToOneField(Order, related_name='ri_to_order', on_delete = models.CASCADE)
    reason = models.CharField(max_length=400)