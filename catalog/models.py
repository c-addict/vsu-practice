from django.db import models
from django.urls import reverse
import uuid

# Create your models here.


class Genre(models.Model):

    name = models.CharField(max_length=200, help_text='Enter a book genre')

    def __str__(self):
        return self.name


class Book(models.Model):

    title = models.CharField(max_length=200)

    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')

    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character ISBN number')

    genre = models.ManyToManyField(Genre, help_text='Select a genre for book')

    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, )

    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)

    imprint = models.CharField(max_length=200)

    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reversed'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    class Meta:

        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} {self.book.title}'


class Author(models.Model):

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    date_of_birth = models.DateField(null=True, blank=True)

    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):

        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):

        return f'{self.last_name} {self.first_name}'


class Language(models.Model):

    name = models.CharField(max_length=200, help_text='Enter the books natural language')

    def __str__(self):

        return self.name