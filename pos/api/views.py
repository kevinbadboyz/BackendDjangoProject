from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import (
    RegisterUserSerializer,
    TableRestoSerializer, CategorySerializer, CategoryCreateSerializer, MenuRestoSerializer,
    MenuRestoFilterSerializer, 
    OrderCreateSerializer, OrderSerializer, OrderInfoSerializer,
    OrderDetailCreateSerializer
)
from pos_app.models import TableResto, Category, MenuResto, Order, OrderDetail
from rest_framework import generics
from .paginators import CustomPagination
from rest_framework import filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import login as django_login, logout as django_logout
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny

# If you are using from django.contrib.auth.models import User
class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data,
            context = {'request' : request})
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user = user)
        return JsonResponse({
            'status' : 200,
            'message' : 'Selamat anda berhasil masuk',
            'data' : {
                'token' : token.key,
                'id' : user.id,
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'email' : user.email,
                'is_active' : user.is_active,
            }
        })

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

class TableRestoListCreateAPIView(APIView):
    def get(self, request, format=None):
        table_resto = TableResto.objects.all()
        serializer = TableRestoSerializer(table_resto, many=True)
        return Response(serializer.data) 
    
    def post(self, request, format=None):
        serializer = TableRestoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TableRestoDetailAPIView(APIView):
    def get_object(self, id):
        try:
            return TableResto.objects.get(id = id)
        except TableResto.DoesNotExist:
            return None
        
    
    def get(self, request, id, *args, **kwargs):
        table_resto_instance = self.get_object(id)
        # Check the data is exist or not
        if not table_resto_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Data does not exist...',
                    'data' : {}
                }, status = status.HTTP_400_BAD_REQUEST
            )
        serializer = TableRestoSerializer(table_resto_instance)
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'Data retrieve successfully...',
            'data' : serializer.data
        }
        return Response(response, status = status.HTTP_200_OK)
    

    def put(self, request, id, *args, **kwargs):
        table_resto_instance = self.get_object(id)
        # Check the data is exist or not
        if not table_resto_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Data does not exist...',
                    'data' : {}
                }, status = status.HTTP_400_BAD_REQUEST
            )
        data = {
            'name' : request.data.get('name'),
            'capacity' : request.data.get('capacity'),
            'table_status' : request.data.get('table_status'),
            'status' : request.data.get('status'),
        }
        serializer = TableRestoSerializer(
            table_resto_instance,
            data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_200_OK,
                'message' : 'Data updated successfully...',
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_200_OK)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, *args, **kwargs):
        table_resto_instance = self.get_object(id)
        if not table_resto_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Data does not exist...',
                    'data' : {}
                }, status = status.HTTP_400_BAD_REQUEST
            )
        
        table_resto_instance.delete()
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'Data deleted successfully...'
        }
        return Response(response, status = status.HTTP_200_OK)
    
class TableRestoListAPIView(generics.ListAPIView):
    queryset = TableResto.objects.all()
    serializer_class = TableRestoSerializer

class TableRestoCreateAPIView(generics.CreateAPIView):
    queryset = TableResto.objects.all()
    serializer_class = TableRestoSerializer

class TableRestoInfoAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TableResto.objects.all()
    serializer_class = TableRestoSerializer

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer

class MenuRestoListAPIView(generics.ListCreateAPIView):
    queryset = MenuResto.objects.all()
    serializer_class = MenuRestoSerializer
    # permission_classes = [IsAuthenticated]

class MenuRestoFilterApi(generics.ListAPIView):
    queryset = MenuResto.objects.all()
    serializer_class = MenuRestoFilterSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category__name']
    ordering_fields = ['created_on']
    # permission_classes = [IsAuthenticated]

class OrderListApiView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderCreateApiView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer

class OrderInfoApiView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderInfoSerializer

class OrderDeleteApiView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer