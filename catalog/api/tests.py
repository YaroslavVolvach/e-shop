from rest_framework.test import APITestCase
from rest_framework import status
from account.models import CustomUser
from catalog.models import Product, Category, Comment, Like


class CatalogAPITest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@gmail.com', user_name='Test_name', password='*qwerty#')
        self.staff = CustomUser.objects.create_staff(
            email='stafftest@gmail.com',
            user_name='Staff',
            password='*qwerty#',
        )


class ProductAPITest(CatalogAPITest):

    def setUp(self):
        self.product = Product.objects.create(title='Watch', description='Nice', price=1000, quantity=10)
        self.data = {'title': 'Car', 'description': 'Nice', 'price': 1000, 'quantity': 10}
        super().setUp()

    def test_product_list(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_detail(self):
        response = self.client.get('/api/products/{}/'.format(self.product.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_create_api_anonymous(self):
        response = self.client.post('/api/products/', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.json())

    def test_product_create_api_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.post('/api/products/', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.json())

    def test_product_create_api_staff(self):
        self.client.force_authenticate(self.staff)
        response = self.client.post('/api/products/', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())

    def test_product_delete_api_anonymous(self):
        response = self.client.delete('/api/products/{}/'.format(self.product.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.json())

    def test_product_delete_api_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete('/api/products/{}/'.format(self.product.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.json())

    def test_product_delete_api_staff(self):
        self.client.force_authenticate(self.staff)
        response = self.client.delete('/api/products/{}/'.format(self.product.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_product_update_api_anonymous(self):
        product = self.product
        response = self.client.put('/api/products/{}/'.format(product.id), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_update_api_user(self):
        self.client.force_authenticate(self.user)
        product = self.product
        response = self.client.put('/api/products/{}/'.format(product.id), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_product_update_api_staff(self):
        self.client.force_authenticate(user=self.staff)
        product = self.product
        response = self.client.put('/api/products/{}/'.format(product.id), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CategoryAPITest(CatalogAPITest):
    @classmethod
    def setUpTestData(cls):
        cls.data = {'title': 'New_category_name_test'}

    def setUp(self):
        self.category = Category.objects.create(title='CategoryTest')
        super().setUp()

    def test_category_list(self):
        response = self.client.get('/api/category/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_detail(self):
        response = self.client.get('/api/category/{}/'.format(self.category.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_create_api_anonymous(self):
        response = self.client.post('/api/category/', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.json())

    def test_category_create_api_no_staff(self):
        self.client.force_authenticate(self.user)
        response = self.client.post('/api/category/', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.json())

    def test_category_create_api_staff(self):
        self.client.force_authenticate(self.staff)
        response = self.client.post('/api/category/', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())

    def test_category_delete_api_anonymous(self):
        response = self.client.delete('/api/category/{}/'.format(self.category.id), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.json())

    def test_category_delete_api_no_staff(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete('/api/category/{}/'.format(self.category.id), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.json())

    def test_category_delete_api_staff(self):
        self.client.force_authenticate(self.staff)
        response = self.client.delete('/api/category/{}/'.format(self.category.id), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_category_update_api_anonymous(self):
        response = self.client.put('/api/category/{}/'.format(self.category.id), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_category_update_api_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.put('/api/category/{}/'.format(self.category.id),  data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_update_api_staff(self):
        self.client.force_authenticate(self.staff)
        response = self.client.put('/api/category/{}/'.format(self.category.id), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CommentAPITest(CatalogAPITest):
    def setUp(self):
        super().setUp()
        self.product = Product.objects.create(title='Watch', description='Nice', price=1000, quantity=10)
        self.comment = Comment.objects.create(user=self.user, product=self.product, text='Descriipton')
        self.data = {'user': self.user.id, 'product': self.product.id, 'text': 'New decription'}

    def test_comment_list(self):
        response = self.client.get('/api/comment/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_detail(self):
        response = self.client.get('/api/comment/{}/'.format(self.comment.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_create_api_anonymous(self):
        response = self.client.post('/api/comment/', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.json())

    def test_comment_create_api_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.post('/api/comment/', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())

    def test_comment_create_api_staff(self):
        self.client.force_authenticate(self.staff)
        response = self.client.post('/api/comment/', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())

    def test_comment_delete_api_anonymous(self):
        response = self.client.delete('/api/comment/{}/'.format(self.comment.id), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.json())

    def test_comment_delete_api_user_and_not_owner(self):
        comment = self.comment
        comment.user = self.staff
        comment.save()
        self.client.force_authenticate(self.user)
        response = self.client.delete('/api/comment/{}/'.format(comment.id), data=self.data)
        self.assertFalse(comment.user == self.user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_delete_api_owner(self):
        comment = self.comment
        user = self.user
        self.client.force_authenticate(user)
        response = self.client.delete('/api/comment/{}/'.format(comment.id), data=self.data)
        self.assertTrue(comment.user == user)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_comment_delete_api_staff(self):
        self.client.force_authenticate(self.staff)
        response = self.client.delete('/api/comment/{}/'.format(self.comment.id), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_comment_update_api_anonymous(self):
        response = self.client.put('/api/comment/{}/'.format(self.comment.id), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_update_api_owner(self):
        user = self.user
        comment = self.comment
        self.client.force_authenticate(user)
        response = self.client.put('/api/comment/{}/'.format(comment.id), data=self.data)
        self.assertTrue(comment.user == user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_update_api_staff_not_owner(self):
        staff = self.staff
        comment = self.comment
        self.client.force_authenticate(staff)
        response = self.client.put('/api/comment/{}/'.format(comment.id), data=self.data)
        self.assertFalse(comment.user == staff)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_update_api_staff_owner(self):
        staff = self.staff
        comment = self.comment
        comment.user = staff
        comment.save()
        self.client.force_authenticate(staff)
        response = self.client.put('/api/comment/{}/'.format(comment.id), data=self.data)
        self.assertTrue(comment.user == staff)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LikeApiTest(CatalogAPITest):
    def setUp(self):
        super().setUp()
        self.product = Product.objects.create(title='Watch', description='Nice', price=1000, quantity=10)
        self.comment = Comment.objects.create(user=self.user, product=self.product, text='Descriipton')
        self.like = Like.objects.create(user=self.user, comment=self.comment)

    def test_like_list(self):
        response = self.client.get('/api/like/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tect_like_create_api_anonymous(self):
        response = self.client.post('/api/like/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def tect_like_create_api_user(self):
        user = self.user
        self.client.force_authenticate(user)
        response = self.client.post('/api/like/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def tect_like_create_api_staff(self):
        self.client.force_authenticate(self.staff)
        response = self.client.post('/api/like/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_like_delete_api_anonymous(self):
        response = self.client.delete('/api/like/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tect_like_delete_api_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete('/api/like/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def tect_like_delete_api_staff(self):
        self.client.force_authenticate(self.staff)
        response = self.client.delete('/api/like/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
