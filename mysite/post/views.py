from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# 이제 로그인하지 않은 유저가 강제로 글 작성 페이지의 URL에 접근하거나, 댓글을 작성하려는 경우 로그인 페이지로 이동하며 로그인 완료 후 원래 있던 URL로 이동한다.
from utils.decorators import login_required

# Create your views here.

from .models import Post, Comment, Provider, Food
from .forms import PostForm, CommentForm


def post_list(request):
    posts = Post.objects.all()
    # comments = Comment.objects.get(pk=1)
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'post/post_list.html', context)

@login_required
def comment_create(request, post_pk):
    # GET파라미터로 전달된 작업 완료 후 이동할 URL값
    next_path = request.GET.get('next')

    # 요청 메서드가 POST방식 일 때만 처리
    if request.method == 'POST':
        # Post인스턴스를 가져오거나 404 Response를 돌려줌
        post = get_object_or_404(Post, pk=post_pk)
        # request.POST에서 'content'키의 값을 가져옴(Bounded Form생성)
        comment_form = CommentForm(request.POST)
        # 올바른 데이터가 Form인스턴스에 바인딩 되어있는지 유효성 검사
        if comment_form.is_valid():
            # 유효성 검사에 통과하면 ModelForm의 save()호출로 인스턴스 생성
            # DB에 저장하지 않고 인스턴스만 생성하기 위해 commit=False옵션 지정
            comment = comment_form.save(commit=False)
            # CommentForm에 지정되지 않았으나 필수요소인 author와 post속성을 지정
            comment.post = post
            comment.author = request.user
            # DB에 저장
            comment.save()
            # 성공 메시지를 다음 request의 결과로 전달하도록 지정
            messages.success(request, '댓글이 등록되었습니다')
        else:
            # 유효성 검사에 실패한 경우
            # 에러 목록을 순회하며 에러메시지를 작성, messages의 error레벨로 추가
            error_msg = '댓글 등록에 실패했습니다\n{}'.format(
                '\n'.join(
                    [f'- {error}'
                     for key, value in comment_form.errors.items()
                     for error in value]))
            messages.error(request, error_msg)

        if next_path:
            return redirect(next_path)

        return HttpResponseRedirect(reverse('post:post_list'))

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # post = Post(photo = request.FILES['photo'])
            post = form.save(commit=False)
            post.author = request.user
            post.save()
        return HttpResponseRedirect(reverse('post:post_list'))
    else:
        post_form=PostForm()
        return render(request, "post/post_new.html", {'post_form':post_form})

def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment_form = CommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,
    }
    return render(request, 'post/post_detail.html', context)

# POST요청에 대해 커스터마이징한 login_required를 사용한다
@login_required
def post_like_toggle(request, post_pk):
    # GET파라미터로 전달된 이동할 URL
    next_path = request.GET.get('next')
    # post_pk에 해당하는 Post객체
    post = get_object_or_404(Post, pk=post_pk)
    # 요청한 사용자
    user = request.user

    # 사용자의 like_posts목록에서 like_toggle할 Post가 있는지 확인
    filtered_like_posts = user.like_posts.filter(pk=post.pk)
    # 존재할경우, like_posts목록에서 해당 Post를 삭제
    if filtered_like_posts.exists():
        user.like_posts.remove(post)
    # 없을 경우, like_posts목록에 해당 Post를 추가
    else:
        user.like_posts.add(post)

    # 이동할 path가 존재할 경우 해당 위치로, 없을 경우 Post상세페이지로 이동
    if next_path:
        return redirect(next_path)
    return redirect('post:post_detail', post_pk=post_pk)



def oe_haters_main(request):
    providers = Provider.objects.all()
    foods = Food.objects.all()
    context = {
        'providers': providers,
        'foods': foods,
    }
    return render(request, 'haters/oe/main.html', context)

def oe_haters_list(request):
    providers = Provider.objects.all()
    foods = Food.objects.all()
    context = {
        'providers': providers,
        'foods': foods,
    }
    return render(request, 'haters/oe/main.html', context)


def oe_haters_list_byprovider(request,provider_pk):
    providers = Provider.objects.all()
    foods = Food.objects.filter(provider=provider_pk)
    context = {
        'providers': providers,
        'foods': foods,
    }
    return render(request, 'haters/oe/main.html', context)


def oe_haters_list_byscore(request):
    providers = Provider.objects.all()
    foods = Food.objects.order_by('score')
    context = {
        'providers': providers,
        'foods': foods,
    }
    return render(request, 'haters/oe/main.html', context)


def oe_haters_ranking(request, page_num, order):
    x = int(page_num)
    if order == "increasing":
        providers = Provider.objects.order_by('score')[10*(x- 1):10*(x)]
    else:
        providers = Provider.objects.order_by('-score')[10*(x- 1):10*(x)]
    context = {
        'providers': providers,
        'page_num': (x-1)*10,
    }
    return render(request, 'haters/oe/ranking.html', context)



def oe_haters_detail(request, food_pk):
    food_detail = get_object_or_404(Food, pk=food_pk)
    comment_form = CommentForm()
    context = {
        'food': food_detail,
        'comment_form': comment_form
    }
    return render(request, 'haters/oe/detail.html', context)

@login_required
def oe_haters_hate_toggle(request, food_pk):
    next_path = request.GET.get('next')
    post = get_object_or_404(Food, pk=food_pk)
    user = request.user

    filtered_like_posts = user.hate_foods.filter(pk=food_pk)
    if filtered_like_posts.exists():
        user.hate_foods.remove(post)
    else:
        user.hate_foods.add(post)
    if next_path:
        return redirect(next_path)
    return redirect('post:oe_haters_detail', food_pk=food_pk)

@login_required
def oe_haters_like_toggle(request, food_pk):
    next_path = request.GET.get('next')
    post = get_object_or_404(Food, pk=food_pk)
    user = request.user

    filtered_like_posts = user.like_foods.filter(pk=food_pk)
    if filtered_like_posts.exists():
        user.like_foods.remove(post)
    else:
        user.like_foods.add(post)
    if next_path:
        return redirect(next_path)
    return redirect('post:oe_haters_detail', food_pk=food_pk)

@login_required
def oe_food_comment_create(request, food_pk):
    # GET파라미터로 전달된 작업 완료 후 이동할 URL값
    next_path = request.GET.get('next')
    # 요청 메서드가 POST방식 일 때만 처리
    if request.method == 'POST':
        # Post인스턴스를 가져오거나 404 Response를 돌려줌
        post = get_object_or_404(Food, pk=food_pk)
        # request.POST에서 'content'키의 값을 가져옴(Bounded Form생성)
        comment_form = CommentForm(request.POST)
        # 올바른 데이터가 Form인스턴스에 바인딩 되어있는지 유효성 검사
        if comment_form.is_valid():
            # 유효성 검사에 통과하면 ModelForm의 save()호출로 인스턴스 생성
            # DB에 저장하지 않고 인스턴스만 생성하기 위해 commit=False옵션 지정
            comment = comment_form.save(commit=False)
            # CommentForm에 지정되지 않았으나 필수요소인 author와 post속성을 지정
            comment.food = post
            comment.author = request.user
            # DB에 저장
            comment.save()
            # 성공 메시지를 다음 request의 결과로 전달하도록 지정
            messages.success(request, '댓글이 등록되었습니다')
        else:
            # 유효성 검사에 실패한 경우
            # 에러 목록을 순회하며 에러메시지를 작성, messages의 error레벨로 추가
            error_msg = '댓글 등록에 실패했습니다\n{}'.format(
                '\n'.join(
                    [f'- {error}'
                     for key, value in comment_form.errors.items()
                     for error in value]))
            messages.error(request, error_msg)
        if next_path:
            return redirect(next_path)
        return HttpResponseRedirect(reverse('post:oe_haters_main'))
