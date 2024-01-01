import secrets
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from app.forms import RegisterUserForm, CommentForm, SubscribeForm
from app.models import MetaData, Post, Comment, Profile, Tag
from django.urls import reverse

# Create your views here.


def home(request):

    if (MetaData.objects.all()):
        meta_data = MetaData.objects.all()[0]
    else:
        meta_data = None

    meta_data = MetaData.objects.all()[0]
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
            request.session['subscribed'] = True
            subscribe_form = SubscribeForm()
            subscribe_successful = "Subscribed Successfully!"

    context = {
        'subscribe_form': subscribe_form,
        'posts': posts,
        'recent_posts': recent_posts,
        'top_posts': top_posts,
        'subscribe_successful': subscribe_successful,
        'featured_blog': featured_blog,
        'meta_data': meta_data,
    }
    return render(request, 'app/home.html', context)


def post(request, slug):
    post = Post.objects.get(slug=slug)
    most_recent_posts = Post.objects.all().order_by('-date_created')[0:3]
    related_posts = Post.objects.exclude(
        slug=slug).order_by('?')[0:2]
    top_authors = User.objects.annotate(total_number_of_posts=Count(
        'posts')).order_by('-total_number_of_posts')[0:3]
    top_tags = Tag.objects.annotate(total_number_of_uses=Count(
        'post')).order_by('-total_number_of_uses')

    # Bookmark Logic:
    # ==========================================================================
    # Remember, bookmarks is a 'User' model that is in manytomany relationship
    # with post. And, in those relationship, if you say:
    # post.bookmarks.values('id') you get ids of users. And if you say
    # user.bookmarks.values('id') you get all ids of posts that are bookmarked
    # by that user. Therefore, by saying post.bookmarks.filter(<id>) you
    # get the ids of all users that are bookmarked that post.
    # ==========================================================================
    is_bookmarked = False
    if post.bookmarks.filter(id=request.user.id):
        is_bookmarked = True

    # Post Like Logic:
    post_is_liked = False
    if post.likes.filter(id=request.user.id):
        post_is_liked = True
    total_post_likes = post.likes.all().count()

    # View Logic:
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

            # =======================================================================
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

                    # Checking if the user is logged in
                    # AND THEN AND ONLY THEN SAVING THE REPLY:
                    if request.user.is_authenticated:
                        comment_reply.author = request.user
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
                if request.user.is_authenticated:
                    comment.author = request.user
                    comment.save()

                # =======================================================================
                # OR you can simply use:
                # comment.post = Post.objects.get(slug=slug)
                # instead of the post_id and Post.objects.get(id=post_id)
                # comment.save()
                # =======================================================================

                # =======================================================================
                # We use this HttpResponseRedirect() class to redirect the page
                # to eliminate the page to the same site, to fix a refresh bug that
                # is caused by chromium/django (idk which, most likely chromium.)
                return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))
                # =======================================================================

    context = {
        'total_post_likes': total_post_likes,
        'is_bookmarked': is_bookmarked,
        'post_is_liked': post_is_liked,
        'post': post,
        'comment_form': comment_form,
        'comments': comments,
        'comments_count': comments.count(),
        'most_recent_posts': most_recent_posts,
        'related_posts': related_posts,
        'top_authors': top_authors,
        'top_tags': top_tags,
    }
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
    # This ? will sort them randomly.
    more_tags = Tag.objects.exclude(slug=slug).order_by('?')[0:11]
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


def author(request, slug):
    author_profile = Profile.objects.get(slug=slug)
    author_posts = Post.objects.filter(author=author_profile.user)
    other_authors_profile = Profile.objects.all()
    print(other_authors_profile)

    top_posts = author_posts.order_by('-view')[0:2]
    trending_posts = author_posts.order_by('-date_created')[0:3]

    # ==============================================================
    # Top authors are counted by their total number of posts
    # ==============================================================
    # Annotate means: create a new column 'total_number_of_posts'
    top_authors = User.objects.annotate(
        total_number_of_posts=Count('posts')).order_by('total_number_of_posts')[0:3]
    # It's posts because you added related_name to the model
    # ==============================================================
    # ==============================================================

    context = {
        'author_profile': author_profile,
        'top_posts': top_posts,
        'trending_posts': trending_posts,
        'other_authors_profile': other_authors_profile,
        'top_authors': top_authors,
    }
    return render(request, 'app/author.html', context)


def search(request):
    search_parameter = ''
    searched_posts = Post.objects.all()

    if request.GET.get('q'):
        search_parameter = request.GET.get('q')

        # aka find the search parameter in the title of all posts case insensitive.
        searched_posts = Post.objects.filter(
            Q(title__icontains=search_parameter) |
            Q(tag__name__icontains=search_parameter)
        ).distinct()
        # Q is an imported stuff from django.db.models
        # IT ALLOWS YOU TO PERFORM COMPLEX QUERY SEARCHES.

    context = {
        'search_parameter': search_parameter,
        'searched_posts': searched_posts
    }
    return (render(request, 'app/search.html', context))


def about(request):
    if (MetaData.objects.all()):
        meta_data = MetaData.objects.all()[0]
    else:
        meta_data = None
    context = {
        'meta_data': meta_data
    }
    print(meta_data)
    return render(request, 'app/about.html', context)


def all_posts(request):
    all_posts = Post.objects.all()
    context = {
        'all_posts': all_posts,
    }
    return render(request, 'app/all_posts.html', context)


def all_top_posts(request):
    all_top_posts = Post.objects.all().order_by('-view')
    context = {
        'all_top_posts': all_top_posts,
    }
    return render(request, 'app/all_top_posts.html', context)


def all_new_posts(request):
    all_new_posts = Post.objects.all().order_by('-date_created')
    context = {
        'all_new_posts': all_new_posts,
    }
    return render(request, 'app/all_new_posts.html', context)


def register_user(request):
    register_user_form = RegisterUserForm()

    if request.POST:
        register_user_form = RegisterUserForm(request.POST)

        if register_user_form.is_valid():
            new_user = register_user_form.save()
            login(request, new_user)
            return redirect('/')

    context = {
        'register_user_form': register_user_form,
    }
    return render(request, 'registration/register_user.html', context)


def bookmarks(request):
    search_parameter = ''
    bookmarked_posts = None

    if request.user.is_authenticated:
        bookmarked_posts = request.user.bookmarked_posts.all()

    if request.GET.get('q'):
        search_parameter = request.GET.get('q')

        # aka find the search parameter in the title or tag of all posts case insensitive.
        bookmarked_posts = bookmarked_posts.filter(
            Q(title__icontains=search_parameter) |
            Q(tag__name__icontains=search_parameter)
        ).distinct()
        # Q is an imported stuff from django.db.models
        # IT ALLOWS YOU TO PERFORM COMPLEX QUERY SEARCHES.

    context = {
        'search_parameter': search_parameter,
        'searched_posts': bookmarked_posts
    }
    return render(request, 'app/bookmarks.html', context)


def bookmark_post(request, slug):
    # Exactly as it says, the below shortcut tries to get an object
    # based on the below mentioned constraint, if that fails, it gives
    # a 404 error.
    post = get_object_or_404(Post, id=request.POST.get('post_id'))

    # ====================================================================
    # Remember, bookmarks is a ManyToMany IN Post Model! So when we write
    # post.bookmarks() BELOW, IT AUTOMATICALLY GETS THE ID OF THE post.
    # All that's left is to add the user which is ALSO added below:
    # ====================================================================
    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)
    # ====================================================================
    return HttpResponseRedirect(
        reverse('post_page', args=[str(slug),])
    )


def all_liked_posts(request):
    all_liked_posts = None
    if request.user.is_authenticated:
        all_liked_posts = request.user.liked_posts.all()
    context = {'all_liked_posts': all_liked_posts, }
    return render(request, 'app/all_liked_posts.html', context)


def liked_post(request, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(
        reverse(
            'post_page', args=[str(slug),]
        )
    )
