from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from .models import Product,ProductCategory
from .serializers import ProductSerializer,ProductCategorySerializer,UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.core.mail import send_mail

# Create your views here.
class ProductApiView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']

class ProductCategoryApiView(GenericViewSet):
    permission_classes = [IsAuthenticated]

    def list(self,request):
        product_category_objs = ProductCategory.objects.all()
        serializer = ProductCategorySerializer(product_category_objs,many=True)
        return Response(serializer.data)
    
    def create(self,request):
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def update(self,request,pk):
        try:
            product_category_obj = ProductCategory.objects.get(id=pk)
        except:
            return Response({'detail':'No matching data found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = ProductCategorySerializer(product_category_obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self,request,pk):
        try:
            product_category_obj = ProductCategory.objects.get(id=pk)
        except:
            return Response({'detail':'No matching data found!'},status=status.HTTP_404_NOT_FOUND)
        product_category_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def retrieve(self,request,pk):
        try:
            product_category_obj = ProductCategory.objects.get(id=pk)
        except:
            return Response({'detail':'No matching data found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = ProductCategorySerializer(product_category_obj)
        return Response(serializer.data)
    
@api_view(['POST'])
def register_api_view(request):
    password = request.data.get('password')
    hash_password = make_password(password)
    data = request.data.copy()
    data['password'] = hash_password
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        email = request.data.get('email')
        send_mail(subject='Welcome to IMS application',message='You have succesfully registered into our IMS application.',from_email='surubasnet824@gmail.com',recipient_list=[email])
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def login_api_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username,password=password)

    if user == None:
        return Response({'detail':'Invalid credentials'},status=status.HTTP_400_BAD_REQUEST)
    else:
        token,_ = Token.objects.get_or_create(user=user)
        return Response(token.key)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout_api_view(request):
    user = request.user
    token = Token.objects.get(user=user)
    token.delete()
    return Response()