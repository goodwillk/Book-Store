from django.db import models
from customer.models import BaseModel, CustomUser

from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(BaseModel):
    name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name


class Book(BaseModel):
    name = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    price = models.IntegerField()
    quantity_left = models.SmallIntegerField()
    genre_id = models.ForeignKey(Genre, related_name='book_to_genre', on_delete = models.CASCADE)
    
    def __str__(self):
        return f"{self.name} By {self.author}"


class Review(BaseModel):
    custom_user_id = models.ForeignKey(CustomUser, related_name='review_to_cu', on_delete = models.CASCADE)
    rating = models.SmallIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(max_length=1500)
    book_id = models.ForeignKey(Book, default=0, related_name='review_to_book', on_delete=models.CASCADE)
