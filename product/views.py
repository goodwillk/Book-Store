from django.shortcuts import render
from rest_framework.views import View

from msg_enum import Message

from django.http import HttpResponse, JsonResponse
from .serializers import ReviewSerializer, BookSerializer
from customer.models import CustomUser
from .models import Review, Book

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from .pagination import CustomPagination

import io
from rest_framework.parsers import JSONParser

@method_decorator(csrf_exempt, name='dispatch')
class ReviewApi(View):
    """CRUD API's for Review models"""
    def post(self, request, product_id=None):
        """API to post a review by currently Logged-In User"""
        try:
            stream = io.BytesIO(request.body)
            data = JSONParser().parse(stream)

            data['custom_user_id'] = request.user.uuid
            data['book_id'] = product_id
            
            serializer = ReviewSerializer(data=data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response = {
                    'status' : status.HTTP_201_CREATED,
                    'message' : Message.review_create.value,
                    'data' : serializer.data
                }
                return JsonResponse(response)
            return HttpResponse(serializer.errors)

        except Exception as e:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : e
            }
            return JsonResponse(response)
    
    def get(self, request):
        """Get all the reviews a logged-in user ever wrote."""
        try:
            dataset = Review.objects.filter(custom_user_id = request.user.uuid)
            serializer = ReviewSerializer(dataset, many=True)
            response = {
                'status' : status.HTTP_200_OK,
                'data' : serializer.data
            }
            return JsonResponse(response)
        except Exception as e:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : e
            }
            return JsonResponse(response)
        
    def patch(self, request, review_id=None):
        """API to update a particular review on a particular product"""
        try:
            stream = io.BytesIO(request.body)
            data = JSONParser().parse(stream)
            
            # user = CustomUser.objects.get(uuid = request.user.uuid)
            # review_instance = user.review_to_cu.get(uuid = review_id)
            """The upper two lines which are commented performs the same work."""
            review_instance = Review.objects.get(uuid = review_id)
            
            serializer = ReviewSerializer(instance=review_instance, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'status' : status.HTTP_202_ACCEPTED,
                    'message' : Message.review_update.value,
                    'data' : serializer.data
                }
                return JsonResponse(response)
            return HttpResponse(serializer.errors)
        except Exception as e:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : e
            }
            return JsonResponse(response)
        
    def delete(self, request, review_id=None):
        """API to delete a review"""
        try:
            review = Review.objects.get(uuid = review_id)
            response = {
                'status' : status.HTTP_200_OK,
                'message' : Message.review_delete.value,
                'data deleted was' : f"rating - {review.rating}, review - {review.description}"
            }
            review.delete()
            return JsonResponse(response)
        except Exception as e:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : e
            }
            return JsonResponse(response)
        

class BookApi(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    pagination_class = CustomPagination
    ordering_fields = ['name', 'author']
    filterset_fields = ['name', 'author']


class PriceRangeFilter(generics.ListAPIView):
    serializer_class = BookSerializer
    filterset_fields = ('price')
    
    def get_queryset(self):
        queryset = Book.objects.all()
        start = self.request.query_params.get('start', None)
        end = self.request.query_params.get('end', None)
        if start and end:
            return queryset.filter(price__range=[start, end]).order_by('-price')