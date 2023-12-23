import random
import secrets
from django.http import HttpResponseRedirect
from django.shortcuts import render
from app.forms import CommentForm, SubscribeForm
from app.models import Post, Comment, Tag
from django.urls import reverse

# Create your views here.


def home(request):
    posts = Post.objects.all()
    recent_posts = posts.order_by('-date_created')[0:3]
    top_posts = posts.order_by('-view')[0:3]
    subscribe_form = SubscribeForm()
    subscribe_successful = None
    featured_blogs = Post.objects.filter(is_featured=True)
    featured_blog = None

    if featured_blogs:
        featured_blog = secrets.choice(featured_blogs)

    if (request.POST):
        subscribe_form = SubscribeForm(request.POST)
        if (subscribe_form.is_valid()):
            subscribe_form.save()
            subscribe_form = SubscribeForm()
            subscribe_successful = "Subscribed Successfully!"

    context = {
        'subscribe_form': subscribe_form,
        'posts': posts,
        'recent_posts': recent_posts,
        'top_posts': top_posts,
        'subscribe_successful': subscribe_successful,
        'featured_blog': featured_blog,
    }
    return render(request, 'app/home.html', context)


def post(request, slug):
    post = Post.objects.get(slug=slug)

    # Adding views per post viewd.
    if (post.view == None):
        post.view = 1
        post.save()
    else:
        post.view = post.view + 1
        post.save()

    # To ensure that replies are not taken as comments.
    comments = Comment.objects.filter(post=post, parent=None)
    comment_form = CommentForm()
    parent = None

    if (request.POST):
        comment_form = CommentForm(request.POST)
        if (comment_form.is_valid()):

            # THIS IF STATEMENT IS FOR REPLIES, SKIP TO 'else:' FOR COMMENTS.
            # =======================================================================
            if (request.POST.get('parent_id')):
                parent_id = request.POST.get('parent_id')
                parent = Comment.objects.get(id=parent_id)

                if (parent):
                    comment_reply = comment_form.save(commit=False)
                    comment_reply.parent = parent

                    # parent is obtained through slug (1st line of this function)
                    comment_reply.post = post
                    comment_reply.save()
                    return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))
            # =======================================================================

            else:
                # =======================================================================
                # This means to take an instance of the user inputted form without saving
                # the comment to the database.
                # LOOK, JUST DON'T OVERTHINK IT, SIMPLY USE modelForm_variable.save(commit=False) for
                # adding additional variables manually. And use modelForm_variable.instance()
                # to get an instance of the variable to use it's request.POST values immediately
                # after saving the variable.
                comment = comment_form.save(commit=False)
                # =======================================================================

                # =======================================================================
                post_id = request.POST.get('post_id')
                comment.post = Post.objects.get(id=post_id)
                # =======================================================================

                # =======================================================================
                # OR you can simply use:
                # comment.post = Post.objects.get(slug=slug)
                # instead of the post_id and Post.objects.get(id=post_id)
                comment.save()
                # =======================================================================

                # =======================================================================
                # We use this HttpResponseRedirect() class to redirect the page
                # to eliminate the page to the same site, to fix a refresh bug that
                # is caused by chromium/django (idk which, most likely chromium.)
                return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))
                # =======================================================================

    context = {'post': post, 'comment_form': comment_form, 'comments': comments}
    return render(request, 'app/post.html', context)

# =============================================================================
# def post(request, slug):
#     comment_form = CommentForm()
#     post = Post.objects.get(slug=slug)

#     if (request.POST):
#         comment_form = CommentForm(request.POST)
#         if (comment_form.is_valid()):

#             # This means to take an instance of the user inputted form
#             # without saving the comment to the database.
#             comment = comment_form.save(commit=False)

#             post_id = request.POST.get('post_id')
#             comment.post = Post.objects.get(id=post_id)
#             comment.save()

#     context = {'post': post, 'comment_form': comment_form}
#     return render(request, 'app/post.html', context)
# =============================================================================


def tag(request, slug):
    tag = Tag.objects.get(slug=slug)
    top_posts = Post.objects.filter(tag=tag).order_by('-view')[0:2]
    more_tags = Tag.objects.all().order_by('?')[0:11]
    # =====================================================================================
    # YOU CAN ALSO USE:
    # =====================================================================================
    # top_posts = Post.objects.filter(tag__in=tag).order_by('-view')[0:2]
    # This will also return all posts that have their "tag__in" 'tag'.
    # *** This is useful because you can use it to get all posts that have "tag__in"
    # a list of tags.
    # =====================================================================================

    trending_posts = Post.objects.filter(tag=tag).order_by('view')[0:3]

    context = {
        'tag': tag,
        'top_posts': top_posts,
        'trending_posts': trending_posts,
        'more_tags': more_tags,
    }
    return render(request, 'app/tag.html', context)
