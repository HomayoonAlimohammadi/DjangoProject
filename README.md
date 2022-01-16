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
