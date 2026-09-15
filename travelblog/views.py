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


@login_required
def process_add_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('post_text')
        if title and content:
            Blog.objects.create(user_id=request.user.id, title=title, content=content)
        return redirect('travelblog:blog')
    return redirect('travelblog:add_post')
