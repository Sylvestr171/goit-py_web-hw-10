from django.shortcuts import render, get_object_or_404, redirect

from .models import Author, Tag, Quote
from django.core.paginator import Paginator
from .forms import AuthorForm, QuoteForm
from django.contrib.auth.decorators import login_required

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

@login_required(login_url='users:login')
def author_add(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/author_add.html', {'form': form})
    return render(request, 'quotes/author_add.html', context={'form': AuthorForm()})

@login_required(login_url='users:login')
def quote_add(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.save()

            tag_names = form.cleaned_data['tags']
            tags = []
            for name in tag_names:
                tag, created = Tag.objects.get_or_create(name=name)
                tags.append(tag)
            quote.tags.set(tags)
            return redirect(to='quotes:root')
        else:
            form = QuoteForm()
            return render(request, 'quotes/quote_add.html', {'form': form})
    return render(request, 'quotes/quote_add.html', context={'form': QuoteForm()})

