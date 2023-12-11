from django.urls import path
from app import views

urlpatterns = [
    path('', views.home, name='home_page'),
    
    # <type:variable>
    path('post/<slug:slug>', views.post, name='post_page')
]
