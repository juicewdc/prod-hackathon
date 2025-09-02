from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Blog
@login_required
def blog(request):
    context = {
        'blogs': []
    }
    for blog in Blog.objects.all().order_by('-id'):
        context['blogs'].append({'from_user': blog.user.username, 'title': blog.title, 'content': blog.content})
    return render(request, 'blog.html', context=context)

@login_required
def add_post(request):
    return render(request, 'add_blog.html')


def process_add_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['post_text']
        blog = Blog.objects.create(user_id=request.user.id, title=title, content=content)
        blog.save()
        return redirect('travelblog:blog')
