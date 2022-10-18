from django.shortcuts import render, redirect
from .forms import ArticleForm
from .models import Article
from django.views.decorators.http import require_http_methods

# Create your views here.
def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)

@require_http_methods(['GET', 'POST'])
def create(request):
    # GET이 아닌 POST 사용
    if request.method == 'POST':
        # DB에 저장
        article_form = ArticleForm(request.POST, request.FILES)
        # print(request.FILES)
        # 유효성 검사
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:index')
    else:
        # 유효하지 않은 경우
        # 이슈가 발생한 페이지를 보여주고 정정하라고 함
        article_form = ArticleForm()
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/create.html', context)


def detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'article': article
    }
    return render(request, 'articles/detail.html', context)

@require_http_methods(['GET', 'POST'])
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES, instance=article)
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:detail', article.pk)
    else:
        article_form = ArticleForm(instance=article)
    context = {
        'article': article,
        'article_form': article_form
    }
    return render(request, 'articles/update.html', context)


def delete(request, pk):
    Article.objects.get(pk=pk).delete()
    return redirect('articles:index')