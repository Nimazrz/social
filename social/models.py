from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager
from django.urls import reverse


# Create your models here.

class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='account-image', null=True, blank=True)
    job = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)


class Post(models.Model):
    #relation
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    description = models.TextField(verbose_name='توضیحات')
    #date
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        # verbose_name="وب"

    def __str__(self):
        return self.author.username

    def get_absolute_url(self):  # for making canonical urls(The unique url of each post)
        return reverse('social:post_detail', args=[self.id])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)