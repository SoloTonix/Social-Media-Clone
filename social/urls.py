from django.urls import path
from .views import *
urlpatterns = [
    path('', Home.as_view(), name='Home'),
    path('post.details/<int:pk>', PostDetail.as_view(), name='Post'),
    path('post.edit/<int:pk>', PostEdit.as_view(), name='PostEdit'),
    path('post.pre.delete/<int:pk>', PrePostDelete, name='PrePostDelete'),
    path('post.delete/<int:pk>', PostDelete, name='PostDelete'),
    path('post.like/<int:pk>', LikePost, name='LikePost'),
    path('post.dislike/<int:pk>', disLikePost, name='disLikePost'),
    path('post.search/', SearchPost, name='SearchPost'),
    path('comment.delete/<int:pk>', deleteComment, name='deleteComment'),
]