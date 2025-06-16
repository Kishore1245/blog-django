from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
import logging
from .models import Post , AboutUs
from django.http import Http404
from django.core.paginator import Paginator
from .forms import ContactForm
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .forms import ForgotPasswordForm  
from .forms import ResetPasswordForm  
from django.utils.http import urlsafe_base64_decode

from django.contrib.auth.decorators import login_required, permission_required
from .models import Category
from .forms import PostForm
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.
#posts = [
#        {'id' : 1, 'title': 'post 1', 'content' :'content of post 1'},
#        {'id' : 2, 'title': 'post 2', 'content' :'content of post 2'},
#        {'id' : 3, 'title': 'post 3', 'content' :'content of post 3'},
#        {'id' : 4, 'title': 'post 4', 'content' :'content of post 4'},
#   ]

def index(request):
    blog_title = "Latest Posts"
    #getting data from post model
    all_posts = Post.objects.all()

    #paginate
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'blog_title': blog_title, 'page_obj': page_obj})
    
 
def detail(request, slug):
   # post = next((item for item in posts if item['id'] == int(post_id)), None)
   try:
      #getting data from model by post id
      post = Post.objects.get(slug=slug)
      related_posts = Post.objects.filter(category = post.category).exclude(pk=post.id)
   except Post.DoesNotExist:
    raise Http404("Post Does not Exist")
   return render(request, 'detail.html', {'post': post, 'related_posts':related_posts})

    #logger = logging.getLogger("TESTING")
    #logger.debug(f'Post variable is {post}')
    

def old_url_redirect(request):
    return redirect(reverse('blog:new_page_url'))

def new_url_view(request):
    return HttpResponse("This is New Url") 

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        logger = logging.getLogger("TESTING")
        if form.is_valid():
            logger.debug(f'POST Data is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['message']}')
            #send email or save in database
            success_message = 'Your Email has been sent!'
            return render(request,'contact.html', {'form':form,'success_message':success_message})
        else:
            logger.debug('Form validation failure')
        return render(request,'contact.html', {'form':form, 'name': name, 'email':email, 'message': message})
    return render(request,'contact.html')


def about(request):
    about_content = AboutUs.objects.first()

    if about_content is None or not about_content.content:
        about_content = "Default content goes here."
    else:
        about_content = about_content.content

    return render(request, 'about.html', {'about_content': about_content})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            
            # Add user to "Readers" group
            readers_group, created = Group.objects.get_or_create(name="Readers")
            user.groups.add(readers_group)
            
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('blog:login')  # Redirect to login or other page
    else:
        form = RegisterForm()
        
    return render(request, 'register.html', {'form': form})


def login_view(request): 
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('blog:dashboard')
            else:
                messages.error(request, 'Invalid username or password.')  
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


def dashboard(request):
    blog_title = "My Posts"
    #getting user posts
    all_posts = Post.objects.filter(user=request.user)

    # paginate
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'dashboard.html', {'blog_title': blog_title, 'page_obj': page_obj})


def logout(request):
    auth_logout(request) 
    return redirect('blog:index')  # Redirect to the Home page 

def forgot_password(request):
    form = ForgotPasswordForm()
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)

                # Generate token and UID
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                current_site = get_current_site(request)
                domain = current_site.domain

                # Email content
                subject = "Reset Password Requested"
                message = render_to_string('reset_password_email.html', {
                    'user': user,
                    'domain': domain,
                    'uid': uid,
                    'token': token
                })

                # Send email
                send_mail(subject, message, 'noreply@example.com', [email])
                messages.success(request, 'Reset password email has been sent.')
                return redirect('blog:login')  # Redirect to login or success page

            except User.DoesNotExist:
                messages.error(request, 'No account found with this email.')

    return render(request, 'forgot_password.html', {'form': form})

def reset_password(request, uidb64, token):
    form = ResetPasswordForm()
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            try:
                # ✅ Decode UID safely
                uid = urlsafe_base64_decode(uidb64).decode()
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been reset successfully!')
                return redirect('blog:login')
            else:
                messages.error(request, 'The password reset link is invalid or has expired.')
    
    return render(request, 'reset_password.html', {'form': form})

@login_required
@permission_required('blog.add_post', raise_exception=True)
def new_post(request):
    categories = Category.objects.all()  # Optional, only if needed in the template
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Assumes your Post model has a ForeignKey to User
            post.save()
            form.save_m2m()  # Needed if your form has many-to-many fields (e.g. tags)
            return redirect('blog:dashboard')

    return render(request, 'new_post.html', {'form': form, 'categories': categories})


# ✅ Edit Post View
@login_required
@permission_required('blog.change_post', raise_exception=True)
def edit_post(request, post_id):
    categories = Category.objects.all()
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post Updated Successfully!')
            return redirect('blog:dashboard')
    else:
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {
        'categories': categories,
        'post': post,
        'form': form
    })


# ✅ Delete Post View
@login_required
@permission_required('blog.delete_post', raise_exception=True)
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, 'Post Deleted Successfully!')
    return redirect('blog:dashboard')


# ✅ Publish Post View
@login_required
@permission_required('blog.can_publish', raise_exception=True)  # Custom permission
def publish_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.is_published = True
    post.save()
    messages.success(request, 'Post Published Successfully!')
    return redirect('blog:dashboard')
    