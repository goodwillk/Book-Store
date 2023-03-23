from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Address, CustomUser
from .serializers import AddressSerializer, CustomUserSerializer

from msg_enum import Message

from django.middleware.csrf import get_token

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view

from rest_framework.response import Response

import io
from rest_framework import generics, response, status
from rest_framework.views import APIView, View
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from django.db import transaction

@method_decorator(csrf_exempt, name='dispatch')
class CustomUserList(View):
    def post(self, request):
        """API to create a new User"""
        try:
            with transaction.atomic():
                stream = io.BytesIO(request.body)
                data = JSONParser().parse(stream)
                
                address_data = data.pop('address')
                
                serializer_address = AddressSerializer(data=address_data)
                if serializer_address.is_valid(raise_exception=True):
                    uuid_address = serializer_address.save()

                serializer_user = CustomUserSerializer(data=data)
                psd = serializer_user.validate_password(data['password'])
                
                if psd:
                    user = serializer_user.create(data)
                    user.address.add(uuid_address)
                    response = {
                        'status' : status.HTTP_201_CREATED,
                        'message' : Message.customuser_create.value,
                        'data' : f"User Details - {serializer_user.initial_data}, Address Details - {serializer_address.data}"
                    }
                    return JsonResponse(response)
                print("going for serializer.errors")
                return HttpResponse(serializer_user.errors)
        except Exception as e:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : e
            }
            return JsonResponse(response)

    
    # def post(self, request):
    #     """API to create a new User"""
    #     try:
    #         stream = io.BytesIO(request.body)
    #         data = JSONParser().parse(stream)
            
    #         address_data = data.pop('address')
    #         print(address_data)
    #         serializer_address = AddressSerializer(data=address_data)
    #         if serializer_address.is_valid(raise_exception=True):
    #             print("is valid of serializer_address called inside post of Customsuser")
    #             uuid_address = serializer_address.save()
                
    #         print("new address uuid created - ", uuid_address)

    #         data['address'] = str(uuid_address)
    #         # data['address'] = list(uuid_address)
            
    #         print("-----------//-------- >",data)
    #         serializer = CustomUserSerializer(data=data)
    #         print("serializer = ", serializer)
    #         if serializer.is_valid(raise_exception=True):
    #             print("is valid called for user data serializer")
    #         #     msg = "User Created"
    #         #     return HttpResponse(msg)
    #         return HttpResponse(serializer_address.errors)
    #     except Exception as e:
    #         return HttpResponse(e)

    # def post(self, request):
    #     """API to create a new User"""
        # try:
        #     stream = io.BytesIO(request.body)
        #     data = JSONParser().parse(stream)

        #     serializer = CustomUserSerializer(data=data)
        #     print(data)

        #     if serializer.is_valid(raise_exception=True):
        #         print("is valid called")
        #         msg = "User Created"
        #         return HttpResponse(msg)
        #     return HttpResponse(serializer.errors)
        # except Exception as e:
        #     return HttpResponse(e)

    def put(self, request):
        try:
            stream = io.BytesIO(request.body)
            data = JSONParser().parse(stream)
            user = CustomUser.objects.get(uuid=request.user.uuid)
        
            serializer = CustomUserSerializer(instance=user, data=data)
            serializer.update(user, data)
            
            response = {
                'status' : status.HTTP_202_ACCEPTED,
                'message' : Message.customuser_update.value,
                'data' : serializer.initial_data
            }
            return JsonResponse(response)

        except Exception as e:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : e
            }
            return JsonResponse(response)

    def get(self, request):
        """API to get data of user who is currently logged in"""
        try :   
            dataset = CustomUser.objects.get(uuid=request.user.uuid)
            serializer = CustomUserSerializer(dataset)
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

    def delete(self, request):
        """API to delete an existing User"""
        try:
            user = CustomUser.objects.get(uuid=request.user.uuid)
            response = {
                'status' : status.HTTP_202_ACCEPTED,
                'message' : Message.customuser_delete.value,
                "User's Name" : f"{user.first_name} {user.last_name}"
            }
            user.delete()
            return JsonResponse(response)

        except Exception as e:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : e
            }
            return JsonResponse(response)


@method_decorator(csrf_exempt, name='dispatch')
class LogInUser(View):
    def post(self, request):
        """Api for User to Log In"""
        try:
            stream = io.BytesIO(request.body)
            data = JSONParser().parse(stream)
            
            email = data['email']
            password = data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                response_successful = {
                    'status' : status.HTTP_202_ACCEPTED,
                    'message' : Message.login_success.value,
                    "User" : email
                }
                return JsonResponse(response_successful)
            
            response_failure = {
                'status' : status.HTTP_401_UNAUTHORIZED,
                'message' : Message.login_fail.value 
            }
            return JsonResponse(response_failure)

        except Exception as e:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : e
            }
            return JsonResponse(response)


@method_decorator(login_required(login_url='login'), name='dispatch')       #will redirect to login page
class LogOutUser(APIView):
    def get(self, request):
        """Api for User to Log Out"""
        try:
            logout(request)
            response = {
                'status' : status.HTTP_202_ACCEPTED,
                'message' : Message.logout.value
            }
            return JsonResponse(response)
        except Exception as e:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : e
            }
            return JsonResponse(response)


@method_decorator(csrf_exempt, name='dispatch')
class AddressList(View):
    def post(self, request):
        """API to Add another Address Object for an existing user
           Because an address is already given at the time of Creating User
           (A User can have multiple addresses)"""
        try:
            stream = io.BytesIO(request.body)       #Required - As we cannot directly access request.data when
            data = JSONParser().parse(stream)       #   importing from 'View' class

            user = CustomUser.objects.get(uuid=request.user.uuid)

            serializer = AddressSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                address = serializer.save()
                user.address.add(address)
                response = {
                    'status' : status.HTTP_201_CREATED,
                    'message' : Message.address_create.value,
                    "data" : serializer.data
                }
                return JsonResponse(response)
            return HttpResponse(serializer.errors)
        except Exception as e:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : e
            }
            return JsonResponse(response)

    def put(self, request, house_no=None):
        """Update a specific address object(Using house_no) of currently logged-in user"""
        try:
            stream = io.BytesIO(request.body)
            dataset = JSONParser().parse(stream)

            user = CustomUser.objects.get(uuid=request.user.uuid)
            address = user.address.get(house_no=house_no)

            serializer = AddressSerializer(address)
            data = serializer.update(address, dataset)

            if data:
                response = {
                    'status' : status.HTTP_202_ACCEPTED,
                    'message' : Message.address_update.value,
                    "data" : serializer.initial_data
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
        """API to get all address objects of a user who is currently logged in"""  
        try:  
            user = CustomUser.objects.get(uuid=request.user.uuid)
            dataset = user.address.all()
            
            serializer = AddressSerializer(dataset, many=True)
            response = {
                'status' : status.HTTP_200_OK,
                "data" : serializer.data
            }
            return JsonResponse(response)

        except Exception as e:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : e
            }
            return JsonResponse(response)

    def delete(self, request, house_no=None):
        """API to delete a specific address(Using house_no) of currently logged in user
           Because a user can have multiple addresses stored and the user wants to delete 
           a particular address & not all the addresses"""
        try:
            user = CustomUser.objects.get(uuid=request.user.uuid)
            address = user.address.get(house_no=house_no)
            
            response = {
                'status' : status.HTTP_200_OK,
                'message' : Message.address_delete.value,
                "data" : f"{address.type} {address.house_no}"
            }
            address.delete()
            return JsonResponse(response)

        except Exception as e:
            response = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'error' : e
            }
            return JsonResponse(response)