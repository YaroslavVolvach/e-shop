from rest_framework import serializers
from catalog.models import Product, Category, Comment, Like


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['title', 'image', 'category', 'description', 'price', 'quantity', 'images', 'comments', 'id']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category

        fields = ['title', 'products', 'id']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['product', 'user', 'text', 'created_date', 'updated_date', 'id']
        read_only_fields = ('created_date', 'updated_date')


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['comment', 'user', 'id']
