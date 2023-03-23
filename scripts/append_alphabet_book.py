from product.models import Book
BATCH_SIZE=1000

def run():
    test = Book.objects.all()[:BATCH_SIZE]
    ch = 'Z'

    for i in test:
        x = chr(ord(ch) + 1)
        if x=='[':
            ch='A'
            x='A'
        i.name = f"{i.name}-{x}"
        i.save()
        # Book.objects.update(name=i.name)
        # i.update(name=i.name)
        ch=x