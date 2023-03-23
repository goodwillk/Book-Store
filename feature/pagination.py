from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import ModelSerializer
from .serializers import OrderSerializer, ReturnItemSerializer
from rest_framework import status
from rest_framework.response import Response

class MyPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 2

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'status' : status.HTTP_200_OK,
            'total pages': self.page.paginator.count,
            'current page': int(self.request.GET.get('page', 1)), 
            'page size': int(self.request.GET.get('page_size', self.page_size)),
            'order details': OrderSerializer(data, many=True).data
        })
        

class CustomPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 2

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'status' : status.HTTP_200_OK,
            'total pages': self.page.paginator.count,
            'current page': int(self.request.GET.get('page', 1)), 
            'page size': int(self.request.GET.get('page_size', self.page_size)),
            'order details': ReturnItemSerializer(data, many=True).data
        })