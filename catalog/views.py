from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from .mixins import ProductCreateUpdateMixin
from .models import Product, Category, Comment, Like
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache


class ProductList(ListView):
    model = Product
    page_kwarg = 12
    template_name = 'catalog/product_list.html'

    def get_context_data(self):
        category_id = self.kwargs.get('category_id')
        current_category = self.get_category(category_id)

        context = {
            'products': self.get_products(category_id, current_category),
            'categories': self.get_categories(),
            'current_category': self.get_category(category_id),
        }

        return context

    @staticmethod
    def get_products_all():
        products = cache.get('products')
        if products is None:
            products = Product.objects.all()
            cache.set('products', products)
        return products

    @staticmethod
    def get_categories():
        categories = cache.get('categories')
        if categories is None:
            categories = Category.objects.all()
            cache.set('categories', categories)
        return categories

    @staticmethod
    def get_category(category_id):
        if category_id is not None:
            category_cache_key = 'category_{}'.format(category_id)
            category = cache.get(category_cache_key)
            if category is None:
                category = get_object_or_404(Category, id=category_id)
                cache.set(category_cache_key, category)
            return category

    def get_products(self, category_id, category):
        if category_id is not None:
            product_category_cache = "products_of_category_{}".format(category_id)
            products_of_category = cache.get(product_category_cache)
            if products_of_category is None:
                products_of_category = category.products.all()
                cache.set(product_category_cache, products_of_category)
            return products_of_category

        return self.get_products_all()


def product_detail(request, product_id):
    product_cache = 'product_{}'.format(product_id)
    product = cache.get(product_cache)
    if product is None:
        product = get_object_or_404(Product, id=product_id)
        cache.set(product_cache, product)

    context = {
        'product': product,
        'comments': product.comments.all()
        }

    return render(request, 'catalog/product_detail.html', context)


class ProductCreateView(ProductCreateUpdateMixin):
    pass


class ProductUpdateView(ProductCreateUpdateMixin):

    def get_form_kwargs(self):
        product_id = self.kwargs['product_id']
        product_cache = 'product_{}'.format(product_id)
        product = cache.get(product_cache)
        if product is None:
            product = get_object_or_404(Product, id=product_id)
        self.kwargs['product'] = product

        return self.kwargs

    def get(self, *args, **kwargs):
        kwargs = self.get_form_kwargs()
        return super().get(*args, *kwargs)

    def post(self, *args, **kwargs):
        kwargs = self.get_form_kwargs()
        return super().post(*args, *kwargs)


@staff_member_required(login_url='catalog:product_list')
def product_delete(request, product_id):
    product = cache.get('product_{}'.format(product_id))
    if product is None:
        product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('catalog:product_list')


def comment_create(request, product_id):
    product = cache.get('product_{}'.format(product_id))
    user = request.user
    if product is None:
        product = get_object_or_404(Product, id=product_id)
    if user.is_active:
        Comment.objects.create(product=product, user=user, text=request.POST.get('text'))
    return redirect('catalog:product_detail', product_id)


def comment_edit(request, comment_id, product_id):
    edit_comment = get_object_or_404(Comment, id=comment_id)
    if request.user == edit_comment.user:
        edit_comment.text = request.POST.get('text')
        edit_comment.updated_date = timezone.now()
        edit_comment.save()
    return redirect('catalog:product_detail', product_id)


def comment_delete(request, comment_id, product_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user or request.user.is_staff:
        comment.delete()
    return redirect('catalog:product_detail', product_id)


def like(request, comment_id, product_id):
    if request.user.is_active:
        Like.objects.create(comment=get_object_or_404(Comment, id=comment_id), user=request.user)

    return redirect('catalog:product_detail', product_id)


def unlike(request, like_id, product_id):
    like_ = get_object_or_404(Like, id=like_id)
    if request.user == like_.user:
        like_.delete()
    return redirect('catalog:product_detail', product_id)


@staff_member_required(login_url='catalog:product_list')
def category_delete(request, id):
    get_object_or_404(Category, id=id).delete()
    return redirect('catalog:product_list')
