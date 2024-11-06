from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Index.as_view(), name='Index'),
    path('userprofile/', PersonalProfile.as_view(), name='PersonalProfile'),
    path('userprofile/<int:pk>', UserProfile.as_view(), name='Profile'),
    path('userprofileedit/<int:pk>', UserProfileEdit.as_view(), name='ProfileEdit'),
    path('follow/<int:pk>', FollowUser, name='FollowUser'),
    path('unfollow/<int:pk>', UnfollowUser, name='UnfollowUser'),
    path('signup/', SignUp, name='SignUp'),
    path('login/', Login, name='Login'),
    path('logout/', Logout, name='Logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
