from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import BlogCreatorPost
from .models import Comment
from .models import Category

# Create your views here.
@login_required
def index(request):
    # This view will render the index page and the latest article
    latest_post = BlogCreatorPost.objects.order_by('-created_at').first() # Get the most recent post
    latest_articles = BlogCreatorPost.objects.order_by('-created_at')[:2] # Get the two most recent posts

    # This view will render the comments for a specific article
    if latest_post is not None:
        show_article = BlogCreatorPost.objects.get(id=latest_post.id) # Get the article by primary key (pk)
        comments = Comment.objects.filter(blogcreatorpost=show_article).order_by('-publication_date') # Get comments for the article
    else:
        comments = None

    # This logic will render the show categories page
    categories = Category.objects.all() # Get all categories
    if not categories:
        return render(request, 'show-categories.html', {'error_message': 'No categories found'})
    
    return render(request, 'index.html', {'latest_post': latest_post, 'latest_articles': latest_articles, 'comments':comments, 'categories': categories})

def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('all-categories')

def all_categories(request):
    # This view will render the all categories page
    categories = Category.objects.all()

    if categories is not None:
        return render(request, 'all-categories.html', {'categories': categories})
    else:
        return render(request, 'all-categories.html')

def delete_article(request, pk):
    article = get_object_or_404(BlogCreatorPost, pk=pk)
    article.delete()
    return redirect('all-articles')

def all_articles(request):
    # This view will render all the articles page
    articles = BlogCreatorPost.objects.all()

    if articles is not None:
        return render(request,'all-articles.html', {'articles': articles})
    else:
        return render(request, 'all-articles', {'error_message': 'No articles found'})

def add_category(request):
    # This view will render the add category page
    if request.method == 'POST':
        category_name = request.POST.get('category-name')

        if category_name:
            # Create a new category if the name is provided
            new_category = Category.objects.create(category_name=category_name)
            new_category.save()
            return redirect('index')  # Redirect to index after adding category
        else:
            error_message = 'Category name is required'
            return render(request, 'add-category.html', {'error_message': error_message})
    else:
        # If GET request just render the add-category page
        if request.user.is_authenticated:
            return render(request, 'add-category.html')
        else:
            # If user is not authenticated, redirect to login
            return redirect('login')

def show_categories(request):
    categories = Category.objects.all()

    if categories is not None:
        return render(request, 'show-categories.html', {'categories': categories})
    else:
        return render(request, 'show-categories.html')

def show_article(request, pk):
    # This view will render the show-article page
    show_article = BlogCreatorPost.objects.get(id=pk) # Get the article by primary key (pk)
    latest_articles = BlogCreatorPost.objects.order_by('-created_at')[:2] # Get the two most recent posts
    comments = Comment.objects.filter(blogcreatorpost=show_article).order_by('-publication_date') # Get comments for the article

    # If the article does not exist, return an error message
    if not show_article:
        return render(request, 'show-article.html', {'error_message': 'Article not found'})
    
    # This logic will render the show categories page
    categories = Category.objects.all() # Get all categories
    if not categories:
        return render(request, 'show-categories.html', {'error_message': 'No categories found'})

    # Render the show-article page with the article and latest articles
    return render(request, 'show-article.html', {'show_article': show_article, 'latest_articles': latest_articles, 'comments': comments, 'categories': categories})

@login_required
def post_comments(request):
    # This view will render the post-comments page
    if request.method == 'POST':
        comment = request.POST.get('comment')
        email = request.POST.get('email')
        blog_post_id = request.POST.get('blog_post_id')

        # Validate that all fields are provided
        if comment and email and blog_post_id:
            blog_post = BlogCreatorPost.objects.get(id=blog_post_id)
            new_comment = Comment.objects.create(
                user=request.user,
                blogcreatorpost=blog_post,
                comment=comment,
                email=email
            )
            new_comment.save()
            return redirect('show-article', blog_post_id)
        else:
            error_message = 'All fields are required'
            return render(request, 'index.html', {'error_message': error_message})
    else:
        return render(request, 'index.html')

@csrf_exempt
def post_articles(request):
    # This logic will fetch the categories
    categories = Category.objects.all() # Get all categories
    if not categories:
        return render(request, 'post-articles.html', {'error_message': 'No categories found'})
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        content = request.POST.get('content')
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)

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
            return render(request, 'post-articles.html', {'user_posts': user_posts, 'categories': categories})
        else:
            # If user is not authenticated, redirect to login
            return redirect('login')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
        
    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']

        if password == repeatPassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                error_message = 'Error creating account'
                return render(request, 'signup.html', {'error_message': error_message})
        else:
            error_message = 'Passwords do not match'
            return render(request, 'signup.html', {'error_message': error_message})
    
    return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('/')
