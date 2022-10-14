from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, update_session_auth_hash
# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    users = get_user_model().objects.order_by('-pk')
    context = {
        'users': users,
    }
    return render(request, 'accounts/index.html', context)


def signup(request):
    # 이미 로그인 한 사람은 accounts:index로 보내기
    if request.user.is_authenticated:
        return redirect('accounts:index')
    else:
        # POST 요청 처리
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                auth_login(request, user)
                return redirect('accounts:index')
        else:
            form = CustomUserCreationForm()
        context = {
            'form': form
        }
        return render(request, 'accounts/signup.html', context)
    

def login(request):
    if request.user.is_authenticated:
        return redirect('accounts:index')
    else:
        if request.method == 'POST':
            # AuthenticationForm은 ModelForm이 아님
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                # 세션에 저장
                # login 함수는 request, user 객체를 인자로 받음
                # user 객체는 form에서 인증된 유저 정보
                auth_login(request, form.get_user())
                return redirect('accounts:index')
        else:
            form = AuthenticationForm()
        context = {
            'form': form
        }
        return render(request, 'accounts/login.html', context)


def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    context = {
        'user': user
    }
    return render(request, 'accounts/detail.html', context)


@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:detail', request.user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/update.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('accounts:detail', request.user.pk)
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/change_password.html', context)
    

def logout(request):
    auth_logout(request)
    return redirect('index')


@login_required
def delete(request):
    # 선 탈퇴
    request.user.delete()
    # 후 로그아웃
    auth_logout(request)
    return redirect('index')
