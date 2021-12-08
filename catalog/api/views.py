from .permission import IsOwnerOrReadOnly, AdminOrReadonlyPermission
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import ProductSerializer, CategorySerializer, LikeSerializer, CommentSerializer
from catalog.models import Product, Category, Comment, Like
from rest_framework import viewsets


class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.filter().order_by('id')
    permission_classes = [AdminOrReadonlyPermission]


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminOrReadonlyPermission]
    serializer_class = CategorySerializer
    queryset = Category.objects.filter().order_by('id')


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.filter().order_by('id')
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.filter().order_by('id')
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
