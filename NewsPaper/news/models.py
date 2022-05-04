from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    rating_user = models.FloatField(default=0.0)

    def update_rating(self):
        rating_post_author = self.post_set.all().aggregate(sum('rating_post_author')) * 3
        rating_comment = self.user.comment_set.all().aggregate(sum('rating_comment'))
        rating_comment_post = Post.objects.filter(author=self).values('rating_comment_post')
        self.user_rating = rating_post_author + rating_comment + rating_comment_post
        self.save()

class Category(models.Model):
    Category_Name = models.CharField(max_length=128, unique=True)

post_type_list = [
    ('post', 'статья'),
    ('news', 'новость')
]
class Post(models.Model):
    post_type = models.CharField(max_length=4, choices=post_type_list)
    time_creation = models.DateTimeField(auto_now_add=True)
    header = models.CharField(max_length=150, choices=post_type_list )
    text = models.TextField(choices=post_type_list)
    rating = models.FloatField(default=0.0 )
    author = models.ForeignKey(Author, on_delete= models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def preview(self):
        preview_post = self.text[:124] + '...'
        return preview_post

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    text = models.TextField()
    me_creation = models.DateField(auto_now_add=True)
    rating = models.FloatField(default=0.0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
