from django.urls import path
from . import views

urlpatterns = [
    path('review/<product_id>/write-review/', views.ReviewApi.as_view(), name='write_review' ),
    path('review/get-all-reviews/', views.ReviewApi.as_view(), name='get_all_review' ),
    path('review/<review_id>/update-review/', views.ReviewApi.as_view(), name='update_review' ),
    path('review/<review_id>/delete-review/', views.ReviewApi.as_view(), name='delete_review' ),
    
    path('book/browse/', views.BookApi.as_view(), name='browse_book' ),
    path('book/filter-price/', views.PriceRangeFilter.as_view(), name='filter_price' ),
]