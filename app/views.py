from tokenize import Comment
from django.shortcuts import render
from app.forms import CommentForm
from app.models import Post

# Create your views here.


def home(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'app/home.html', context)


def post(request, slug):
    comment_form = CommentForm()
    post = Post.objects.get(slug=slug)

    if (request.POST):
        comment_form = CommentForm(request.POST)
        if (comment_form.is_valid()):

            # This means to take an instance of the user inputted form without saving
            # the comment to the database.
            # LOOK, JUST DON'T OVERTHINK IT, SIMPLY USE modelForm_variable.save(commit=False) for
            # adding additional variables manually. And use modelForm_variable.instance()
            # to get an instance of the variable to use it's request.POST values immediately
            # after saving the variable. 
            comment = comment_form.save(commit=False)

            post_id = request.POST.get('post_id')
            comment.post = Post.objects.get(id=post_id)
            comment.save()

    context = {'post': post, 'comment_form': comment_form}
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

