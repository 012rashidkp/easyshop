from rest_framework import viewsets
from . import models
from . import serializers 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ProductViewset(viewsets.ModelViewSet):
    queryset = models.Products.objects.all()
    serializer_class = serializers.ProductSerializer
    
  
    
    
    
