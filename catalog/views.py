from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name = 'html/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class BookDetailView(generic.DetailView):

    model = Book
    template_name = 'html/book_detail.html'


class AuthorDetailView(generic.DetailView):

    model = Author
    template_name = 'html/author-detail.html'


class BookListView(generic.ListView):

    model = Book
    context_object_name = 'book_list'
    template_name = 'html/book_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.all()[:5]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        return context


def index(request):

    num_of_books = Book.objects.all().count()
    num_of_instances = BookInstance.objects.all().count()
    num_of_available_instances = BookInstance.objects.filter(status__exact='a').count()
    num_of_authors = Author.objects.all().count()
    request.session.setdefault('num_of_visits', 0)
    request.session['num_of_visits'] += 1
    request.session.modified = True
    return render(request, 'html/index.html', context={
        'num_of_books': num_of_books,
        'num_of_instances': num_of_instances,
        'num_of_available_instances': num_of_available_instances,
        'num_of_authors': num_of_authors,
        'num_of_visits': request.session['num_of_visits'],
    })

