from django.core.cache import cache


class CacheDeleteMixin:
    def delete_cache(self):
        if self.__class__.__name__ == 'Category':
            cache.delete_pattern("categories")
        else:
            cache.delete_pattern('products')

    def save(self, *args, **kwargs):
        self.delete_cache()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.delete_cache()
        super().delete(*args, **kwargs)
