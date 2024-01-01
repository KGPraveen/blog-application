from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

# Create your models here.


class MetaData(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    about = models.TextField()

    def __str__(self):
        return self.title


# =================================================================
# post1.author.profile.profile_picture -> will automatically
# give you the profile of the selected user.
# Django does this automatically. No need for extra adding stuff.
# =================================================================
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='images/', blank=True, null=True
    )
    slug = models.SlugField(max_length=200, unique=True)
    bio = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.user.username)
        return super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s Profile"
# =================================================================


class Subscribe(models.Model):
    email = models.EmailField(max_length=200)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


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
    is_featured = models.BooleanField(default=False)

    # =============================================================================
    tag = models.ManyToManyField(Tag, blank=True, related_name='post')
    # =============================================================================
    # RELATED_NAME: with the above line, on Tag, you can say:
    # "ATagObject.post.all() and get all posts." where 'post' is related name.
    # =============================================================================

    view = models.IntegerField(null=True, blank=True)

    # ==============================================================================
    # Uses the django inbuilt User model that you can see in the admin panel.
    # ==============================================================================
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='posts'
    )
    # ==============================================================================

    # ===============================================================================
    # DO NOT OVERTHINK THIS, Use the One-To-One, Many-To-One, Many-To-Many on the
    # model name and this value name. Many-To-One as in Many Posts and Many Bookmark
    # users, because the bookmark stores who's the bookmarking user. If it was Foreign
    # Key, aka Many-To-One, then it would be Many Posts but only one bookmarking User,
    # which makes no sense as multiple users will bookmark the same post and many posts
    # can be bookmarked.
    # ===============================================================================
    bookmarks = models.ManyToManyField(
        User, blank=True, related_name='bookmarked_posts', default=None
    )
    # ===============================================================================
    likes = models.ManyToManyField(
        User, blank=True, related_name='liked_posts', default=None
    )
    # ===============================================================================

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    email = models.EmailField(max_length=200)
    website = models.CharField(max_length=200, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='commented_posts',
    )
    parent = models.ForeignKey(
        'self', on_delete=models.DO_NOTHING, blank=True, null=True, related_name='replies'
    )
    # RELATED_NAME: with the above line, on a Comment object,
    # you can say: "cmt.replies.all()" and get a queryset of all replies.
    # where 'replies' is related name.

    def __str__(self):
        if self.parent:
            return f"Reply by {self.author} to {self.parent.name}"
        else:
            return f"Comment by {self.author} on {self.post} post."
