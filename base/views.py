from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from .models import Product,ProductCategory
from .serializers import ProductSerializer,ProductCategorySerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class ProductApiView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductCategoryApiView(GenericViewSet):

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