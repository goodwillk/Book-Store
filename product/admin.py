from django.contrib import admin
from .models import Review, Book, Genre
# Register your models here.
class CustomBook(admin.ModelAdmin):
    model = Book
    list_display = ('name', 'author', 'price', 'genre_id', 'quantity_left',)

class CustomGenre(admin.ModelAdmin):
    model = Genre
    list_display = ('name', )

class CustomReview(admin.ModelAdmin):
    model = Review

admin.site.register(Review, CustomReview)
admin.site.register(Book, CustomBook)
admin.site.register(Genre, CustomGenre)