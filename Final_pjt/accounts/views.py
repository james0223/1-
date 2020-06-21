from django.shortcuts import render,redirect,get_object_or_404
from .forms import CustomUserChangeForm,CustomUserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model,update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm
from .forms import CustomUserChangeForm,CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from movies.models import Genre, Love
# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            genres = Genre.objects.all()
            for genre in genres:
                Love.objects.create(user=user, genre=genre)
            auth_login(request, user)
            messages.success(request,'회원가입이 완료되었습니다.')
            return redirect('movies:home')
    else:
        form = CustomUserCreationForm()
    context = {
        'form':form,
    }
    return render(request,'accounts/forms.html',context)

def login(request):
    if request.user.is_authenticated:
        return redirect('movies:home')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            messages.success(request, f'{request.user.username}님 환영합니다')
            return redirect('movies:home')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/forms.html', context)

@login_required
def logout(request):
    auth_logout(request)
    messages.success(request,'로그아웃 되었습니다')
    return redirect('movies:home')

@login_required
def update(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    if request.user == user:
        if request.method == 'POST':
            form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                user = form.save()
                return redirect('accounts:profile', user.username)
        else:
            form = CustomUserChangeForm(instance=user)
        context = {
            'form': form,
        }
        return render(request, "accounts/forms.html", context)

    else:
        messages.warning(request, 'You are not {{ user.nickname }}!')
        return redirect('accounts:profile', user.username)

@login_required
def follow(request, username):
    User = get_user_model()
    followee = request.user
    target = get_object_or_404(User,username=username)
    if followee != target:
        if followee.following.filter(pk=target.pk).exists():
            followee.following.remove(target)
        else:
            followee.following.add(target)
    return redirect('accounts:profile',username)

@login_required
def profile(request, username):
    User = get_user_model()
    person = get_object_or_404(User,username=username)
    articles = person.article_set.all()
    liked_articles = person.like_articles.all()
    flag = 0
    act = get_object_or_404(Genre, id=28)
    action = get_object_or_404(Love, user=person, genre=act)
    flag += action.value
    ani = get_object_or_404(Genre, id=12)
    animation = get_object_or_404(Love, user=person, genre=ani)
    flag += animation.value
    com = get_object_or_404(Genre, id=16)
    comedy = get_object_or_404(Love, user=person, genre=com)
    flag += comedy.value
    crim = get_object_or_404(Genre, id=35)
    crime = get_object_or_404(Love, user=person, genre=crim)
    flag += crime.value
    docu = get_object_or_404(Genre, id=80)
    documentary = get_object_or_404(Love, user=person, genre=docu)
    flag += documentary.value
    dra = get_object_or_404(Genre, id=99)
    drama = get_object_or_404(Love, user=person, genre=dra)
    flag += drama.value
    fam = get_object_or_404(Genre, id=10751)
    family = get_object_or_404(Love, user=person, genre=fam)
    flag += family.value
    fan = get_object_or_404(Genre, id=14)
    fantasy = get_object_or_404(Love, user=person, genre=fan)
    flag += fantasy.value
    his = get_object_or_404(Genre, id=36)
    history = get_object_or_404(Love, user=person, genre=his)
    flag += history.value
    hor = get_object_or_404(Genre, id=27)
    horror = get_object_or_404(Love, user=person, genre=hor)
    flag += horror.value
    mu = get_object_or_404(Genre, id=10402)
    music = get_object_or_404(Love, user=person, genre=mu)
    flag += music.value
    mys = get_object_or_404(Genre, id=9648)
    mystery = get_object_or_404(Love, user=person, genre=mys)
    flag += mystery.value
    ro = get_object_or_404(Genre, id=10749)
    romance = get_object_or_404(Love, user=person, genre=ro)
    flag += romance.value
    sfe = get_object_or_404(Genre, id=878)
    sf = get_object_or_404(Love, user=person, genre=sfe)
    flag += sf.value
    tv = get_object_or_404(Genre, id=10770)
    tvm = get_object_or_404(Love, user=person, genre=tv)
    flag += tvm.value
    thri = get_object_or_404(Genre, id=53)
    thriller = get_object_or_404(Love, user=person, genre=thri)
    flag += thriller.value
    wa = get_object_or_404(Genre, id=10752)
    war = get_object_or_404(Love, user=person, genre=wa)
    flag += war.value
    wes = get_object_or_404(Genre, id=37)
    western = get_object_or_404(Love, user=person, genre=wes)
    flag += western.value
    context = {
        'person':person,
        "articles":articles,
        "liked_articles":liked_articles,
        "action":action,
        "animation":animation,
        "comedy":comedy,
        "crime":crime,
        "documentary":documentary,
        "drama":drama,
        "family":family,
        "fantasy":fantasy,
        "history":history,
        "horror":horror,
        "music":music,
        "mystery":mystery,
        "romance":romance,
        "sf":sf,
        "tvm":tvm,
        "thriller":thriller,
        "war":war,
        "western":western,
        "flag":flag,
    }
    return render(request,'accounts/profile.html',context)

def password(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    if request.user == user:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('accounts:profile', user.username)
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = PasswordChangeForm(request.user)
        context = {
            'form': form,
        }
        return render(request, "accounts/password.html", context)
    else:
        messages.warning(request, 'You are not {{ user.nickname }}!')
        return redirect('accounts:profile', user.username)
