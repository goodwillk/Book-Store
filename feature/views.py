from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from msg_enum import Message

from rest_framework import viewsets, authentication, mixins
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import CartSerializer, WishListSerializer, PaymentSerializer, OrderSerializer, ReturnItemSerializer
from .models import Cart, WishList, Payment, Order, ReturnItem 

from .pagination import MyPagination, CustomPagination
from rest_framework import generics, status

from django.db import transaction

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.decorators import login_required

from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

class CartViewSet(viewsets.ModelViewSet):
    def add_item(self, request, book_id=None):
        try:
            with transaction.atomic():
                try:
                    cart_obj = Cart.objects.get(custom_user_id = request.user.uuid)
                except Exception as e:
                    dataset = {'custom_user_id':request.user.uuid}
                    serializer = CartSerializer(data=dataset)
                    
                    if serializer.is_valid(raise_exception=True):
                        cart_obj = serializer.save()
                finally:
                    cart_obj.book_id.add(book_id)
                    response = {
                        'status' : status.HTTP_201_CREATED,
                        'message' : Message.cart_add_item.value,
                        'data' : {'Book ID' : book_id}
                    }
                    return Response(response)

        except Exception as e:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : e
            }
            return Response(response)

    def remove_item(self, request, book_id=None):
        try:
            with transaction.atomic():
                cart_obj = Cart.objects.get(custom_user_id = request.user.uuid)
                cart_obj.book_id.remove(book_id)
                response = {
                    'status' : status.HTTP_202_ACCEPTED,
                    'message' : Message.cart_remove_item.value,
                    'data' : {'Book ID' : book_id}
                }
                return Response(response)
        except Exception as e:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : e
            }
            return Response(response)
    
    def view_cart(self, request):
        try:
            try:
                dataset = Cart.objects.get(custom_user_id = request.user.uuid)
            except:
                msg = "Cart is empty"
                return Response(msg)

            serializer = CartSerializer(dataset)
            response = {
                'status' : status.HTTP_200_OK,
                'data' : serializer.data
            }
            return Response(response)
        except Exception as e:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : e
            }
            return Response(response)
    
    def checkout_cart(self, request):
        try:
            with transaction.atomic():
                cart_obj = Cart.objects.get(custom_user_id = request.user.uuid)
                cart_items = cart_obj.book_id.values()

                serializer = PaymentSerializer(data = request.data)
                if serializer.is_valid(raise_exception=True):
                    payment_id = serializer.save()
                
                order_data = {}
                order_data['user_id'] = request.user.uuid
                order_data['payment_id'] = payment_id.uuid

                serializer_order = OrderSerializer(data = order_data)

                if serializer_order.is_valid(raise_exception=True):
                    order_obj = serializer_order.save()
                
                for id in cart_items:
                    order_obj.book_id.add(id['uuid'])
                    
                book = []
                amount = []
                for items in cart_items:
                    book.append(items['name'])
                    amount.append(items['price'])

                msg = f"For the Book(s) - {book}. Total amount is {sum(amount)}Rs."
                print(msg)
                cart_obj.delete()           #Cart items should be removed after a checkout
                response = {
                    'status' : status.HTTP_201_CREATED,
                    'message' : f"{Message.cart_checkout.value} {msg}",
                    'data' : serializer.initial_data
                }
                return Response(response)

        except Exception as e:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : e
            }
            return Response(response)


class WishListViewSet(viewsets.ModelViewSet):
    def create_wishlist(self, request):
        try:
            with transaction.atomic():
                dataset = {'custom_user_id':request.user.uuid}
                serializer = WishListSerializer(data=dataset)

                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    msg = f" for {request.user.first_name} {request.user.last_name}"
                response = {
                    'status' : status.HTTP_201_CREATED,
                    'message' : f"{Message.wishlist_create.value} {msg}",
                }
                return Response(response)
        except Exception as e:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : e
            }
            return Response(response)

    def add_item(self, request, book_id=None, wishlist_id=None):
        try:
            with transaction.atomic():
                wishlist = WishList.objects.get(uuid=wishlist_id)
                wishlist.book_id.add(book_id)
                response = {
                    'status' : status.HTTP_202_ACCEPTED,
                    'message' : Message.wishlist_add_item.value,
                    'data' : f"Book ID - {book_id}, WishList ID - {wishlist_id}"
                }
                return Response(response)
        except Exception as e:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : e,
                'data' : f"Book - {book_id} cannot be added to {wishlist_id}"
            }
            return Response(response)
        
    def remove_item(self, request, book_id=None, wishlist_id=None):
        try:
            with transaction.atomic():
                wishlist = WishList.objects.get(uuid=wishlist_id)
                wishlist.book_id.remove(book_id)
                response = {
                    'status' : status.HTTP_202_ACCEPTED,
                    'message' : Message.wishlist_remove_item.value,
                    'data' : f"Book ID - {book_id}, WishList ID - {wishlist_id}"
                }
                return Response(response)
        except Exception as e:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : e,
                'data' : f"Book - {book_id} cannot be removed from {wishlist.custom_user_id.first_name}'s wishlist."
            }
            return Response(response)
        
        
class OrderViewSet(MyPagination, viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    pagination_class = MyPagination

    def get_all_order(self, request):
        try:
            dataset = Order.objects.filter(user_id=request.user.uuid)
            dataset = self.paginate_queryset(dataset, request)
            dataset =  self.get_paginated_response(dataset)
            return dataset

        except Exception as e:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : e
            }
            return Response(response)
        

class ReturnItemViewSet(CustomPagination, viewsets.ModelViewSet):
    serializer_class = ReturnItemSerializer
    pagination_class = CustomPagination

    def return_order(self, request, order_id=None):
        try:
            with transaction.atomic():
                print("agya")
                reason = request.data.pop('reason')
                dataset = {'order_id':order_id, 'reason':reason}
                print("dataset", dataset)
                serializer = ReturnItemSerializer(data = dataset)
                if serializer.is_valid(raise_exception=True):
                    print("inside valid")
                    serializer.save()
                response = {
                    'status' : status.HTTP_201_CREATED,
                    'message' : Message.return_order.value,
                    'data' : serializer.data
                }
                return Response(response)
        except Exception as e:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : e
            }
            return Response(response)
        
    def all_returned_order(self, request):
        try:
            with transaction.atomic():
                order = Order.objects.filter(user_id = request.user.uuid).values()

                dataset = []
                for id in order:
                    return_item = ReturnItem.objects.filter(order_id=id['uuid'])
                    if return_item:
                        dataset.append(return_item)

                dataset = self.paginate_queryset(dataset, request)
                
                for data_set in dataset:
                    dataset = self.get_paginated_response(data_set)
                return dataset
                    
        except Exception as e:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : e
            }
            return Response(response)
            
        """Old code for 'all_returned_order' --> Without Pagination"""
        # try:
        #     with transaction.atomic():
        #         order = Order.objects.filter(user_id = request.user.uuid).values()

        #         dataset = []
        #         for id in order:
        #             returnitem = ReturnItem.objects.filter(order_id=id['uuid'])
        #             if returnitem:
        #                 serializer = ReturnItemSerializer(returnitem, many=True)
        #                 dataset.append(serializer.data)

        #         return Response(dataset)
        
            # order = Order.objects.filter(user_id = request.user.uuid)
            # if order.exists():
            #     abc = order.ri_to_order.all()
            #     dataset = OrderSerializer(abc, many=True)