from django.db import models
from django.urls import reverse
from django.utils import timezone
from account.models import CustomUser
from .model_mixins import CacheDeleteMixin


class Category(CacheDeleteMixin, models.Model):
    title = models.CharField(max_length=150, unique=True)

    def get_absolute_url(self):
        return reverse('catalog:select_category', args=[self.id])

    def __str__(self):
        return self.title


class Product(CacheDeleteMixin, models.Model):
    title = models.CharField(max_length=20)
    image = models.ImageField(
        upload_to='product_image/product_photo/main_photo/',
        default='product_image/default_image/default-no-image.png'
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def get_absolute_url(self):
        return reverse('catalog:product_detail', args=[self.id])

    def __str__(self):
        return self.title


class Gallery(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_image/product_photo/')

    def __str__(self):
        return '{}'.format(self.image)


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=1000)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(null=True)

    def __str__(self):
        return '{}...'.format(self.text[:5])


class Like(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return 'Like {}'.format(self.id)
