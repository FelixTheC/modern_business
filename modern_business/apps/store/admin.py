from django.contrib import admin
from .models import Author, Book, Review, Cart, BookOrder


# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
        list_display = ['first_name', 'last_name']


class BookAdmin(admin.ModelAdmin):
        list_display = ['title', 'author', 'stock']


class ReviewAdmin(admin.ModelAdmin):
        list_display = ['book', 'user', 'publish_date']


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookOrder)
admin.site.register(Cart)
admin.site.register(Review, ReviewAdmin)
