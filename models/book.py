class Book():
    def __init__(self, title, price, author, publisher):
        self.title = title
        self.price = price
        self.author = author
        self.publisher = publisher

    def __str__(self):
        return f'<book{self.title}>'
