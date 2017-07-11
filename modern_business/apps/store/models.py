from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from cms.models.fields import PlaceholderField
from django.core.urlresolvers import reverse
from django.utils import timezone


def image_upload_path(instance, filename):
    return '/'.join(['images', str(instance.name), filename])


class Author(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        return "{0}, {1}".format(self.first_name, self.last_name)


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author)
    description = models.TextField()
    placeholder_description = PlaceholderField(slotname='description', null=False, blank=False)
    publish_date = models.DateField(default=timezone.now)
    cover = models.ImageField(upload_to=image_upload_path, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('store:book_detail',
                       kwargs={'pk': str(self.pk)})


class Review(models.Model):
    book = models.ForeignKey(Book)
    user = models.ForeignKey(User)
    publish_date = models.DateField(default=timezone.now)
    text = models.TextField()

    def get_update_url(self):
        return reverse('store:update_review',
                       kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('store:delete_review',
                       kwargs={'pk': self.pk})


class Cart(models.Model):
    user = models.ForeignKey(User)
    active = models.BooleanField(default=True)
    order_date = models.DateField(null=True)
    payment_type = models.CharField(max_length=100, null=True)
    payment_id = models.CharField(max_length=100, null=True)

    def add_to_cart(self, book_id):
        _book = Book.objects.get(pk=book_id)
        try:
            preexisting_order = BookOrder.objects.get(book=_book, cart=self)
            preexisting_order.quantity += 1
            preexisting_order.save()
        except ObjectDoesNotExist:
            new_order = BookOrder.objects.create(
                book=_book,
                cart=self,
                quantity=1
            )
            new_order.save()

    def remove_from_cart(self, book_id):
        _book = Book.objects.get(pk=book_id)
        try:
            preexisting_order = BookOrder.objects.get(book=_book, cart=self)
            if preexisting_order.quantity > 1:
                preexisting_order.quantity -= 1
                preexisting_order.save()
            else:
                preexisting_order.delete()
        except BookOrder.DoesNotExist:
            pass


class BookOrder(models.Model):
    book = models.ForeignKey(Book)
    cart = models.ForeignKey(Cart)
    quantity = models.IntegerField()
