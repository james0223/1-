from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('',views.list, name='home'),
    path('search',views.search, name='search'),
    path('search_genre/<int:genre_pk>/',views.search_genre, name="search_genre"),
    path('tops',views.tops, name='tops'),
    path('data',views.data, name='data'),
    path('<int:movie_pk>/', views.movie_detail, name ='movie_detail'),
    path('<int:movie_pk>/create/', views.movie_co_create, name="movie_co_create"),
    path('community/', views.article_list, name="article_list"),
    path('community/create/',views.article_create, name = 'article_create'),
    path('community/<int:article_pk>/',views.article_detail, name='article_detail'),
    path('community/<int:article_pk>/update/', views.article_update, name= 'article_update'),
    path('community/<int:article_pk>/delete/', views.article_delete, name = 'article_delete'),
    path('community/<int:article_pk>/like/', views.like, name = 'like'),
    path('community/<int:article_pk>/comment/', views.comment_create, name='comment_create'),
    path('community/<int:article_pk>/comment/<int:comment_pk>/update/', views.comment_update, name= 'comment_update'),
    path('community/<int:article_pk>/comment/<int:comment_pk>/delete', views.comment_delete, name= 'comment_delete'),
    path('nowPlaying',views.now_playing, name='now_playing'),
    path('upcoming',views.upcoming, name='upcoming'),
    path('<int:movie_pk>/<int:moviecomment_pk>/update/', views.movie_co_update, name="movie_co_update"),
    path('<int:movie_pk>/<int:moviecomment_pk>/delete/', views.movie_co_delete, name="movie_co_delete"),
]