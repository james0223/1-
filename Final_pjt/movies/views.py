from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Movie,Article,ArticleComment,MovieComment,Genre,Love
from .forms import ArticleForm,ArticleCommentForm,MovieCommentForm
from django.views.decorators.http import require_POST,require_GET
from django.contrib import messages
import json,requests
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.paginator import Paginator

# Create your views here.
def list(request):
    top5movies = Movie.objects.all().order_by('-vote_average')[:5]
    top1 = top5movies[0]
    top2 = top5movies[1]
    top3 = top5movies[2]
    top4 = top5movies[3]
    top5 = top5movies[4]
    movies = Movie.objects.all().order_by('-vote_average')[5:]
    paginator = Paginator(movies, 8)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        person = request.user
        fav = person.lover.all().order_by('-value')[:3]
        fav_one = fav[0].genre
        fav_two = fav[1].genre
        fav_thr = fav[2].genre
        tmp1 = Movie.objects.all().filter(genres=fav_one).order_by('-vote_average')
        foru1 = []
        idx = 0
        while len(foru1) < 4:
            if not tmp1[idx].reviews.filter(user=request.user).exists():
                foru1.append(tmp1[idx])
            idx += 1
        tmp2 = Movie.objects.all().filter(genres=fav_two).order_by('-vote_average')
        foru2 = []
        idx = 0
        while len(foru2) < 4:
            if not tmp2[idx].reviews.filter(user=request.user).exists():
                foru2.append(tmp2[idx])
            idx += 1
        tmp3 = Movie.objects.all().filter(genres=fav_thr).order_by('-vote_average')
        foru3 = []
        idx = 0
        while len(foru3) < 4:
            if not tmp3[idx].reviews.filter(user=request.user).exists():
                foru3.append(tmp3[idx])
            idx += 1
        context = {
            'top1':top1,
            'top2':top2,
            'top3':top3,
            'top4':top4,
            'top5':top5,
            'movies':movies,
            'page_obj':page_obj,
            'fav_one':fav_one,
            'fav_two':fav_two,
            'fav_thr':fav_thr,
            'foru1':foru1,
            'foru2':foru2,
            'foru3':foru3,
        }
        return render(request, 'movies/home.html', context)
    context = {
            'top1':top1,
            'top2':top2,
            'top3':top3,
            'top4':top4,
            'top5':top5,
            'movies':movies,
            'page_obj':page_obj,
            }
    return render(request,'movies/home.html',context)

def tops(request):
    movies = Movie.objects.all().order_by('-site_average')
    context = {
        'movies':movies
    }
    return render(request, "movies/home.html", context)

def now_playing(request):
    movies = Movie.objects.filter(now_playing=True)
    context = {
        'movies' : movies,
    }
    return render(request, 'movies/nowPlaying.html', context)

def upcoming(request):
    movies = Movie.objects.filter(upcoming=True)
    context = {
        'movies' : movies,
    }
    return render(request, 'movies/upcoming.html', context)


def search_genre(request, genre_pk):
    genre = get_object_or_404(Genre, id=genre_pk)
    movies = Movie.objects.all().filter(genres=genre).order_by('-vote_average')
    context = {
        "genre":genre,
        "movies":movies
    }
    return render(request, "movies/home.html", context)

@require_GET
def search(request):
    movies = Movie.objects.all()
    search = request.GET.get('search','')
    res = []
    Sum = 0
    if search:
        resMovies = movies.filter(title__contains=search)
        if resMovies:
            Sum = resMovies.count()
            for i in range(Sum):
                res.append({
                    'title': resMovies[i].title,
                    'id':resMovies[i].id,
                    'backdrop_path':resMovies[i].backdrop_path,
                    'date':resMovies[i].release_date,
                    'overview':resMovies[i].overview,
                    'vote_average':resMovies[i].vote_average,
                })
        context = {
            'movies':movies,
            'search':search,
            'res':res,
            'Sum':Sum,
        }
        return render(request, 'movies/search.html', context)

    else:
        return redirect('movies:home')


def data(request):
    if not request.user.is_superuser:
        messages.warning(request,'권한이 없습니다!')
        return redirect('movies:home')

    SECRET_KEY = 'edca96b252b83e38a517c3a0d7ec4168'
    API_URL_GENRE = f"https://api.themoviedb.org/3/genre/movie/list?api_key={SECRET_KEY}&language=ko"
    response = requests.get(API_URL_GENRE)
    Movie_Genre = response.json()
    for item in Movie_Genre['genres']:
        genre = Genre()
        genre.id = item.get('id')
        genre.name = item.get('name')
        genre.save()

    for idx in range(1,3):
        API_URL = f'https://api.themoviedb.org/3/movie/popular?api_key={SECRET_KEY}&language=ko-kr&page={idx}'
        response = requests.get(API_URL)
        MovieData = response.json()
        for item in MovieData['results']:
            movies = Movie()
            if item['vote_count'] != 0 and item['backdrop_path'] != None:
                tmp = item.get('release_date')
                if not tmp:
                    continue
                movies.title = item.get('title')
                movies.overview = item.get('overview')
                movies.original_title = item.get('original_title')
                movies.popularity = item.get('popularity')
                movies.vote_count = item.get('vote_count')
                movies.vote_average = item.get('vote_average')
                movies.original_language = item.get('original_language')
                movies.release_date = item.get('release_date')
                movies.poster_path = item.get('poster_path')
                movies.backdrop_path = item.get('backdrop_path')
                movies.save()
                for num in item.get('genre_ids'):
                    movies.genres.add(num)

        NowPlay_API_URL = f'https://api.themoviedb.org/3/movie/now_playing?api_key={SECRET_KEY}&language=ko-kr&page={idx}'
        NowPlayResponse = requests.get(NowPlay_API_URL)
        NowPlayData = NowPlayResponse.json()
        for item in NowPlayData['results']:
            movies = Movie()
            if item['vote_count'] != 0 and item['backdrop_path'] != None:
                tmp = item.get('release_date')
                if not tmp: continue

                temp = item.get('title')
                try:
                    movie = Movie.objects.get(title=temp)
                    movie.now_playing = True
                    movie.save()
                except ObjectDoesNotExist:
                    movies.title = item.get('title')
                    movies.overview = item.get('overview')
                    movies.original_title = item.get('original_title')
                    movies.popularity = item.get('popularity')
                    movies.vote_count = item.get('vote_count')
                    movies.vote_average = item.get('vote_average')
                    movies.release_date = item.get('release_date')
                    movies.adult = item.get('adult')
                    movies.original_language = item.get('original_language')
                    movies.poster_path = item.get('poster_path')
                    movies.backdrop_path = item.get('backdrop_path')
                    movies.now_playing = True
                    movies.save()
                    for num in item.get('genre_ids'):
                        movies.genres.add(num)

        Up_API_URL = f'https://api.themoviedb.org/3/movie/upcoming?api_key={SECRET_KEY}&language=ko-kr&page={idx}'
        UpResponse = requests.get(Up_API_URL)
        UpData = UpResponse.json()
        for item in UpData['results']:
            movies = Movie()
            if item['vote_count'] != 0 and item['backdrop_path'] != None:
                tmp = item.get('release_date')
                if not tmp: continue

                temp = item.get('title')
                try:
                    movie = Movie.objects.get(title=temp)
                    movie.upcoming = True
                    movie.save()
                except ObjectDoesNotExist:
                    movies.title = item.get('title')
                    movies.overview = item.get('overview')
                    movies.original_title = item.get('original_title')
                    movies.release_date = item.get('release_date')
                    movies.popularity = item.get('popularity')
                    movies.vote_count = item.get('vote_count')
                    movies.vote_average = item.get('vote_average')
                    movies.adult = item.get('adult')
                    movies.original_language = item.get('original_language')
                    movies.poster_path = item.get('poster_path')
                    movies.backdrop_path = item.get('backdrop_path')
                    movies.upcoming = True
                    movies.save()
                    for num in item.get('genre_ids'):
                        movies.genres.add(num)
    messages.success(request, 'Done!')
    return render(request, 'movies/data.html')

def movie_detail(request,movie_pk):
    movie = get_object_or_404(Movie,id=movie_pk)
    form = MovieCommentForm()
    comments = movie.reviews.all()
    pagintor = Paginator(comments, 5)
    page_number = request.GET.get('page')
    page_obj = pagintor.get_page(page_number)

    #재호
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'key': settings.YOUTUBE_API_KEY,
        'part': 'snippet',
        'type': 'video',
        'q': movie.title + '예고편',
        'maxResults':2
    }
    response = requests.get(url, params)
    response_dict = response.json()

    #기람
    find = 0
    ls = []
    usercomment = ''
    result = ''
    lst=''
    if request.user.is_authenticated:
        find = request.user.mcomments.all().filter(movie_id = movie_pk).count()
        lst = request.user.mcomments.all()
        for i in lst.values_list():
            ls.append(i)
            # if i[2] == movie_pk:
            #     mcommentid = i[1]
        for data in ls:
            if data[2] == movie_pk:
                result = data[0]

        if find > 0:
            usercomment = request.user.mcomments.all()
    context = {
        'movie':movie,
        'form':form,
        'comments':comments,
        'find':find,
        'usercomment':usercomment,
        'ls':ls,
        'lst':lst,
        'result':result,
        'youtube_items':response_dict['items'],
        'page_obj':page_obj
    }

    return render(request,'movies/movie_detail.html',context)

@login_required
@require_POST
def movie_co_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    form = MovieCommentForm(request.POST)
    if form.is_valid():
        for genre in movie.genres.all():
            target = get_object_or_404(Love, genre=genre, user=request.user)
            target.value += 1
            target.save()
        mcomment = form.save(commit=False)
        mcomment.user = request.user
        mcomment.movie = movie
        mcomment.save()
        movie.site_total += mcomment.rank
        movie.site_count += 1
        movie.site_average = round(movie.site_total/movie.site_count, 1)
        movie.save()
        request.user.points += 4
        request.user.save()
    return redirect('movies:movie_detail', movie_pk)

@login_required
def movie_co_update(request, movie_pk, moviecomment_pk):
    movie = get_object_or_404(Movie,pk=movie_pk)
    mcomment = get_object_or_404(MovieComment, pk=moviecomment_pk)
    ori = mcomment.rank
    if request.user != mcomment.user:
        return redirect('movies:movie_detail', movie_pk)
    if request.method == 'POST':
        form = MovieCommentForm(request.POST, instance=mcomment)
        if form.is_valid():
            mcomment = form.save()
            movie.site_total -= ori
            movie.site_total += mcomment.rank
            movie.site_average = round(movie.site_total/movie.site_count, 1)
            movie.save()
            return redirect('movies:movie_detail', movie_pk)
    else:
        form = MovieCommentForm(instance=mcomment)
    context = {
        'movie':movie,
        'form':form,
    }
    return render(request,'movies/home.html',context)

@login_required
def movie_co_delete(request, movie_pk, moviecomment_pk):
    movie = get_object_or_404(Movie,pk=movie_pk)
    mcomment = get_object_or_404(MovieComment, pk=moviecomment_pk)
    ori = mcomment.rank
    if request.user == mcomment.user:
        mcomment.delete()
        movie.site_total -= ori
        movie.site_count -= 1
        if movie.site_total == 0:
            movie.site_average = 0
        else:
            movie.site_average = round(movie.site_total/movie.site_count, 1)
        movie.save()
    else:
        messages.warning(request, "What do you think you are doing?")
    return redirect('movies:movie_detail', movie_pk)


def article_list(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 15)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'articles':articles,
        'page_obj':page_obj,
    }
    return render(request, 'movies/article_list.html', context)

@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            request.user.points += 5
            request.user.save()
            article.save()
            return redirect('movies:article_list')
    else:
        form = ArticleForm()
    context = {
        'form':form,
    }
    return render(request, 'movies/article_create.html', context)

@login_required
def article_detail(request, article_pk):
    article = get_object_or_404(Article, id=article_pk)
    form = ArticleCommentForm()
    comments = article.articlecomment_set.all()
    context = {
        'article':article,
        'form':form,
        'comments':comments,
    }
    return render(request,'movies/article_detail.html', context)

@login_required
def article_update(request, article_pk):
    article = get_object_or_404(Article,pk=article_pk)
    if article.user != request.user:
        return redirect('movies:article_list')

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article=form.save()
            return redirect('movies:article_detail', article_pk)
    else:
        form = ArticleForm(instance=article)
    context = {
        'article':article,
        'form':form,
    }
    return render(request,'movies/article_create.html',context)

@login_required
@require_POST
def article_delete(request,article_pk):
    article = get_object_or_404(Article,pk=article_pk)
    if request.user == article.user:
        request.user.points -= 2
        request.user.save()
        article.delete()
    return redirect('movies:article_list')


@login_required
def like(request,article_pk):
    article = get_object_or_404(Article,pk=article_pk)
    user = request.user
    if request.user.is_authenticated:
        if request.user == article.user:
            messages.warning(request, "This is your own article!")
        else:
            if article.like_users.filter(id=user.id).exists():
                article.user.points += 10
                article.like_users.remove(user)
            else:
                article.user.points -= 10
                article.like_users.add(user)
            article.user.save()
        return redirect('movies:article_detail', article.pk)
    else:
        return redirect('accounts:login')

def comment_create(request,article_pk):
    article = get_object_or_404(Article,pk=article_pk)
    form = ArticleCommentForm(request.POST)
    if form.is_valid():
        request.user.points += 3
        request.user.save()
        comment = form.save(commit=False)
        comment.user = request.user
        comment.article = get_object_or_404(Article,id=article_pk)
        comment.save()
    return redirect('movies:article_detail', article_pk)

@login_required
def comment_update(request,article_pk,comment_pk):
    article = get_object_or_404(Article,pk=article_pk)
    comment = get_object_or_404(ArticleComment, pk=comment_pk)

    if comment.user != comment.user:
        return redirect('movies:article_detail', article_pk)
    if request.method == 'POST':
        form = ArticleCommentForm(request.POST, instance=article)
        if form.is_valid():
            comment=form.save()
            return redirect('movies:article_detail', article_pk)
    else:
        form = ArticleCommentForm(instance=article)
    context = {
        'article':article,
        'form':form,
    }
    return render(request,'movies/article_create.html',context)

def comment_delete(request, article_pk,comment_pk):
    comment = get_object_or_404(ArticleComment, pk=comment_pk)
    if request.user == comment.user:
        request.user.points -= 3
        request.user.save()
        article = get_object_or_404(Article,pk=article_pk)
        comment.delete()
    else:
        messages.warning(request, "What do you think you are doing?")
    return redirect('movies:article_detail', article_pk)