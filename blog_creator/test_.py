from django.test import TestCase
from django.shortcuts import render, redirect
from .models import BlogCreatorPost

# Create your tests here.
def post_articles(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        content = request.POST.get('content')
        category = request.POST.get('category')

        if title and author and content and category:
            new_blog_post = BlogCreatorPost.objects.create(
                user=request.user,
                blog_title=title,
                blog_author=author,
                blog_content=content,
                category=category,
                tag=request.POST.get('tag', ''), # Optional tag field
                # You can add more fields as needed
                # publication_date will be set automatically
                # by the model's auto_now_add=True
                # field
            )
            new_blog_post.save()
            return redirect('index') # Redirect to index after posting
        else:
            error_message = 'All fields are required'
            return render(request, 'post-articles.html', {'error_message': error_message})
    else:
        # If GET request just render the post-articles page
        if request.user.is_authenticated:
            user_posts = BlogCreatorPost.objects.filter(user=request.user)
            return render(request, 'post-articles.html', {'user_posts': user_posts})
        else:
            # If user is not authenticated, redirect to login
            return redirect('login')