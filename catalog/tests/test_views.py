from django.test import TestCase
from catalog import models
from django.urls import reverse
from django.core.cache import cache


class CreateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for number in range(1, 11):
            product = models.Product.objects.create(
                title='Product:{}'.format(number),
                description='Nice',
                price=1000,
                quantity=10
            )
            category = models.Category.objects.create(title="Category:{}".format(number))
            category.products.set([product])
            models.Gallery.objects.create(product=product, image='product_image/default_image/default-no-image.png')

    def tearDown(self):
        cache.delete_pattern("categories")
        cache.delete_pattern("products")


class ProductListViewTest(CreateViewTest):
    def test_view_url_exists_at_desired_location(self):
        self.assertEqual(self.client.get('').status_code, 200)

    def test_view_url_exists_at_accessible_by_name(self):
        response = self.client.get(reverse('catalog:product_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        self.assertTemplateUsed((self.client.get(''), 'catalog/product_list.html'))

    def test_view_list(self):
        all_product_ = self.client.get('').context['products']
        all_product = models.Product.objects.all()
        self.assertEqual(all_product_.__class__, all_product.__class__)
        self.assertEqual(all_product_.count(), all_product.count())

    def test_view_category_list(self):
        all_categories_list = self.client.get('').context['categories'].count()
        all_categories_count = models.Category.objects.all().count()
        self.assertEqual(all_categories_list, all_categories_count)


class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.product = models.Product.objects.create(title='Watch', description='Nice', price=1000, quantity=10)
        self.user = models.CustomUser.objects.create_user(
            email='product_delete_test@gmail.com',
            password='secret',
            user_name='ProductDeleteTest'
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('catalog:product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_accessible_by_name(self):
        response = self.client.get(reverse('catalog:product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('catalog:product_detail', args=[self.product.id]))
        self.assertTemplateUsed(response, 'catalog/product_detail.html')

    def test_context_view(self):
        response = self.client.get(reverse('catalog:product_detail', args=[self.product.id]))
        product = models.Product.objects.get(id=self.product.id)
        self.assertEqual(response.context['product'], product)

    def test_comment_view(self):
        response = self.client.get(reverse('catalog:product_detail', args=[self.product.id]))
        product = models.Product.objects.get(id=self.product.id)
        comments = response.context['comments']
        self.assertQuerysetEqual(comments, product.comments.all())


class ProductDeleteTest(TestCase):
    def setUp(self):
        self.product = models.Product.objects.create(title='Watch', description='Nice', price=1000, quantity=10)
        self.user = models.CustomUser.objects.create_user(
            email='product_delete_test@gmail.com',
            password='secret',
            user_name='ProductDeleteTest'
        )
        self.comment = models.Comment.objects.create(
            product=self.product,
            user=self.user,
            text='Comment for Django test'
        )

    def test_delete_view_anonymous(self):
        response = self.client.get(reverse('catalog:product_delete', args=[self.product.id]))
        self.assertTrue(models.Product.objects.filter(id=self.product.id).exists())
        self.assertEqual(response.status_code, 302)

    def test_delete_view_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('catalog:product_delete', args=[self.product.id]))
        self.assertTrue(models.Product.objects.filter(id=self.product.id).exists())
        self.assertEqual(response.status_code, 302)

    def test_delete_view_staff(self):
        self.user.is_staff = True
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.get(reverse('catalog:product_delete', args=[self.product.id]))
        self.assertFalse(models.Product.objects.filter(id=self.product.id).exists())
        self.assertRedirects(response, '/', 302, 200)


class CommentViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = models.Product.objects.create(title='Watch', description='Nice', price=1000, quantity=10)
        cls.user = models.CustomUser.objects.create_user(email='jon@gmail.com', password='secret', user_name='Jon')
        cls.text = {'text': 'Test'}

    def setUp(self):
        user = self.user
        product = self.product
        self.comment = models.Comment.objects.create(product=product, user=user, text='Comment for Django test')

    def test_comment_create_for_anonymous_user(self):
        product = self.product
        comment_count = models.Comment.objects.all().count()
        response = self.client.post(reverse('catalog:comment_create',  args=[product.id]), self.text)

        create_by_anonymous = models.Comment.objects.all().count()

        self.assertFalse(create_by_anonymous > comment_count)
        self.assertRedirects(response, reverse('catalog:product_detail', args=[product.id]), 302, 200)

    def test_comment_create_for_authenticated_user(self):
        comment_count = models.Comment.objects.all().count()
        self.client.force_login(self.user)
        response = self.client.post(reverse('catalog:comment_create', args=[self.product.id]), self.text)
        create_by_anonymous = models.Comment.objects.all().count()

        self.assertTrue(create_by_anonymous > comment_count)
        self.assertRedirects(response, reverse('catalog:product_detail', args=[self.product.id]), 302, 200)

    def test_comment_edit_for_anonymous_user(self):
        text = {'text': 'Edit Test'}
        response = self.client.post(reverse('catalog:comment_edit', args=[self.comment.id, self.product.id]), text)

        self.comment.refresh_from_db()
        self.assertNotEqual(self.comment.text, 'Edit Test')
        self.assertRedirects(response, reverse('catalog:product_detail', args=[self.product.id]), 302, 200)

    def test_comment_edit_for_authenticated_user(self):
        text = {'text': 'Edit Test'}

        self.client.force_login(self.user)
        response = self.client.post(reverse('catalog:comment_edit', args=[self.comment.id, self.product.id]), text)

        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text, 'Edit Test')
        self.assertRedirects(response, reverse('catalog:product_detail', args=[self.product.id]), 302, 200)

    def test_comment_delete_for_anonymous_user(self):
        response = self.client.post(reverse('catalog:comment_delete', args=[self.comment.id, self.product.id]))

        self.assertTrue(models.Comment.objects.filter(id=self.comment.id))

        self.assertRedirects(response, reverse('catalog:product_detail', args=[self.product.id]), 302, 200)

    def test_comment_delete_for_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('catalog:comment_delete', args=[self.comment.id, self.product.id]))

        self.assertFalse(models.Comment.objects.filter(id=self.comment.id))
        self.assertRedirects(response, reverse('catalog:product_detail', args=[self.product.id]), 302, 200)


class LikeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = models.Product.objects.create(title='Watch', description='Nice', price=1000, quantity=10)
        cls.user = models.CustomUser.objects.create_user(email='jon@gmail.com', password='secret', user_name='Jon')
        cls.comment = models.Comment.objects.create(product=cls.product, user=cls.user, text='Comment for Django test')
        cls.like = models.Like.objects.create(comment=cls.comment, user=cls.user)

    def like_comment_create_for_anonymous_user(self):
        like_count = models.Like.objects.all().count()
        response = self.client.post(reverse('catalog:like', args=[self.comment.id, self.product.id]))

        create_by_anonymous = models.Like.objects.all().count()

        self.assertFalse(create_by_anonymous > like_count)
        self.assertRedirects(response, reverse('catalog:product_detail', args=[self.product.id]), 302, 200)

    def like_comment_create_for_authenticated_user(self):
        like_count = models.Like.objects.all().count()
        self.client.force_login(self.user)
        response = self.client.post(reverse('catalog:like', args=[self.comment.id, self.product.id]))

        create_by_anonymous = models.Like.objects.all().count()

        self.assertTrue(create_by_anonymous > like_count)
        self.assertRedirects(response, reverse('catalog:product_detail', args=[self.product.id]), 302, 200)

    def test_unlike_for_anonymous_user(self):
        response = self.client.post(reverse('catalog:unlike', args=[self.like.id, self.product.id]))

        self.assertTrue(models.Like.objects.filter(id=self.like.id))
        self.assertRedirects(response, reverse('catalog:product_detail', args=[self.product.id]), 302, 200)

    def test_unlike_for_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('catalog:unlike', args=[self.like.id, self.product.id]))

        self.assertFalse(models.Like.objects.filter(id=self.like.id))
        self.assertRedirects(response, reverse('catalog:product_detail', args=[self.product.id]), 302, 200)


class CategoryViewTest(TestCase):
    def setUp(self):
        self.user = models.CustomUser.objects.create_user(email='jon@gmail.com', password='secret', user_name='Jon')
        self.category = models.Category.objects.create(title='Test')

    def test_category_delete_for_no_staff(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('catalog:category_delete', args=[self.category.id]))
        self.assertTrue(models.Category.objects.filter(id=self.category.id).exists())
        self.assertRedirects(response, '/?next=%2Fcategory_delete%2F1', 302, 200)

    def test_category_delete_for_staff(self):
        self.user.is_staff = True
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.post(reverse('catalog:category_delete', args=[self.category.id]))
        self.assertFalse(models.Category.objects.filter(id=self.category.id))
        self.assertRedirects(response, '/', 302, 200)
