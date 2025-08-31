from django.shortcuts import render, get_object_or_404

from .models import Author, Tag, Quote
from django.core.paginator import Paginator

# Create your views here.
def main(request, page=1):
    quotes = Quote.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes' : quotes_on_page})

def author(request, author_fullname):
    author=get_object_or_404(Author, fullname=author_fullname)
    return render(request, 'quotes/author.html', context={'author' : author})