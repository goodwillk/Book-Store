from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'carts', views.CartViewSet, basename='carts')

urlpatterns = [
    path('', include(router.urls)),
    path('<book_id>/cart/', views.CartViewSet.as_view({'delete':'remove_item', 'post':'add_item'})),
    path('cart/', views.CartViewSet.as_view({'get':'view_cart'})),
    path('cart-checkout/', views.CartViewSet.as_view({'put':'checkout_cart'})),
    
    path('wishlist/', views.WishListViewSet.as_view({'post':'create_wishlist'})),
    path('<wishlist_id>/<book_id>/wishlist/', views.WishListViewSet.as_view({'delete':'remove_item', 'put':'add_item'})),
    
    path('order/', views.OrderViewSet.as_view({'get':'get_all_order'})),
    
    path('<order_id>/return-order/', views.ReturnItemViewSet.as_view({'post':'return_order'})),
    path('return-order/', views.ReturnItemViewSet.as_view({'get':'all_returned_order'})),
]