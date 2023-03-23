from django.urls import path
from . import views

urlpatterns = [
    path('customer/create-user/', views.CustomUserList.as_view(), name='create_user'),
    path('customer/get-user/', views.CustomUserList.as_view(), name='list_user'),
    path('customer/update-user/', views.CustomUserList.as_view(), name='update_user'),
    path('customer/delete-user/', views.CustomUserList.as_view(), name='delete_user'),
    
    path('user/login/', views.LogInUser.as_view(), name='login'),
    path('user/logout/', views.LogOutUser.as_view(), name='logout'),

    path('address/create-address/', views.AddressList.as_view(), name='create_address'),
    path('address/get-address/', views.AddressList.as_view(), name='list_address'),
    path('address/<house_no>/update-address/', views.AddressList.as_view(), name='update_address'),
    path('address/<house_no>/delete-address/', views.AddressList.as_view(), name='delete_address'),
]
