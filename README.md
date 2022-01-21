# Django Tutorial!
## Sessions 1-14:
### Create virtual environment:
```python
# in Windows Powershell
python -m venv . # Create virtual environment in the directory
cd env
.\Scripts\activate # Activate the environment
deactivate # Deactivate the enviroment
# When activated:
pip install Django>=3.2,<3.3 # Install a specific version of Django
pip freeze # look at the current packages with their corresponding versions
pip freeze > requirements.txt # requirements.txt is a file, containing packages with their corresponsing versions, which contributed to the project. it is going to be a referrence in later uses.
pip install -r requirements.txt # Install all the packages mentions in the requirements.txt with their corresponding versions.
django-admin # Take a look at django-admin commands
django-admin startproject . # Start a default Django project in the mentioned directory
python manage.py runserver # Run the server according to the server files.
```
### Create view.py in the project folder (to render HTML)
```python
python manage.py # Tale a look at manage.py commands (looks like django-admin but more)
python manage.py startapp <component_name> # Creates a folder for a new component of the project.
python manage.py startapp articles
```
- Now go to TryDjango (server folder?) -> settings.py:
```python
# Under INSTALLED_APPS add:
INSTALLED_APPS = [
    'articles',
]
```
- Alter the models.py in articles folder.  
After each change in article's models.py file run:
```python
python manage.py makemigrations
python manage.py migrate # Some kind of apply changes?
```

## Session 15:
```python
from dataclasses import dataclass
@dataclass  
class BlogPost:  
    title: str  
    content: str  

obj = BlogPost(title='Hello World!', content='This is cool!')

# or! in the Terminl
>>> python manage.py shell 
from articles.models import Article
obj = Article(title='This is my first title!', content='cool!')
obj.title >>> 'This is my first title!'
obj.content >>> 'cool!'
obj.save() # Saves this with an incremental id (1,2,3,...)
# This instance is going to be saved db.sqlite3 file, right?
obj.id >>> 1 # if it's the first saved Article

# Load an already saved Article:
a = Article.objects.get(id=1)
a.title >>> 'This is my first title!'
a.content >>> 'cool!'
a.id >>> 1
```
## Session 16:
- Head over to server repository (TryDjango folder) -> views.py
```python 
from articles.models import Article

article_obj = Article.objects.get(id=x) # "X" being the id of the saved article object in the database
```
- Now you can use
```python
article_obj.title
article_obj.content
```
in order to show something in the browser which is originally located in the database.

## Session 17:
- Change views.py slightly by just using .format() instead of 'f string'
```python
context = {
    'title' = article_obj.title,
    'id' = article_obj.id,
    'content' = article_obj.content
}
html_string = '''
<h1>{title}, (id: {id})</h1>  
<p>{content}!</p>
'''.format(**context)
```
- Or you can do something like that if you are using a custome template
```python
f = open('my_template.html', 'r')
string = f.read()
html_string = string.format(**context)
```
- Create a file to like your template -> Folder: Templates  
Now add the string to that file like
```html
<h1>{title} (id: {id})</h1>  
<p>{content}</p>
```
- Again add your costume Templates file to settings.py -> TEMPLATES 
- <i>it doesn't have to be the same name of your function in view.py (home_view.html), i just named it that way to make it simpler to remember.</i>
- <b><i>Let's do it the wrong way first!</i></b>
```python
TEMPLATES = [
    {
        'DIRS' = [
            # right click on the Templates folder and copy it's path
            'C:\Users\Pazzo\Desktop\Python\Django\Project\Templates'
        ]
    }
]
```
- Now instead of using open() in views.py, use Django's built in loader  
-> views.py
```python
from django.template.loader import render_to_string

html_string = render_to_string('home_view.html', context = context)
return HttpResponse(html_string)
```
- didn't work, why? 
- for some reason, deviating from what the tutorial says, you have to put 'Relative Path' in dir 'DIRS' in 'settings.py'. like this:
```python
TEMPLATES = [
    {
        'DIRS' = [
            # right click on the Templates folder and copy it's path
            './Templates'
        ]
    }
]
```
- now you can see that it is not rendered correctly, the context is not being expanded and passed to the views.py correctly
- because what you've written in home_view.html is not standard html page, it's Django template. 
- <b><i>The right way:</i></b>
```html
<h1>{{title}} (id: {{id}})</h1>
<p>{{content}}</p>
```
- There are other ways, instead of render_to_strings
```python
from django.template.loader import get_template

template = get_template('home_view.html')
template_string = template.render(context)
# render_to_string does just this, but in a single line, so why bother?!
```
### Tepmlate inheritance:
- what we can do now is to use a base.html and just change little parts of it by home_view.html, like this:
- and we put BASE_DIR / 'Templates' instead of the copy paste path or relative path.
- a quick walkthrough would be:
- <i>for home_view.html</i>
```html
{% extends 'base.html' %}

{% block title %}
<h1>{{title}} (id: {{id}})</h1>
{% endblock title %}

{% block content %} 
<p>{{content}}</p>
{% endblock content %}
```
- <i>for base.html</i>
```html
<!DOCTYPE html>
<html>
    <head>
        {% block title %}
        {% endblock title %}
    </head>
    <body>
        {% block content %}
        {% endblock content %}
    </body>
</html>
```
## Session 18:
- Passing a list of numbers of even article objects to the webpage, printing them out in seperate lines
- Attaching a link to each of them
```python
object_list = Articles.objects.all() # This is not a List, it's a QuerySet
# Add to context
context = {
    'object_list' = object_list
}
```
- and for HTML
```html
{% for query in object_list %}
{% if query.title != '' %}
<li><a href = '/articles/{{x.id}}/'>{{x.title}} - {{x.content}}</a></li>
{% endif %}
{% endfor %}
```
## Session 19:
- Dynamic URL Routing
- add a path() in the TryDjano urls.py leading to the url you want plus the view you want to be rendered
- in the articles views.py:
```python
from articles.models import Article

def article_detail_view(request, id=None):
    article_obj = None
    if id is not None:
        article_obj = Article.objects.get(id=id)
    context = {
        'obj' : article_obj
    }
    return render(request, 'Articles/Detail.html', context = context)
```
- in a .html file, Templates/articles/Detail.html:
```html
{% extends 'Base.html' %}

{% block title %}
<h1>{{obj.title}}</h1>
{% endblock %}

{% block content %}
<p>{{obj.content}}</p>
{% endblock %}
```
- in the TryDjango urls.py:
```python
from articles import views
# Add this to urlpatterns
urlpatterns = [
    path('articles/<int:id>/', views.article_detail_view)
]
```
## Session 20:
- Super Users, Staff Users & the Django Admin
```python
python manage.py createsuperuser
```
- 127.0.0.1:8000/admin
- log in with you admin user and password, and then manage the other users there.
## Session 21:
- Register Model in the Admin  
to do that, just head to the articles/admin.py and add your model just like this:
```python
from articles.models import Article

admin.site.register(Article)
```
- now if you refresh the page you can see that a new section called Articles is inside your Articles tab in admin. 
- to make it more advanced and customized, add this in that same admin.py
```python
class ArticleAdmin(admin.ModelAdmin):
    # These names are predefined in Django maybe? or whatever
    # They cannot be changed, and even the list items are predefined and can't be random and self-chosen
    list_display = ['title', 'id']
    search_fields = ['id', 'title', 'content']

admin.site.register(Article, ArticleAdmin)
```
- Note that the things written in the ArticleAdmin class are very specific and changing them might crash the server. wierdly, they are some specific commands.
## Session 22:
- Search form and Request data
- let's add a search bar and a submit button in the home page (added to Base.html > body):
```html
<form>
    <input type='text' />
    <input type='submit' />
</form>
```
- this works, but not really! you need to give the text input a name so that it has some kind of identity. and then you have to make the form do some kind of action.
```html
<form action =''>
    <input type='text' name='q'/>
    <input type='submit' />
</form>
```
- this way when you submit whatever is written  in the text field you can see that the URL is now dynamic and is changing with the addition of 'q={your_search}'.
- the reason for 'q=...' is that the form's name is q
- <b>action</b> is actually the address where the text input content is being sent
```html
<form action = 'https://www.google.com'>
    <input type='text', name = 'q' />
    <input type ='submit' />
</form>
```
- now the thing you write and submit in the text field is passed to google.com and it will fill in the search bar (but won't search, how to do that??)
- ok enough kos kalak. let's get our search field to work.
- first you should make a view for it, in the articles/views.py:
```python
def article_search_view(request):
    context = {}
    return render(request, 'articles/search.html', context=context)
```
- let's make the Templates/articles/search.html:
```html
{% extends 'Base.html' %}

{% extends 'Base.html' %}

{% block title %}
{% if obj %}
<h1>{{obj.title}}</h1>
{% endif %}
{% endblock %}

{% block content %}
{% if obj %}
<p>{{obj.content}}</p>
{% endif %}
{% endblock %}
```
- now let's add the searched address to the urls.py:
```python
urlpattens = [
    path('articles/', views.articles_search_view)
]
```
- let's get the text which is sent by submitting your query in articles/views.py:
```python
def article_search_view(request):
    query_dict = request.GET

    # let's make it in a way so that non sense searchs won't crash our website
    article_obj = None
    try:
        query = int(query_dict.get('q')) # <input type='text' name='q' />
        article_ids = [article.id for article in Article.objects.all()]
        if query not in article_ids:
            query = None
    except:
        query = None
    
    if query is not None:
        article_obj = Article.objects.get(id=query)
    context = {
        'obj': article_obj
    }
    return render(request, 'articles/search.html', context=context)
```
- Now it should work and it will filter irrelevant results.
## Session 23:
- Add a form in Django to create an Article on your own!
- create an html file in Templates/articles/Create.html:
```html
<form method='POST'>
    <input type='text' name='title' placeholder='Title' />
    <textarea name='content' placeholder='Content'></textarea>
    <button type='submit'>Create Article</button>
</form>
```
- now in your articles/views.py add:
```python
def article_create_view(request):
    context = {}
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        article_object = Article.objects.create(title=title, content=content)
    context['title'] = title
    context['content'] = content
    context['object'] = article_object
    context['created'] = True
    return render(request, 'articles/Create.html', context=context)
```
- now let's add csrf_token (a security token to prevent bad data sent to you) to Create.html:
- <b><i> you can use a decorator @csrf_exempt but it can cause risks, but you might want that if you are building some sort of REST API. </i></b>
```html
{% csrf_token %}
<form method='POST'>
    <input type='text' name='title' placeholder='Title' />
    <textarea name='content' placeholder='Content'></textarea>
    <button type='submit'>Create Article</button>
</form>
```
- add new path to TryDjango/urls.py:
```python
urlpatterns=[
    path('article/create/', views.article_create_view)
]
```
- in order to make it look better we change Create.html to:
```html
{% extends 'Base.html' %}

{% block title %}
<h1>{{obj.title}}</h1>
{% endblock %}

{% block content %}
{% if not created %}
<form method='POST'>
    {% csrf_token %}
    <input type='text' name='title' placeholder='Title'/><br><br>
    <textarea name='content' placeholder='Content'></textarea><br><br>
    <button type='Submit'>Create Article</button>
</form>
<h3><a href='../../'>Back to Home</a></h3>
{% else %}
<h3>Your article was created!</h3>
<a href='../{{ object.id }}'>Go to Article</a>
{% endif %}
{% endblock %}
```
## Session 24:
- Create a Login view to authenticate users
- create Templates/Accounts/Login.html:
```html
{% extends "Base.html" %} 

{% block title %}
<h1>Login Page</h1>

{% endblock title %} 
{% block content %} 
<form method='POST'>
    <h3>Enter you Username and Password</h3>
    {% csrf_token %}
    <input type='text' name='username' placeholder='Userame'/><br>
    <input type='password' name='password' placeholder='Password'/><br>
    <button type='Submit'>Login</button>
</form>
{% if error %}
<h3 style='color: red'>{{ error }}</h3>
{% endif %}
<h3><a href='../'>Back to Home</a></h3>
{% endblock content %} 
```
- Now create an app (component) to handle login stuff:
```python
python manage.py startapp accounts
```
- in the accounts/views.py add:
```python
from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            context = {
                'error':'Invalid Username or Password'
            }
            return render(request, 'Accounts/Login.html', context=context)
        login(request, user)
        return redirect('/admin')
    context = {}
    return render(request, 'Accounts/Login.html', context=context)

def logout_view(request):
    context={}
    return render(request, 'Accounts/Logout.html', context=context)

def register_view(request):
    context={}
    return render(request, 'Accounts/Register.html', context=context)
```
- now add the needed url to the TryDjango/urls.py:
```python
form accounts.views import (
    login_view,
    logout_view,
    register_view
)

# for now, put the urls in an alphabetic order
urlpatterns=[
    path('login/', login_view)
]
```
- now by doing so you should be able to:
    - make the login page
    - authenticate the user and return an error if it was invalid
    - login to /admin if the user exists
## Session 25:
- now let's implement something to logout
- change the Login.html like  this:
```html
{% if not request.user.is_authenticated %} 
<form method='POST'>
    <h3>Enter you Username and Password</h3>
    {% csrf_token %}
    <input type='text' name='username' placeholder='Userame'/><br>
    <input type='password' name='password' placeholder='Password'/><br>
    <button type='Submit'>Login</button>
</form>
{% if error %}
<h3 style='color: red'>{{ error }}</h3>
{% endif %}
{% else %} 
<p>You are already logged-in, do you want to <a href='/logout/'>Logout</a>?</p>
{% endif %} 
```
- now in the accounts/views.py:
```python
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/login/')  
    context = {}    
    return render(request, 'Accounts/Logout.html', context=context)
```
- after that make a Logout.html in Templates/Accounts:
```html
{% extends "Base.html" %} 

{% block title %}
<h1>Logout Page</h1>

{% endblock title %} 
{% block content %}
{% if request.user.is_authenticated %} 
<form method='POST'>
    {% csrf_token %}
    <p>Are you sure you want to Logout?</p>
    <button type='submit'>Yes, Logout.</button>   
</form>
{% else %} 
<p>You are not Logged-in! <a href='/login/'>Login.</a></p> 
{% endif %} 
{% endblock content %} 
```
- now in the TryDjano/urls.py:
```python
urlpatterns =[
    path('logout/', logout_view)
]
```
## Session 26:
- Login required for article creation:
- 2 major ways, 1, you can add this to articles/views.py > article_create_view:
```python
def article_create_view(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
```
- because you might need to copy and paste these lines over and over again, the other way is to use a prebuilt decorator:
```python
from django.contrib.auth.decorators import login_required

@login_required
def article_create_view(request):
    ....
```
- but note that this will automatically direct you to Django's default login page which is 'accounts/login/'.
- to overwrite this predefined path, go to TryDjango/settings.py, and somewhere in the middle add:
```python
LOGIN_URL = 'login/'
```
- note that the caps lock and the spelling is important.
## Session 27:
- go in articles folder and create a python file forms.py:
```python
from django import forms

class ArticleForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField()
```
- go to articles/views.py
```python
from articles.forms import ArticleForm

def article_create_view(request):
    form = ArticleForm()
    context = {
        'form': form
    }
```
- head to Templates/Articles/Create.html and add this:
```html
{% if not created %}

{{ form.as_p }}
```
- you can now remove input textfields from Create.html and make it like this:
```html
{% block content %}
{% if not created %}


<form method='POST'>
    {% csrf_token %}
    {{ form.as_p }}

    <button type='Submit'>Create Article</button>
</form>
<h3><a href='../../'>Back to Home</a></h3>
{% else %}
<h3>Your article was created!</h3>
<a href='../{{ object.id }}'>Go to Article</a>
{% endif %}
{% endblock %}
```
- now clean the input data (what is cleaning exactly??):
```python
class ArticleForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField()

    # this is not necessary
    def clean_title(self):
        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        return title
```
- now head to the articles/views.py:
```python
if reequest.method == 'POST':
    form = ArticleForm(request.POST)
    if form.is_valid(): # this is if the form is cleaned
        title = form.cleaned_data.get('title')
        content = form.cleaned_data.get('content')
        # tab everything else but return in
```
- head to forms.py:
```python
class ArticleForm(forms.Form):

    def clean_title(self):
        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        if title.lower().strip() == 'something':
            raise forms.ValidationError('This name is taken.')
        return title
```
- nothing is shown, why?
- the form instance #2 was never brought back to the context, so let's do it.
- head to articles/views.py:
```python
@login_required
def article_create_view(request):
    form = ArticleForm()
    context = {
        'form': form
    }
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        context['form'] = form
        if form.is_valid():
            ...
```
- let's change the code in a better way (getting rid of a number of lines):
```python
def article_create_view(request):
    form = ArticleForm(request.POST or None)
    context = {
        'form' : form
    }
    if form.is_valid():
        ...
```
- add another method in forms.py:
```python
def clean(self):
    cleaned_data = self.cleaned_data
    title = cleaned_data.get('title')
    if title.lower().strip() == 'something':
        # This is a nonfield error -> class='errorlist nonfield'
        raise forms.ValidationError('This title is taken.')
    return cleaned_data
```
- this is a nonfield error, let's make it field error:
```python
def clean(self):
    cleaned_data = self.cleaned_data
    title = cleaned_data.get('title')
    if title.lower().strip() == 'something':
        # This is a field error -> class='errorlist'
        self.add_error('title', 'This title is taken.')
    return cleaned_data
```
- field errors are somehow specified maybe?
- you can also add another errors:
```python
def clean(self):
    cleaned_data = self.cleaned_data
    title = cleaned_data.get('title')
    if title.lower().strip() == 'something':
        # This is a field error -> class='errorlist'
        self.add_error('title', 'This title is taken.') # field error (about title field)
    content = cleaned_data.get('content')
    if 'something' in content or 'something' in title:
        self.add_error('content', 'This phrase is not allowed.') # field error (about content field)
        raise forms.ValidationError('This combination is not allowed.') # nonfield (about entire form)
    return cleaned_data
```
## Session 28:
- let's build ModelForm (what is it and why is that?) in forms.py:
```python
from articles.models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
```
- now let's clean up articles/views.py:
```python 
def article_create_view(request):
    form = ArticleForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        article_obj = form.save()
        context['form'] = ArticleForm() # we can put (request.POST or None)
        context['object'] = article_obj
        context['created'] = True
    return render(request, 'articles/Create.html', context=context)
```
- let's a proper validation for your title
- under the class of ArticleForm in forms.py:
```python
def clean(self):
        data = self.cleaned_data
        title = data.get('title')
        qs = Article.objects.all().filter(title__icontains=title) 
        # you don't need .all() you can remove it.
        # it's just a query set, it finds if any of the titles contains your new title.
        if qs.exists():
            self.add_error('title', f'\"{title}\" is already in use!')
        return data
```
## Session 29:
- create a registeration view, in accounts/views.py:
```python
from django.contrib.auth.forms import UserCreationForm

def register_view(request):
    form = UserCreationView(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        return redirect('/login')
    context = {
        'form': form
    }
    return render(request, 'Accounts/Register.html', context=context)
```
- now go to urls.py:
```python
urlpatterns = [
    path('/register', register_view)
]
```
- you don't want to register a user if they are authenticated, or logged-in.
- so let's create a Register.html:
```html
{% extends "Base.html" %} 

{% block title %}
<h1>Login Page</h1>

{% endblock title %} 
{% block content %} 
{% if not request.user.is_authenticated %} 
<form method='POST'>
    {% csrf_token %}
    {{ form.as_p }}
    <button type='Submit'>Register</button>
</form>
<p>Already have an account? <a href='/login'>Login</a></p>
{% else %} 
<p>You are already logged-in and cannot register, do you want to <a href='/logout/'>Logout</a>?</p>
{% endif %} 

<h3><a href='../'>Back to Home</a></h3>
{% endblock content %} 
```
## Session 30:
- AuthenticationForm, head to accounts/views.py:
```python
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method=='POST':
        form = AuthenticationForm(request, data=request.POST) # this unique module has the request as an input, but others don't  
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm(request)
    context = {
        'form': form
    }
    return render(request, 'Accounts/Login.html', context=context)
```
- let's changes Login.html:
```html
{% endblock title %} 
{% block content %} 
{% if not request.user.is_authenticated %} 
<form method='POST'>
    {% csrf_token %}
    {{ form.as_p }}     
    <button type='Submit'>Login</button>
</form>
{% else %} 
<p>You are already logged-in, do you want to <a href='/logout/'>Logout</a>?</p>
{% endif %} 
<p>Need an account? <a href='/register'>Register</a></p>


<h3><a href='../'>Back to Home</a></h3>
{% endblock content %} 
```
## Session 31:
- Development environment and Production environment
- SECRET_KEY and DEBUG are essential for development but shouldn't be altered in production.
- here we introduce .env file (manage environment variables)
- environment variables allow you to inject varaibles and settings or data that maybe you don't wanna hard code in somewhere like settings.py.
- .env uses key:value pairs
- so let's head to TryDjano/settings.py:
```python
import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-%j7o149-csvr6y(-_qy!g1^-*@=!@86ja1(bu1hsh^bqk&!4m*') # SECRET_KEY from .env file or the default one

# this should be False in case of production, not development
# makes the page not found more classic and detail-less
DEBUG = str(os.environ.get('DEBUG')) == '1'

# what domains you want to allow this server to run with
ENV_ALLOWED_HOST=  os.environ.get('DJANGO_ALLOWED_HOST') or None
ALLOWED_HOSTS = []
if ENV_ALLOWED_HOST is not None:
    ALLOWED_HOSTS = [ENV_ALLOWED_HOST]
```
- now let's make a .env file in the root Project folder (next to manage.py) in order to maintain environment variables in it.
- put the required environment variables in .env file:
```env
SECRET_KEY = <whatever>
DEBUG = 1
```
- now let's install dotenv package
- <b> Note that django-dotenv is required. python-dotenv is not</b>
```cmd
pip install django-dotenv
```
- now let's load .env file in manage.py:
```python
import dotenv

def main():
    dotenv.read_dotenv()
    ...
```
- now re-run the server
- now you can changes environment variables (inject them)
- after changing any of the environment variables, you have to re-run the server.
- if the .env file doesn't exist it will show you a user warning this way.
- what if you wanted to put .env in a different path?
- head to manage.py
```python
import pathlib

def main():
    DOT_ENV_PATH = pathlib.Path() / '.env'
    if DOT_ENV_PATH.exists():
        dotenv.read_dotenv(str(DOT_ENV_PAHT))
    else:
        print('No .env file found. Make sure to add it.')
        # This is the  default thing that Django does in case of none existance
```
## Session 32:
- let's get our django project to be deployed on app platform. 
- getting it live on digital oceans app platform
- head to the like below:  https://www.codingforentrepreneurs.com/blog/prepare-django-for-digital-ocean-app-platform
- let's do whatever is in that site.
- add these to requrements.txt:
```python
gunicorn # For productin purposes
psycopg2-binary # PostgreSQL
```
- add a runtime.txt next to requirements.txt
```python
python-3.8.10
```
- how to create SECRET_KEY ?
1. in the shell run, it will print out a password for you and you can copy and paste it in your .env file:  
    ```python
    python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'  
    ```
2. ```python
    import uuid
    print(uuid.uuid4())
    ```
- copy and paste PostgreSQL data in your settings.py, under the DATABASE variable:
```python
POSTGRES_DB = os.environ.get("POSTGRES_DB") # database name
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD") # database password
POSTGRES_USER = os.environ.get("POSTGRES_USER") # database username
POSTGRES_HOST = os.environ.get("POSTGRES_HOST") # database host
POSTGRES_PORT = os.environ.get("POSTGRES_PORT") # database port

POSTGRES_READY = (
    POSTGRES_DB is not None
    and POSTGRES_PASSWORD is not None
    and POSTGRES_USER is not None
    and POSTGRES_HOST is not None
    and POSTGRES_PORT is not None
)

if POSTGRES_READY:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": POSTGRES_DB,
            "USER": POSTGRES_USER,
            "PASSWORD": POSTGRES_PASSWORD,
            "HOST": POSTGRES_HOST,
            "PORT": POSTGRES_PORT,
        }
    }
```
- it's really good to have the same database in development than in production, but here we won't head to PostgreSQL.
- now you can use git and jump to the deploy in digital ocean either blogpost or video.
- but in the next part we will check out basics of git and learn how to deploy our projects in git.
## Session 33:
- "pwd" inside a folder
- use the command below to initialize git in that directory (entire folder)
```cmd
git init
```
other commands in git:
```python
git status # status of files in that directory
git add main.py # track a specific file (like makemigrations and migrate!!!)
git commit -m 'New Update' # commit tracked files and -m for message
git diff main.py # shows change between the last commit and current version
git log # see all commits that you made 
```
- to revert a commit:
```python
git log # copy the commit code (very long code in front of a specific 'commit')
git reset <code> --hard # reset the commit to the last version
```
- but in VSCode you can just ctrl+z and commit that again.
```python
# make a directory and cd to that in shell
git clone <github source repository> . # . is to clone the repository in the directory you are currently in
# you will have all the commit history via git status
git pull # get the most recent change from git
# downloading zipfile from github instead of git pull won't give you commit history with git status
```
- .gitignore is a file that make sure certain files and folders are not tracked
- if you delete .git file from a folder, it means that you are disconnecting that directory from git.
- so what to do if you deleted .git file but wanted git back?
- delete the folder and clone (same steps) again.
    - you won't be able to clone again in that directory without deleting it at first. because it says that the directory is not empty.
- if you wanted to add an already existing directory to a fresh git repository:
    - make a brand new empty repository in github.com
    - delete the .git file from the folder if it exists
    ```python
    git init
    git remote add origin <repository url>
    git add --all # or git add . (same meaning)
    git commit -m 'Initial commit or whatever!'
    ```
```python
git remote # the hosts that you are going to push code to (hence remote not local)
got remote -v 
git remote add github <exact same repository link>
git remote -v # notice that it's name is changed from origin to github (most common is the default origin)
git push ogirin main
git remote remove origin
git remote remove github
git remote add origin
git push origin main
```
- so just for a recap, the main commands are:
```python
mkdir
git init
git remote add origin 
# commands above are like one time per project
git add .
git commit -m 'Your message'
git push origin main
# these three commands are going to be done several times
# and some handy commands
git status
git log
git diff
git log
```
- note that you might be on branch master or main. when i did it, it was master, so if you faced an error, it's maybe because you need to git push origin master
## Session 34:
- deploy our project into production using digital ocean platform
- let's read about these:
    - docker
    - kubenetes
    - database port
    - migration
## Session 35:
- automated test, how to run it? here is a built-in way: 
```python
python manage.py test
```
- runs a test on the whole project
- what is worth testing?
- <b>SERCRET_KEY</b> for example
- catatrophic errors won't be missed since they cause the server to crash and will be noticed easily.
- but problems like <b>very bad secret_key</b> is not something that causes an error, what to to?
- in your configuration folder (Project/TryDjango) create tests.py:
```python
import os
from django.test import TestCase
# or do this for getting secret key
from django.conf import settings
from django.contrib.auth.password_validation import validate_password


class TryDjangoConfigTest(TestCase):
    # all the methods have to start with test_<anything> 
    # Checkout python unittest > TestCase for more info
    def test_secret_key_strength(self):
        # get the secret key
        SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
        # another way: SECRET_KEY = settings.SECRET_KEY
        # how to make sure the password is good?
        try:
            is_strong = validate_password(SECRET_KEY)
        except Exception as e:
            msg = f'Weak SECRET_KEY {e.messages}'
            self.fail(msg) # what message to fail with
```
- be aware of <b>Test Driven Development</b> which basically says you should run tests from the beginning. this might make you to design specifically to pass the test, which is not good. as a beginner don't mind about test from the beginning.
## Session 36:
- change articles/models.py:
```python
from django.db import models

# Create your models here.

class Article(models.Model):
    # put CharField() for title to set max_character length
    # head to the Django Model-field-types
    title = models.CharField(max_length = 100) 
    content = models.TextField()
```
- now it's time for:
```python
python manage.py makemigrations
python manage.py migrate
```
- makemigrations is telling django to be prepared for a database change
- in deployment (production) this is a "Job"
- making changes to model fields
- in the articles/models.py:
```python
from django.db import models
from django.utils import timezone

# Create your models here.

class Article(models.Model):
    # put CharField() for title to set max_character length
    # head to the Django Model-field-types
    title = models.CharField(max_length = 100) 
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # auto_now: whenever the model is saved is going to be saved
    updated = models.DateTimeField(auto_now=True)
    # auto_now_add: whenever the model is added is going to be added
    # now that we added new fields to the Article Model, Django asks what to do with the already existing articles
    # as you know, their new added fields are empty
    # add defualt from shell when shows the warning, timezone.now
    publish = models.DateField(auto_now=False, auto_now_add=False, default = timezone.now) # DateField just has the calender, no time
    # null=True: in the databse it can be empty
    # blank=True: in django forms or django admin in can be empty
    '''why is it showing in the /admin/<article_id> ?'''
    ''' how to delete a field? or how to reset a mistaken field?'''
    # just comment the field commmand and makemigrations and migrate > it is deleted!
    '''for changing a field, simply remove it (by commenting) and re add the altered one'''
```
- to show contents in the django admin, head to the articles/admin.py:
```python
from django.contrib import admin
from articles.models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'timestamp', 'updated']
    search_fields = ['title', 'content', 'id']

admin.site.register(Article, ArticleAdmin)
```
## Session 37:
- in a common website, instead of model id in the url, you are more likely to see a 'Slug'. 
- inside the articles/models.py add this under the 'title' variable:
```python
title = models.CharField(max_length = 100) 
    # add a Slug, to use instead of the model id in the url
    slug = models.SlugField(blank=True, null=True)
```
- now how to turn any title or string in a slugified item?
- go into the python shell:
```python
python manage.py shell
from django.utils.text import slugify
slugify('Hello world this is amazing! cool! @#$@^@')
>>> 'hello-world-this-is-amazing-cool'
```
- how are we going to create a slugfield?
- let's overwrite the save method in the Article Model.
```python:
from django.utils.text import slugify

class Article(models.Model):
    ...

    def save(self, *args, **kwargs):
        # let's change somethings 
        # and add this if in order to change the slug ever after the title was created (with the model)
        if self.slug is None:
            self.slug = slugify(self.title)
        super.save(*args, **kwargs)
```
- overwritting the save() method is not always recommended.
- now the problem is what if we have the same title or almost exact titles for some models? the slugs and so the urls would be the same which is not good at all!
- up to now, we didn't implement this slugified title in the urls did we? :/
## Session 38:
- what are 'Signals'?
- in the articles/models.py:
```python
from django.db.models.signals import pre_save, post_save

# what signals do is essentially the same as the .save() method we customized.
class Article(models.Model):
    ...
    def save(self, *args, **kwargs):
        super.save(*args, **kwargs)
    
def article_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        instance.slug = slugify(instance.title)

pre_save.connect(article_pre_save, sender=Article)

def article_post_save(sender, instance, created, *args, **kwargs):
    # we use this if to prevent recursion
    if created:
        instance.slug = 'my slug'
        # or you can say: instance.slug = slugify(instance.title)

        # pre_save and post_save are being called before and after each save, so calling instance.save() inside post_save function won't actually make an infinite loop??
        instance.save()

post_save.connect(article_post_save, sender=Article)
```
- let's improve our slug rather than something fixed or even slugified title. 
## Session 39:
- let's create unique slugs
- we have to use django query sets and lookups
- then we have to change our views from using ids to using slugs (the main purpose of slugs)
```python
python manage.py shell
from articles.models import Article

obj = Article.objects.get(slug='my slug')
# query sets
qs = Article.objects.all()
qs.count()
len(qs)
# .count() is more efficient cause it's django specific
# let's see if a slug exists in the database
qs = Article.objects.filter(slug='hello-world')
qs # this will return all articles with this slug
qs = Article.objects.filter(slug='hello-world').filter(title='Hello world')
# to make it case insensitive
qs = Article.objects.filter(title__iexist='Hello World')


# and this one is case sensitive
qs = Article.objects.filter(title__exist='Hello World')

# or whether it contains (not being the exact same)
qs = Article.objects.filter(title__contain='Hello World') # case sensitive
qs = Article.objects.filter(title__icontain='Hello World') # case insensitive

# this is called querying the database
```
- let's change the articles/models.py a bit:
```python

def slugify_instance_title(instance, save=False):
    slug = slugify(instance.title)
    qs = Article.objects.filter(slug=slug).exclude(id=instance.id)
    # the exclude method is useful when u want to edit the same article, cause u don't want the current instance's slug to be included in the query
    if qs.exists():
        slug = f'{slug}-{qs.count()+1}'
    instance.slug = slug
    if save:
        instance.save()
    return instance

def article_pre_save(sender, instance, *args, **kwargs):
    print('pre_save')
    if instance.slug is None:
        slugify_instance_title(instance)

pre_save.connect(article_pre_save, sender=Article)

def article_post_save(sender, instance, created, *args, **kwargs):
    print('post_save')
    # we write this if to prevent recursion
    if created:
        slugify_instance_title(instance, save=True)

post_save.connect(article_post_save, sender=Article)
```
- the problem here is that we have multiple instances of the same slug again! what to do??, next episode :))
## Session 40:
- Auto generate new slugs
- let's use recusion, head to the articles/models.py:
```python
import random

class Article(models.Model):
    slug = models.SlugField(unique=True, blank=True, null=True)
    ...


def slugify_instance_title(instance, save=False, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    CLASS = instance.__class__
    qs = CLASS.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        rand_int = random.randint(300_000, 500_000) # adding randomness
        slug = f'{slug}-{rand_int}'
        return slugify_instance_title(instance, save=save, new_slug=slug)
    instance.slug = slug
    if save:
        instance.save()
    return instance
```
- this way we are adding some kind of randomness.
- how to make exact numbers of the times the slug is repeated instead of this random?
- let's bring slugify_instance_title() to utils.py and done!
## Session 41:
- let's make sure our slugify and stuff words fine, so head to articles/tests.py:
```python
from articles.models import Article

class ArticleTestCase(TestCase):

    def test_queryset_exists(self):
        qs = Article.objects.all()
        self.assertTrue(qs.exists())
```
- now in the shell:
```shell
python manage.py test articles # to specify only test articles not the whole thing
```
- it fails, why? <b>because something with the database made for the tests is wrong</b>
- tests have their own 'Testing databases'
- so again in the articles/tests.py:
```python
from articles.models import Article

class ArticleTestCase(TestCase):
    def setUp(self):
        Article.objects.create(title='Hello world', content='something random')
    def test_queryset_exists(self):
        qs = Article.objects.all()
        self.assertTrue(qs.exists())
```
- let's make another tests for slugs also:
```python
from django.test import TestCase
from articles.models import Article
from django.utils.text import slugify
# Create your tests here.

class ArticleTestCase(TestCase):
    def setUp(self):
        self.number_of_articles = 5
        for i in range(0, self.number_of_articles):
            Article.objects.create(title='Hello world', content='Something Random')

    def test_queryset_exists(self):
        qs = Article.objects.all()
        self.assertTrue(qs.exists())

    def test_queryset_count(self):
        qs = Article.objects.all()
        self.assertEqual(qs.count(), self.number_of_articles)
    
    def test_slug(self):
        obj = Article.objects.all().order_by('id').first() # grab the first item in the queryset (like qs[0])
        title = obj.title
        slug = obj.slug
        slugified_title = slugify(title)
        self.assertEqual(slug, slugified_title)

    def test_hello_world_slug(self):
        qs = Article.objects.exclude(slug__iexact='hello-world')
        for obj in qs:
            title = obj.title
            slug = obj.slug
            slugified_title = slugify(title)
            self.assertNotEqual(slug, slugified_title)
```
## Session 42:
- let's add another test functions:
```python
from articles.utils import slugify_instance_title

class ArticleTestCase(TestCase):
    ...

    def test_slugify_instance_title(self):
            obj = Article.objects.all().last()
            new_slugs = []
            for i in range(5):
                instance = slugify_instance_title(obj, save=False)
                new_slugs.append(instance.slug)

            unique_slugs = list(set(new_slugs))
            self.assertEqual(len(new_slugs), len(unique_slugs))
```
- after running test articles, we get success, but it's a false sense of security, because only 5 slugs was tested. you can test 50_000.
- but to be a sure you have to make more articles instead of testing more slugs:
```python
from django.test import TestCase
from articles.models import Article
from django.utils.text import slugify
from articles.utils import slugify_instance_title


class ArticleTestCase(TestCase):
    def setUp(self):
        self.number_of_articles = 500
        for i in range(0, self.number_of_articles):
            Article.objects.create(title='Hello world', content='Something Random')

    def test_queryset_exists(self):
        qs = Article.objects.all()
        self.assertTrue(qs.exists())

    def test_queryset_count(self):
        qs = Article.objects.all()
        self.assertEqual(qs.count(), self.number_of_articles)
    
    def test_slug(self):
        obj = Article.objects.all().order_by('id').first() # grab the first item in the queryset (like qs[0])
        title = obj.title
        slug = obj.slug
        slugified_title = slugify(title)
        self.assertEqual(slug, slugified_title)

    def test_hello_world_slug(self):
        qs = Article.objects.exclude(slug__iexact='hello-world')
        for obj in qs:
            title = obj.title
            slug = obj.slug
            slugified_title = slugify(title)
            self.assertNotEqual(slug, slugified_title)

    def test_slugify_instance_title(self):
        obj = Article.objects.all().last()
        new_slugs = []
        for i in range(25):
            instance = slugify_instance_title(obj, save=False)
            new_slugs.append(instance.slug)

        unique_slugs = list(set(new_slugs))
        self.assertEqual(len(new_slugs), len(unique_slugs))

    def test_slugify_instance_title_redux(self):
        # make a list after a queryset
        slug_list = Article.objects.all().values_list('slug', flat=True)
        unique_slug_list = list(set(slug_list))
        self.assertEqual(len(slug_list), len(unique_slug_list))
```
- one of the ways to facilitate test process, is to create all the articles once in a persistant database, a testing database which is a stand alone. which is not in the scope of thie tutorial.
## Session 43:
- slugs in dynamic urls finally!
- head to the TryDjano/urls.py and change this line only:
```python
path('articles/<slug:slug>/', article_detail_view),
```
- now head to the articles/views.py and change this function:
```python
from django.http import Http404  

def article_detail_view(request, slug=None):
    article_obj = None
    if slug is not None:
        try:
            article_obj = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404

        # this shouldn't be even a case! but just to be sure
        except Article.MultipleObjectsReturned:
            article_obj = Article.objects.filter(slug=slug).first()
        except:
            raise Http404
    context = {
        'obj' : article_obj
    }
    return render(request, 'Articles/Detail.html', context = context)
```
- now let's go to Templates/HomeView.html and just change this line of code:
```html
<li><a href='/articles/{{x.slug}}/'>{{x.title}} - {{x.content}}</a></li>
```
## Session 44:
- get absolute url method
- the goal is to make the dynamic url based of of the instance itself, not being hard-coded
- so head to the articles/models.py:
```python
class Article(models.Model):
    ...

    def get_absolute_url(self):
        return f'/articles/{self.slug}'
```
- and in the HomeView.html:
```html
<li><a href='{{ x.get_absolute_url }}'>{{x.title}} - {{x.content}}</a></li>
```
- this is a more robust way to declare dynamic urls. hence it's not perfect yet.
## Session 45:
- Django URLs Reverse
- you can use 'name' argument in path in the urls.py in order to address the urls easier later.
```python
path('articles/create/', article_create_view, name='article-create'),
path('articles/<slug:slug>/', article_detail_view, name='article-detail')
```
- and in the HomeView.html:
``` html
<h3><a href='{% url "article-create" %}'>Create Article</a></h3>
```
- and in the articles/models.py:
```python
class Article(models.Model):
    ...

    def get_absolute_url(self):
            # return f'/articles/{self.slug}/'
            return reverse('article-detail', kwargs={'slug':self.slug})
```
- and in the articles/views.py:
```python
@login_required
def article_create_view(request):
    form = ArticleForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        article_obj = form.save()
        context['form'] = ArticleForm() # we can put (request.POST or None)
        context['object'] = article_obj
        context['created'] = True
        return redirect('article-detail', slug=article_obj.slug)
    return render(request, 'articles/Create.html', context=context)
```
- or better to say:
```python
@login_required
def article_create_view(request):
    form = ArticleForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        article_obj = form.save()
        context['form'] = ArticleForm() # we can put (request.POST or None)
        context['object'] = article_obj
        context['created'] = True
        return redirect(article_obj.get_absolute_url())
    return render(request, 'articles/Create.html', context=context)
```
## Session 46:
- complex search using djdango query lookup
- we want to show querysets in the search result instead of a unique result
- so let's go to articles/views.py:
```python
from django.db.models import Q
# this is for Query Lookup

def article_search_view(request):
    query = request.GET.get('q')
    # qs = Query Set
    qs = Article.objects.all()
    if query is not None:
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        qs = Article.objects.filter(lookups)

    context = {
        'obj_list': qs
    }
    return render(request, 'articles/search.html', context=context)
```
- and so the Templates/Articles/search.html:
```html
{% extends 'Base.html' %}


{% block title %}
<h1>Search</h1>
<form action=''>
    <input type='text' name='q' />
    <input type='submit' />
</form>
<ol>
{% for obj in obj_list %} 
    {% if obj.title %}
    <li><h4><a href="{{obj.get_absolute_url}}">{{obj.title}}</a></h4></li>
    {% endif %}
{% endfor %} 
</ol>
{% endblock %}
<!-- 
{% block content %}
{% if obj %}
<p>{{obj.content}}</p>
{% endif %}
<h3><a href='../'>Back to Home</a></h3>
{% endblock %} -->
```
- you can change Query lookups with "|", like this:
```python
first_lookup = Q(title__icontains='hi')
second_lookup = Q(title__icontains='hi') | Q(content__icontains='how')
# the second lookup aggregates both results A U B
# "|" is for "or", "&" is for "and"
```
- but the better way to have something like this:
```python
qs = Article.objects.search(query)
# bound to the model itself rather than the views
```
