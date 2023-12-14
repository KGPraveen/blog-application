from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.id:		# i.e. if this Job id doesn't exist, then define this slug.
            self.slug = slugify(self.name)
        return super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    tag = models.ManyToManyField(Tag, blank=True, related_name='post')

    # RELATED_NAME: with the above line, on Tag, you can say:
    # "ATagObject.post.all() and get all posts." where 'post' is related name.

    view = models.IntegerField(null = True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=200)
    website = models.CharField(max_length=200, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    parent = models.ForeignKey(
        'self', on_delete=models.DO_NOTHING, blank=True, null=True, related_name='replies'
    )
    # RELATED_NAME: with the above line, on a Comment object,
    # you can say: "cmt.replies.all()" and get a queryset of all replies.
    # where 'replies' is related name.

    def __str__(self):
        if self.parent:
            return f"Reply by {self.name} to {self.parent.name}"
        else:
            return f"Comment by {self.name} on {self.post} post."
