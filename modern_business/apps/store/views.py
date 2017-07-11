from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from .models import Book, Cart, BookOrder, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, UpdateView, DeleteView
from django.http import HttpResponseNotAllowed


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)


class BookListView(ListView):
    model = Book
    template_name = 'store_index.html'
    ordering = 'title'

    def get_queryset(self, **kwargs):
        return super(BookListView, self).get_queryset(**kwargs).all()


class BookDetailView(DetailView):
    model = Book
    template_name = 'store_detail.html'

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['form'] = ReviewForm
        context['review'] = Review.objects.filter(book=kwargs['object'].pk)
        return context



class ReviewUpdate(LoginRequiredMixin, UpdateView):
    model = Review
    template_name = 'store_update_review.html'
    form_class = ReviewForm

    def get_success_url(self, **kwargs):
        return '/'

    def get_context_data(self, **kwargs):
        context = super(ReviewUpdate, self).get_context_data(**kwargs)
        context['book'] = Book.objects.get(pk=self.object.pk)
        return context

    def form_valid(self, form):
        return super(ReviewUpdate, self).form_valid(form)


class ReviewDelete(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'store_delete_review.html'

    def get_success_url(self, **kwargs):
        return '/'

    def get_context_data(self, **kwargs):
        context = super(ReviewDelete, self).get_context_data(**kwargs)
        context['review'] = Review.objects.get(pk=kwargs['object'].pk)
        return context

    def delete(self, request, *args, **kwargs):
        return super(ReviewDelete, self).delete(request, args, kwargs)


@login_required()
def save_form_review(request, pk):
    if request.method == 'POST':
        form_class = ReviewForm
        form = form_class(data=request.POST)
        if form.is_valid():
            new_Review = Review.objects.create(book=Book.objects.get(pk=pk),
                                               user=request.user,
                                               text=request.POST['text'])
            new_Review.save()
            return redirect('/store/book/'+str(pk)+'/')
    else:
        raise HttpResponseNotAllowed('Method not allowed')


@login_required()
def cart(request):
    context = {}
    try:
        total = 0
        cart = Cart.objects.get(user=request.user)
        bookOrder = BookOrder.objects.filter(cart=cart)
        for book in bookOrder:
            if book.quantity > 1:
                sum = book.quantity * book.book.price
            else:
                sum = book.book.price
            total += sum
            context = {
                'order': bookOrder,
                'total': total
            }
    except MultipleObjectsReturned:
        pass
    return render(request, 'store_cart.html', context)


@login_required()
def add_to_cart(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except ObjectDoesNotExist:
        pass
    try:
        cart = Cart.objects.get(user=request.user,
                                   active=True)
        cart.save()
    except ObjectDoesNotExist:
        cart = Cart.objects.create(user=request.user)
        cart.save()
    cart.add_to_cart(book_id=pk)
    return redirect('store:order')


@login_required()
def remove_from_cart(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except ObjectDoesNotExist:
        pass
    cart = Cart.objects.get(user=request.user,
                            active=True)
    cart.remove_from_cart(book_id=pk)
    return redirect('store:order')
