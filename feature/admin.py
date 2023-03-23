from django.contrib import admin
from .models import Cart, WishList, Payment, Order, ReturnItem
# Register your models here.
admin.site.register(Cart)
admin.site.register(WishList)
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(ReturnItem)

