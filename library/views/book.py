
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from library.models import ReserveBook
from library.models.book import Book
from library.models.publisher import Publisher
from library.models.tags import Tag
from users.models.library_user import LibraryUser
from django.db.models import Count
from django.views.generic import ListView


class BookListView(ListView):
    model = Book
    template_name = 'library/book_shelf.html'
    context_object_name = 'books'
    paginate_by = 13  # Show 11 books per page

    def get_queryset(self):
        # Get the query parameters from the request
        query = self.request.GET.get('q')
        selected_tags = self.request.GET.getlist('tags')
        selected_publishers = self.request.GET.getlist('publisher')

        # Start with all books
        queryset = Book.objects.all()

        # Filter by query if present
        if query:
            queryset = queryset.filter(title__icontains=query)

        # Filter by tags if any are selected
        if selected_tags:
            queryset = queryset.filter(tags__id__in=selected_tags)

        # Filter by publishers if any are selected
        if selected_publishers:
            queryset = queryset.filter(publisher__id__in=selected_publishers)

        return queryset

    def get_context_data(self, **kwargs):
        # Get the default context data
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['tags'] = Tag.objects.all()
        context['publishers'] = Publisher.objects.annotate(num_books=Count('book')).order_by('-num_books')[:10]
        context['selected_tags'] = self.request.GET.getlist('tags')
        context['selected_publishers'] = self.request.GET.getlist('publisher')

        # Define the book styles for each position
        book_styles = [
            {'color': '#960A14', 'rotation': 0, 'width': 5},  # Green, slight right tilt, thinner
            {'color': '#960A14', 'rotation': 0, 'width': 6},  # Red, straight, medium width
            {'color': '#960A14', 'rotation': 0, 'width': 5},  # Orange, slight left tilt, wider
            {'color': '#960A14', 'rotation': -10, 'width': 3},  # Blue, noticeable right tilt, medium width
            {'color': '#960A14', 'rotation': 0, 'width': 4},  # Green, straight, thinner
            {'color': '#960A14', 'rotation': -20, 'width': 5},  # Red, slight left tilt, medium width
            {'color': '#960A14', 'rotation': -22, 'width': 3},  # Orange, straight, wider
            {'color': '#960A14', 'rotation': 0, 'width': 4},  # Blue, slight right tilt, thinner
            {'color': '#960A14', 'rotation': -10, 'width': 6},  # Green, noticeable left tilt, medium width
            {'color': '#960A14', 'rotation': 0, 'width': 4},  # Red, straight, thinner
            {'color': '#960A14', 'rotation': -3, 'width': 6},  # Orange, straight, wider
            {'color': '#960A14', 'rotation': -15, 'width': 6},  # Orange, straight, wider
            {'color': '#960A14', 'rotation': -25, 'width': 6},  # Orange, straight, wider
        ]

        books_with_styles = []
        for i, book in enumerate(context['books']):
            # Assign styles to each book based on its position
            style = book_styles[i % len(book_styles)]
            book.color = style['color']
            book.rotation = style['rotation']
            book.width = style['width']
            books_with_styles.append(book)

        # Update the context with styled books
        context['books'] = books_with_styles
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'library/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        similar_books = book.get_similar_books()[:10]
        context['similar_books'] = similar_books
        return context


class ReserveBookView(LoginRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        user = get_object_or_404(LibraryUser, user=request.user)

        # Check if a reservation already exists for this user and book
        if ReserveBook.objects.filter(book=book, user=user, status='active').exists():
            messages.error(request, 'You have already reserved this book.')
            return redirect('book_detail', pk=pk)

        if book.currently_available_quantity > 0:
            reserve = ReserveBook(
                book=book,
                user=user,
                reserved_date=timezone.now(),
                due_date=timezone.now() + timezone.timedelta(days=1)
            )
            reserve.save()
            book.currently_available_quantity -= 1
            book.save()
            messages.success(request, 'Book reserved successfully.')
        else:
            messages.error(request, 'Sorry, this book is currently not available for reservation.')

        return redirect('book_detail', pk=pk)
