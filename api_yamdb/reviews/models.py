from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.constants import ROLES


class User(AbstractUser):

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=15, choices=ROLES, null=True)
    bio = models.TextField(max_length=200, blank=True, null=True)
    confirmation_code = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(max_length=150)
    year = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=250, blank=True)
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
