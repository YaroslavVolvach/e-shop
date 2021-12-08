from django.test import TestCase

from django.urls import reverse
from catalog.models import Product, Category, Gallery, Comment
from account.models import CustomUser


class ModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.product = Product.objects.create(title='Submariner', description='Nice', price=1000, quantity=10)
        cls.category = Category.objects.create(title="Rolex")
        cls.category.products.set([cls.product])
        cls.category.save()

        cls.gallery = Gallery.objects.create(
            product=cls.product,
            image='product_image/default_image/default-no-image.png'
        )
        cls.user = CustomUser.objects.create_user(email='jon@gmail.com', password='secret', user_name='Jon')

        cls.comment = Comment.objects.create(product=cls.product, user=cls.user, text='Comment for Django test')


class ModelProductTest(ModelTest):
    def test_product_str_method(self):
        self.assertEquals(self.product.__str__(), self.product.title)

    def test_product_get_absolute_url(self):
        self.assertEquals(self.product.get_absolute_url(), reverse('catalog:product_detail', args=[self.product.id]))


class ModelCategoryTest(ModelTest):

    def test_category_str_method(self):
        self.assertEquals(self.category.__str__(), self.category.title)

    def test_product_get_absolute_url(self):
        self.assertEquals(self.category.get_absolute_url(), reverse('catalog:select_category', args=[self.category.id]))


class ModelGalleryTest(ModelTest):
    def test_gallery_str_method(self):
        self.assertEquals(self.gallery.__str__(), str(self.gallery.image))


class ModelCommentTest(ModelTest):
    def test_comment_str_method(self):
        comment = self.comment
        self.assertEquals(comment.__str__(), '{}...'.format(comment.text[:5]))
