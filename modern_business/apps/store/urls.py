from django.conf.urls import url
from django.views.generic import TemplateView

from . import views
from .views import BookDetailView, BookListView, ReviewUpdate, ReviewDelete

app_name = 'store'
urlpatterns = [
    url(r'^$', BookListView.as_view(), name='book_main'),
    url(r'^book/(?P<pk>[\d]+)/$', BookDetailView.as_view(), name='book_detail'),
    url(r'^cart/', views.cart, name='order'),
    url(r'^add/(?P<pk>[\d]+)/$', views.add_to_cart, name='add_cart'),
    url(r'^remove/(?P<pk>[\d]+)/$', views.remove_from_cart, name='remove_cart'),
    url(r'^save_review/(?P<pk>[\d]+)/$', views.save_form_review, name='save_review'),
    url(r'^update_review/(?P<pk>[\d]+)/$', ReviewUpdate.as_view(), name='update_review'),
    url(r'^delete_review/(?P<pk>[\d]+)/$', ReviewDelete.as_view(), name='delete_review'),
]
