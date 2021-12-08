from django.urls import path, include
from . import views as api_view

from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('products', api_view.ProductViewSet),
router.register('category', api_view.CategoryViewSet),
router.register('comment', api_view.CommentViewSet),
router.register('like', api_view.LikeViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls))
]
