from django.db import models
import uuid

class Category(models.Model):
    title = models.CharField(
        max_length=155,
        verbose_name='Название'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категорий'

class Models(models.Model):
    title = models.CharField(
        max_length=155,
        verbose_name='Название'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Category',
        related_name='category',
        blank=True, null=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модел'
        verbose_name_plural = 'Модели'

class Product(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='UUID'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Category',
        related_name='category', 
        blank=True, null=True
    )
    model = models.ForeignKey(
        Models,
        on_delete=models.CASCADE,
        verbose_name='models',
        related_name='models', 
        blank=True, null=True
    )
    title = models.CharField(
        max_length=155,
        verbose_name='Название'
    )
    description = models.TextField(
        verbose_name='Описание товара'
    )
    price = models.IntegerField(
        verbose_name='Цена Товара'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создание'
    )
    size = models.CharField(
        max_length=55,
        verbose_name='Размер'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Продукт'
    )
    image = models.ImageField(
        upload_to='products/',
        verbose_name='Фото продукта'
    )

    class Meta:
        verbose_name = 'Фото продукта'
        verbose_name_plural = 'Фото продуктов'

from django.core.validators import MinValueValidator

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books', null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    published_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

import random
class PasswordResetCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} - {self.code}"