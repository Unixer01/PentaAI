class Book:
    def __init__(self, pages, author, title):
        self.pages = pages
        self.author = author
        self.contentlist = []
        self.title = title
        i = 0
        for i in range(self.pages):
            self.contentlist.append('')

    def __len__(self):
        return self.pages

    def write(self, content, pageno):
        self.contentlist.insert(int(pageno)-1, content)

    def show(self):
        for i in range(len(self.contentlist)):
            print(self.contentlist[i])



book = Book(320, "xXx", 'Test')
print(len(book), book.author)
book.write('Hello', "9")
book.show()