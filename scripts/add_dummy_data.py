from product.models import Book, Genre
BATCHSIZE = 20

def run():
    x=50
    for i in range(0, BATCHSIZE+1):
        Book.objects.create(name=f'temp{i}', author=f'auth-temp{i}', quantity_left=x-17,
                            price=x, genre_id=Genre.objects.get(name='Romantic'))
        x += 10