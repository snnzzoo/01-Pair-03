from django.shortcuts import render, redirect
from .forms import ArticleForm
from .models import Article

# Create your views here.
def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)


def create(request):
    # GET이 아닌 POST 사용
    if request.method == 'POST':
        # DB에 저장
        article_form = ArticleForm(request.POST)
        # 유효성 검사
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:index') # 나중에 글 상세보기 페이지로 변경
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

    