from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.user_login, name='login'),
    path('signup', views.user_signup, name='signup'),
    path('logout', views.user_logout, name='logout'),
    path('post-articles', views.post_articles, name='post-articles'),
    path('show-article/<int:pk>/', views.show_article, name='show-article'),
    path('post-comments', views.post_comments, name='post-comments'),
    path('add-category', views.add_category, name='add-category'),
    path('show-categories', views.show_categories, name='show-categories'),
    path('all-articles', views.all_articles, name='all-articles'),
    path('delete-article/<int:pk>/', views.delete_article, name='delete-article'),
    path('all-categories', views.all_categories, name='all-categories'),
    path('delete-category/<int:pk>/', views.delete_category, name='delete-category'),
]