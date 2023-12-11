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
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    tag = models.ManyToManyField(Tag, blank=True, related_name='post')

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
        'self', on_delete=models.DO_NOTHING, blank=True, null=True
    )

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
