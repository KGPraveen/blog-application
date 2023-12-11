from django.http import HttpResponseRedirect
from django.shortcuts import render
from app.forms import CommentForm
from app.models import Post, Comment
from django.urls import reverse

# Create your views here.


def home(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'app/home.html', context)


def post(request, slug):
    post = Post.objects.get(slug=slug)
    
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
