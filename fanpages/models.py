from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.
class Fanpage(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser, related_name='fanpage_joined', blank=True)
    name = models.TextField()
    description = models.TextField()
    imgFanpage = models.ImageField(upload_to='fanpage/', blank=True, null=True)
    imgFanpageCover = models.ImageField(upload_to='fanpageCover/', blank=True, null=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_fanpage', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fanpage: {self.name} - {self.author.username}"

class ImageFanpage(models.Model):
    image = models.ImageField(upload_to='images_post_fanpage/', blank=True, null=True)

class VideoFanpage(models.Model):
    video = models.FileField(upload_to='videos_post_fanpage/',blank=True, null=True)

class Post_Fanpage(models.Model):
    fanpage = models.ForeignKey(Fanpage, on_delete=models.CASCADE,blank=True,null=True)
    content = models.TextField()
    images = models.ManyToManyField(ImageFanpage, blank=True)
    video = models.ManyToManyField(VideoFanpage, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    likes = models.ManyToManyField(
    CustomUser, related_name='liked_posts_fanpage', blank=True)
    liked = models.TextField(default=False)

    def __str__(self):
        return f"Fanpage {self.fanpage.author.username} - {self.created_at}"

class CommentFanpage(models.Model):
    post = models.ForeignKey(Post_Fanpage, on_delete=models.CASCADE, related_name='commentsPostFanpage')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"


class ReplyCommentFanpage(models.Model):
    comment = models.ForeignKey(CommentFanpage, on_delete=models.CASCADE, related_name='repliesPostFanpage')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.author.username} on {self.comment}"