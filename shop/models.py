from django.db import models
import uuid
from django.urls import reverse


class Type(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank = True)
    image = models.ImageField(upload_to = 'type', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'type'
        verbose_name_plural = 'types'

    def get_absolute_url(self):
        return reverse('shop:products_by_type', args=[self.id])

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank = True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to = 'product', blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, blank = True, null= True
)
    updated = models.DateTimeField(auto_now=True, blank = True, null= True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.type.id, self.id]
    )

    def __str__(self):
        return self.name


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    stars = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    