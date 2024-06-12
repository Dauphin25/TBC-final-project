from django.db.models import Q
from django.views.generic import ListView, DetailView
from library.models.author import Author


class AuthorListView(ListView):
    model = Author
    template_name = 'library/author_list.html'  # Replace with your actual template
    context_object_name = 'authors'
    paginate_by = 9  # Display 10 authors per page

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Author.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
        return Author.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'library/author_detail.html'
    context_object_name = 'author'
