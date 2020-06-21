from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns=[
    path('signup/', views.signup, name='signup' ),
    path('login/', views.login, name='login'),
    path('update/<username>', views.update, name="update"),
    path('password/<username>', views.password, name="password"),
    path('logout/', views.logout, name='logout'),
    path('<username>/', views.profile, name='profile'),
    path('<username>/follow/',views.follow, name='follow'),
]