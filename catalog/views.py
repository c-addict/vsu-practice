from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from .forms import RenewBookForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User


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


def create_user(request):
    if request.method == 'GET':
        return render(request, 'html/create_user.html', context={

        })
    else:
        user = User.objects.create_user()
        user.save()



@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):

    book_inst = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={
            'renewal_date': proposed_renewal_date,
        })
    return render(request, 'html/book_renew_librarian.html', {
        'form': form,
        'bookinst': book_inst,
    })


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


class AuthorCreate(CreateView):

    model = Author
    fields = '__all__'


class AuthorUpdate(UpdateView):

    model = Author
    fields = [
        'first_name',
        'last_name',
        'date_of_birth',
        'date_of_death',
    ]


class AuthorDelete(DeleteView):

    model = Author
    success_url = reverse_lazy('authors')