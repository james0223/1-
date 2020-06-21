from django.db import models
from django.conf import settings

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=50)
    id = models.IntegerField(primary_key=True)

class Love(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lover")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)


class Movie(models.Model):
    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
    overview = models.TextField(blank=True)
    release_date = models.DateField()
    popularity = models.FloatField(default=0)
    original_language = models.CharField(max_length=100)
    poster_path = models.CharField(max_length=100)
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)
    backdrop_path = models.CharField(max_length=100)
    genres = models.ManyToManyField(Genre,related_name = 'movies')
    site_count = models.IntegerField(default=0)
    site_total = models.IntegerField(default=0)
    site_average = models.FloatField(default=0)
    now_playing = models.BooleanField(default=False)
    upcoming = models.BooleanField(default=False)

class MovieComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mcomments")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    content = models.CharField(max_length=20)
    rank = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'like_articles')

class ArticleComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)