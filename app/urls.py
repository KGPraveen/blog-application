from django.urls import path
from app import views

urlpatterns = [
    path('', views.home, name='home_page'),

    # <type:variable>
    path('post/<slug:slug>', views.post, name='post_page'),

    # <type:variable>
    path('tag/<slug:slug>', views.tag, name='tag_page'),

    # <type:variable>
    path('author/<slug:slug>', views.author, name='author_page'),

    # <type:variable> idk why I am copy pasting this lol
    path('search/', views.search, name='search_page'),

    path('about', views.about, name='about_page'),

    path('all_posts', views.all_posts, name='all_posts_page'),

    path('accounts/register', views.register_user, name='register_user_page'),
]
