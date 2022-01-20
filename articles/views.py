from http.client import HTTPS_PORT
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from articles.models import Article
from articles.forms import ArticleForm 
from django.http import Http404  

def article_search_view(request):
    query_dict = request.GET
    article_obj = None
    try:
        query = int(query_dict.get('q')) # <input type='text' name='q' />
    except:
        query = None
    articles_ids = [a.id for a in Article.objects.all()]
    if query not in articles_ids:
        query = None
    if query is not None:
        article_obj = Article.objects.get(id=query)

    context = {
        'obj': article_obj
    }
    return render(request, 'articles/search.html', context=context)

def article_detail_view(request, slug=None):
    article_obj = None
    if slug is not None:
        try:
            article_obj = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404

        # this shouldn't be even a case! but just to be sure
        except Article.MultipleObjectsReturned:
            article_obj = Article.objects.filter(slug=slug).first()
        except:
            raise Http404
    context = {
        'obj' : article_obj
    }
    return render(request, 'Articles/Detail.html', context = context)

@login_required
def article_create_view(request):
    form = ArticleForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        article_obj = form.save()
        context['form'] = ArticleForm() # we can put (request.POST or None)
        context['object'] = article_obj
        context['created'] = True
        return redirect(article_obj.get_absolute_url())
    return render(request, 'articles/Create.html', context=context)

# Reference!
# def article_create_view(request):
#     form = ArticleForm()
#     context = {
#         'form': form
#     }
#     if request.method == 'POST':
#         form = ArticleForm(request.POST)
#         context['form'] = form 
#         if form.is_valid():
#             title = form.cleaned_data.get('title')
#             content = form.cleaned_data.get('content')
#             article_obj = Article.objects.create(title=title, content=content)
#             context['title'] = title
#             context['content'] = content
#             context['object'] = article_obj
#             context['created'] = True
#     return render(request, 'articles/Create.html', context=context)
