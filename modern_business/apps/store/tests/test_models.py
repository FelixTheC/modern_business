from django.test import TestCase
from store.models import Author, Book


class StoreTest(TestCase):
    def setUp(self):
        author = Author.objects.create(first_name='felix', last_name='test')
        mybook = Book.objects.create(title='MyBook', author=author, description='Only a test not for public',
                                     price=12.95, stock=100)

    def test_book_exists(self):
        loadBook = Book.objects.get(title='MyBook')
        self.assertTrue(loadBook)

    def test_fail_update(self):
        pass
