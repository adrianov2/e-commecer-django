from rest_framework import serializers
from .models import Product

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
