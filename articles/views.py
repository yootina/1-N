from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm, CommentForm
# Create your views here.

def index(request):
    articles = Article.objects.all()

    context = {
        'articles': articles,
    }

    return render(request, 'index.html', context)


def detail(request, id):
    article = Article.objects.get(id=id)
    form = CommentForm() # 댓글을 작성하기 위한 form을 만들고 form을 인스턴스화
    context = {
        'article': article,
        'form': form,
    }

    return render(request, 'detail.html', context)

def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)

        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', id=article.id)

    else:
        form = ArticleForm()

    context = {
        'form': form,
    }

    return render(request, 'form.html', context)



# a/1/c/c/
def comment_create(request, article_id):
    form = CommentForm(request.POST)
    # 종이를 보여주는 코드는 detail안에 구현되어있으니 저장되는 로직만 작성

    if form.is_valid():
        # form을 저장 => 추가로 넣어야되는 데이터를 넣기 위해서 저장 멈춰!!!(어떤 게시물에 속해있는지 추가로 정보 필요)
        comment = form.save(commit=False)

        # article을 찾기 위한 첫번째 방법 (객체를 저장하는 방법)
        # article_id를 기준으로 objects 가져오기 (Read했을 때의 동작과 동일)

        # article = Article.objects.get(id=article_id)

        # # article 컬럼에 추가
        # comment.article = article
        # comment.save()

        # article을 찾기 위한 두번째 방법 (integer를 저장하는 방법)
        comment.article_id =  article_id
        comment.save()

        # 첫번째방법은 DB를 뒤지고 두번째방법은 숫자만 찾아오면 되서 상대적으로 두번째방법이 빠르다.

        return redirect('articles:detail', id=article_id)
