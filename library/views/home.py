# views.py
from django.shortcuts import render
from library.models.book import Book
from library.models.author import Author
from django.db.models import Count


def base(request):
    authors = Author.objects.all()
    context = {
        'authors': authors
    }
    print(authors)
    return render(request, 'library/header.html', context)


def home(request):
    # Fetch necessary data from the database
    user_info = request.user  # Fetch information about the logged-in user
    news1 = "If you don’t like to read, you haven’t found the right book."  # News with marquee
    news2 = "There is more treasure in books than in all the pirate’s loot on Treasure Island."  # News with marquee
    popular_authors = Author.objects.annotate(num_books=Count('book')).order_by('-num_books')[:3]
    # Fetch the 3 most popular authors
    popular_books = Book.objects.order_by('-borrowed_quantity')[:8]
    # Fetch the 5 most popular books by number of borrows
    authors = Author.objects.all()
    # Pass the data to the template
    context = {
        'user_info': user_info,
        'news1': news1,
        'news2': news2,
        'popular_authors': popular_authors,
        'popular_books': popular_books,
        'authors': authors
    }

    # Render the home page template with the context data
    return render(request, 'library/home.html', context)
