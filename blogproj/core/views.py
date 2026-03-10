from django.shortcuts import render,redirect,get_object_or_404
from core.models import User ,Blog
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth import authenticate
# Create your views here.

def register(request):
    if request.method == "POST":
         username = request.POST.get("username")
         email = request.POST.get("email")
         password1 = request.POST.get("password1")
         password2 = request.POST.get("password2")
         print("User details", username)

         if not username or not email or not password1:
              return redirect('register')
         
         if password1 != password2:
              return redirect('register')

         if User.objects.filter(email=email).exists():
              return redirect('login')
         
         User.objects.create_user(
              username=username,
              email=email,
              password=password1
         )
         return redirect('login')   
    return render(request, 'register.html')
    
def login(request):
     if request.method == "POST":
          username = request.POST.get("username")
          password = request.POST.get("password")
          print()
          user_exist = authenticate(request, username=username, password=password)
          print("User is", user_exist)
          
          if user_exist:
               request.session['user_id'] = user_exist.id
               request.session['email'] = user_exist.email
               
               return redirect('home')                               
          else:
               return redirect('register')
     return render(request, 'login.html')
     
def home(request):
     blogs = Blog.objects.all().order_by('-id')
     return render(request, 'home.html', {"blogs" : blogs})

def logout(request):
     request.session.flush()
     return redirect("login")

def create_blog(request):
     if request.method  == 'GET':
          print("I will check if user is logged in")
          print(request.session.items())
          if 'user_id' not in request.session:
               request.session['login_required'] = True
               return redirect('home')
     print(request.session)
     
     if request.method == "POST":
          title = request.POST.get("title")
          content = request.POST.get("content")
          
          user = User.objects.get(id = request.session['user_id'])

          Blog.objects.create(
               title=title,
               content=content,
               author=user
          )
          return redirect('home')
     return render(request, 'create_blog.html')

def edit_blog(request, id):
     blog = get_object_or_404(Blog, id=id)
     user_id = request.session.get('user_id')

     if not user_id or blog.author.id != user_id:
          return redirect('home')
     if request.method == "POST":
          blog.title = request.POST.get("title")
          blog.content = request.POST.get("content")
          blog.save()
          return redirect('home')
     
     return render(request, "edit_blog.html  ", {"blog" : blog})

def delete_blog(request, id):
     blog = get_object_or_404(Blog, id=id)
     user_id = request.session.get('user_id')

     if not user_id or blog.author.id != user_id:
          return redirect('home')
     blog.delete()
     return redirect('home')

def blog_detail(request, id):
     blog = get_object_or_404(Blog, id=id)
     return render(request, "blog_detail.html", {"blog" : blog})

          