from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='uploads/profile', default='uploads/profile/default.jpg', blank=True)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')

    def __str__(self):
        return f'{self.user.username}\'s profile'

@receiver(post_save, sender=User)  
def create_user_profile(sender, created, instance, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    profile = UserProfile.objects.get(user=instance)
    profile.save()


