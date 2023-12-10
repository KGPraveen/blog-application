from django.urls import path
from app import views

urlpatterns = [
    # <type:variable>
    path('post/<slug:slug>', views.post, name='post_page')
]