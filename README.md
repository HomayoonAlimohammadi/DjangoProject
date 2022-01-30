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
## Session 47:
- Model Managers and Custom QuerySets for Search
- we have to overwrite our Article.objects 
- so in order to do that, in the articles/models.py:
```python
from django.db.models import Q

class ArticleManager(models.Manager):
    def search(self, query):
        lookup = Q(title__icontains=query) | Q(content__icontains=query)
        return Article.objects.filter(lookup)
```
- and in the articles/views.py:
```python
def article_search_view(request):
    query = request.GET.get('q')
    # qs = Query Set
    qs = Article.objects.all()
    if query is not None:
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        # qs = Article.objects.filter(lookups)

        qs = Article.objects.search(query)

    context = {
        'obj_list': qs
    }
    return render(request, 'articles/search.html', context=context)
```
- or to make it useable across other models:
```python

class ArticleManager(models.Manager):
    def search(self, query):
        lookups = Q(title__icontains=query) | Q(content_icontains=query)
        return self.get_queryset().filter(lookups)
```
- and change models.py:
```python
class ArticleManager(models.Manager):
    def search(self, query=None):
        if query is None or query =='':
            return self.get_queryset().none()
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        return self.get_queryset().filter(lookups)
```
- and views.py:
```python
def article_search_view(request):
    query = request.GET.get('q')
    qs = Article.objects.search(query)

    context = {
        'obj_list': qs
    }
    return render(request, 'articles/search.html', context=context)
```
- and implement your own get_queryset() and another layer or filtering:
```python
class ArticleQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query =='':
            return self.none()
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        return self.filter(lookups)

class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)
```
now by doing this, writing a code like below will be possible:
```python
lookup = #something
qs = Article.objects.filter(title__icontains='hello').search(lookup)
# if we don't implement the code in the cell above we will get this error by the line above:
>>> 'QuerySet' object has no attribute 'search'
```
## Session 48:
- add a test article search manager
- add this to the articles/tests.py:
```python
class ArticleTestCase(TestCase):
    ...

    def test_article_search_manager(self):
            qs = Article.objects.search(query='hello world')
            self.assertEqual(qs.count(), self.number_of_articles)
            qs = Article.objects.search(query='hello')
            self.assertEqual(qs.count(), self.number_of_articles)
            qs = Article.objects.search(query='something random')
            self.assertEqual(qs.count(), self.number_of_articles)
```
## Session 49:
- associate a user with an article
- basic data connection with foreign keys
- so let's head to the articles/models.py:
```python
class Article(models.Model):
    # link a user to an article
    user = models.ForeignKey('auth.User', blank=True, null=True, on_delete=models.SET_NULL)
    ...
```
- and for some nice front end! let's head to templates/articles/details.html:
```html
{% block content %}
<p>{{obj.content}}</p>
<p>Author: {{ obj.user }}</p>
```
- but this is not a good way, so what to do?
- you can add this line to models.py:
```python
from django.conf import settings
User = settings.AUTH_USER_MODEL
class Article(models.Model):
    # link a user to an article
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    ...
```
- but interestingly, if you try to makemigrations, you will find out that no changes were made, in fact django by default sets the user as:
```python
migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0011_alter_article_slug')
```
- now you can do this to filter you objects based of of users:
```shell
python manage.py shell
from articles.models import Article
qs = Article.objects.filter(user__username='pazz')
qs 
>>> <ArticleQuerySet [<Article: Article object (XX)>]>
```
- it's just a way to do query with these user models.
## Session 50:
- let's head to our root, where manage.py is and make a new app called recipes (why?!):
```shell
ls
python manage.py startapp recipes
```

- Global
    - Ingredients
    - Recipes

- User
    - Ingredients
    - Recipes
        - Ingredients
        - Directions for Ingredients

- and in the recipes/models.py:
```python
from django.db import models
from django.conf import settings



class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    quantity = models.CharField(max_length=50) # 1 1/4, ... which are not int or float
    unit = models.CharField(max_length=50) # lbs, oz, gram, ...
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


# class RecipeImages():
#     recipe = models.ForeignKey(Recipe)
```
- and in our installed apps in TryDjango/settings.py add this app:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'articles',
    'recipes'
]
```
- now makemigrations and migrate
## Session 51:
- Admin inlines for foreign keys
- head to the recipes/admin.py:
```python
from django.contrib import admin
from recipes.models import Recipe, RecipeIngredients

admin.site.register(RecipeIngredients)

class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredients
    extra = 0 # how many RecipeIngredients you want to have right of the bat in any recipe
    fields = ['name', 'quantity', 'unit', 'directions'] # which features you want there to be shown

class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list__display = ['name', 'user'] # features to be shown in admin/Recipes
    readonly_fields = ['timestamp', 'updated'] # features that are readonly in each recipe page
    raw_id_fields = ['user'] # make this feature a raw id field, so getting rid of the enormous drop down menu

admin.site.register(Recipe, RecipeAdmin)
```
- let's change it to this:
```python
from django.contrib.auth import get_user_model
from django.contrib import admin
from recipes.models import Recipe, RecipeIngredients

admin.site.register(RecipeIngredients)

User = get_user_model()

class UserInline(admin.TabularInline):
    model = User

class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredients
    extra = 0 # how many RecipeIngredients you want to have right of the bat in any recipe
    fields = ['name', 'quantity', 'unit', 'directions'] # which features you want there to be shown

class RecipeAdmin(admin.ModelAdmin):
    inlines = [UserInline, RecipeIngredientInline]
    list__display = ['name', 'user'] # features to be shown in admin/Recipes
    readonly_fields = ['timestamp', 'updated'] # features that are readonly in each recipe page
    raw_id_fields = ['user'] # make this feature a raw id field, so getting rid of the enormous drop down menu

admin.site.register(Recipe, RecipeAdmin)
```
- it gives an error, 'auth.User' has no ForeignKey to 'recipes.Recipe'
- it's because the hierarchy of these foreignkeys
- instead of tabular inline for the user, we have to tabularinline for the recipe (?!?!?!)
```python
from django.contrib.auth import get_user_model
from django.contrib import admin
from recipes.models import Recipe, RecipeIngredients

admin.site.register(RecipeIngredients)

User = get_user_model()

class RecipeInline(admin.StackedInline):
    model = Recipe
    extra = 0

class UserAdmin(admin.ModelAdmin):
    list_display = ['username']
    inlines = [RecipeInline]

admin.site.register(User, UserAdmin)

class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredients
    extra = 0 # how many RecipeIngredients you want to have right of the bat in any recipe
    fields = ['name', 'quantity', 'unit', 'directions'] # which features you want there to be shown

class RecipeAdmin(admin.ModelAdmin):
    inlines = [UserInline, RecipeIngredientInline]
    list__display = ['name', 'user'] # features to be shown in admin/Recipes
    readonly_fields = ['timestamp', 'updated'] # features that are readonly in each recipe page
    raw_id_fields = ['user'] # make this feature a raw id field, so getting rid of the enormous drop down menu

admin.site.register(Recipe, RecipeAdmin)
```
- now it gives an error: the model User is already registered with 'auth.UserAdmin'
- we have to do this:
```python
from django.contrib.auth import get_user_model
from django.contrib import admin
from recipes.models import Recipe, RecipeIngredients

admin.site.register(RecipeIngredients)
User = get_user_model()
admin.site.unregister(User)

class RecipeInline(admin.StackedInline):
    model = Recipe 
    extra = 0
 
class UserAdmin(admin.ModelAdmin):
    list_display = ['username']
    inlines = [RecipeInline]

admin.site.register(User, UserAdmin)

class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredients
    extra = 0 # how many RecipeIngredients you want to have right of the bat in any recipe
    fields = ['name', 'quantity', 'unit', 'directions'] # which features you want there to be shown

class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list__display = ['name', 'user'] # features to be shown in admin/Recipes
    readonly_fields = ['timestamp', 'updated'] # features that are readonly in each recipe page
    raw_id_fields = ['user'] # make this feature a raw id field, so getting rid of the enormous drop down menu

admin.site.register(Recipe, RecipeAdmin)
```
- ok so this session was somehow crazy, let's master it with practice later.
## Session 52:
- understanding relationships between models via tests
- in models.py we referrence user model like this:
```python
from django.conf import settings
user = settings.AUTH_USER_MODEL
```
- everywhere else if we need to use User model do this:
```python
from django.contrib.auth import get_user_model
User = get_user_model()
```
- in the tests.py add this:
```python
from webbrowser import get
from django.test import TestCase
from django.contrib.auth import get_user_model
from recipes.models import Recipe

User = get_user_model()

class UserTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user('pazzo', password='1991')
        
    def test_user_pw(self):
        checked = self.user_a.check_password("1991")
        self.assertTrue(checked)


class RecipeTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user('pazzo', password='1991')
        self.recipe_a = Recipe.objects.create(
            name = 'Grilled Chicken',
            user = self.user_a
        )

    def test_user_count(self):
        qs = User.objects.all()
        self.assertEqual(qs.count(), 1)
    
    def test_user_recipe_reverse_count(self):
        user = self.user_a
        # user.<model_name>_set (giving the query set for that model)
        qs = user.recipe_set.all()
        self.assertEqual(qs.count(), 1)
```
- notice that here user creation in separate classes doesn't add up.
- let's add recipe_forward_count:
```python
class RecipeTestCase(TestCase):
    ...
    def test_user_recipe_forward_count(self):
            user = self.user_a
            qs = Recipe.objects.filter(user=user)
            self.assertEqual(qs.count(), 1)
```
- and let's do recipeingredient counts + some two level relations:
```python
class RecipeTestCase(TestCase):
    ...
    
    def test_user_recipe_ingredient_reverse_count(self):
        recipe = self.recipe_a
        qs = recipe.recipeingredients_set.all()
        self.assertEqual(qs.count(), 1)

    def test_user_recipe_ingredient_forward_count(self):
        recipe = self.recipe_a
        qs = RecipeIngredients.objects.filter(recipe=recipe)
        self.assertEqual(qs.count(), 1)

    def test_user_two_level_relation(self):
        user = self.user_a
        recipe = self.recipe_a
        # recipe__user is a two level relation 
        # why can't you write user__recipe=recipe? maybe because the hierarchy?
        qs = RecipeIngredients.objects.filter(recipe__user=user)
        self.assertEqual(qs.count(), 1)

    def test_user_two_level_reverse_relation(self):
        user = self.user_a
        recipeingredient_ids = user.recipe_set.all().values_list('recipeingredients', flat=True)
        # qs = RecipeIngredients.objects.filter(recipe__user=user)
        self.assertEqual(recipeingredient_ids.count(), 1)

    def test_user_two_level_relation_via_recipes(self):
        user = self.user_a
        ids = user.recipe_set.all().values_list('id', flat=True)
        qs = RecipeIngredients.objects.filter(recipe__id__in=ids)
        self.assertEqual(qs.count(), 1)
```
## Session 53:
- custom validation for unit measurements
- let's create a new python file in recipes/validators.py:
```python
from django.core.exceptions import ValidationError

# instead of this custom list, use Pint
valid_unit_measurements = ['pounds', 'lbs', 'oz', 'gram']

def validate_unit_of_measure(value):
    if value not in valid_unit_measurements:
        raise ValidationError(f'{value} is not a valid unit of measure!')
```
- let's install "pint" and then do these:
```python
from django.core.exceptions import ValidationError
import pint
from pint.errors import UndefinedUnitError

# instead of this custom list, use Pint
valid_unit_measurements = ['pounds', 'lbs', 'oz', 'gram']

def validate_unit_of_measure(value):
    ureg = pint.UnitRegistry()
    try:
        single_unit = ureg[value]
    except UndefinedUnitError as e:
        raise ValidationError(f'{e}')
    except:
        raise ValidationError(f'{value} is not a valid unit of measure')
```
## Session 54:
- test custom model validation exception
- head to recipes/tests.py:
```python
class RecipeTestCase(TestCase):
    ...

    def test_unit_measure_validation_error(self):
        invalid_unit = 'something random'
        with self.assertRaises(ValidationError):
            ingredient = RecipeIngredients(
                name = 'New',
                quantity = 10,
                recipe = self.recipe_a,
                unit = invalid_unit
            )
            ingredient.full_clean()
            # simillar to form.is_valid()
    
    def test_unit_measure_validation(self):
        invalid_unit = 'grams'
        ingredient = RecipeIngredients(
            name = 'New',
            quantity = 10,
            recipe = self.recipe_a,
            unit = invalid_unit
        )
        ingredient.full_clean()
        # simillar to form.is_valid()
```
- in the future we can add a field for automated units. an API service or parser that somebody can put down a unit, and that parser or API creates that unit for us.
## Session 55:
- we want a field which auto set quantity as a float
- so head to the recipes/models.py:
```python
class RecipeIngredients(models.Model):
    ...
    quantity_as_float = models.FloatField(blank=True, null=True)
```
- now make a new utils.py file in recipes/:
```python
from fractions import Fraction

def number_str_to_float(amount_str):
    success = False
    number_as_float = amount_str
    try:
        number_as_float = float(sum(Fraction(s) for s in f'{amount_str}'.split()))
    except:
        pass
    if isinstance(number_as_float, float):
        success = True
    return number_as_float, success

```
- now we want to make it auto set from self.quantity
- it's nice to overwrite the save() method when a field is automatically being generated from another field
- again in the recipes/models.py:
```python
class RecipeIngredients(models.Model):
    ...

    # it's good to overwrite save method when it's automatically generating a field from another field
    # like slugs from title and quantity as float from quantity
    def save(self, *args, **kwargs):
        qty = self.quantity
        qty_as_float, qty_as_float_success = number_str_to_float(qty)
        if qty_as_float_success:
            self.quantity_as_float = qty_as_float
        else:
            self.quantity_as_float = None
        super().save(*args, **kwargs)
```
- don't forget to makemigrations and migrate
- now let's make it readonly so no one can change it
- when you write a new feature to a model specially, you want to test it
- head to recipes/tests.py:
```python
class RecipeTestCase(TestCase):
    ...
    def test_quantity_as_float(self):
        self.assertIsNotNone(self.recipe_ingredient_a.quantity_as_float)
        self.assertIsNone(self.recipe_ingredient_b.quantity_as_float)
```
- if you do this:
```shell
from recipes.models import *
RecipeIngredients.objects.create(recipe=r, name='Hello There', quantity='21', unit='abc')
```
- this will create a recipe ingredient even tho the unit is invalid. why??!
## Session 56:
- use python Pint package to convert units
- let's head to the recipes/models.py:
```python
import pint

class RecipeIngredient(models.Model):
    ...

    def convert_to_system(self, system='mks'):   
        if self.quantity_as_float is None:
            return '' 
        ureg = pint.UnitRegistry(system=system)
        measurement = self.quantity_as_float * ureg[self.unit]
        print(measurement)
        return measurement # .to_base_units()


    def as_mks(self):
        # meter, kilogram, second
        measurement = self.convert_to_system(system='mks')
        print(measurement)
        return measurement.to_base_units()

    def as_imperial(self):
        # miles, pounds, seconds
        measurement = self.convert_to_system(system='imperial')
        print(measurement)
        return measurement.to_base_units()
```
- and now head to the recipes/admin.py:
```python
class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredients
    extra = 0 # how many RecipeIngredients you want to have right of the bat in any recipe
    # you can use those instance methods as elements in this list too!
    readonly_fields = ['quantity_as_float','as_mks', 'as_imperial']
    # fields = ['name', 'quantity', 'unit', 'directions', 'quantity_as_float'] # which features you want there to be shown
```
- nice thing about this is the fact that i think, you don't have to do migrations
## Session 57:
- CRUD views for recipe model
- CURD -> Create Retrieve Update and Delete
- let's head to the recipes/views.py:
```python
from django.shortcuts import render, get_object_or_404, redirect
from recipes.models import Recipe
from django.contrib.auth.decorators import login_required
from recipes.forms import RecipeForm
# CURD -> Create Retrieve Update and Delete

@login_required
def recipe_list_view(request):
    qs = Recipe.objects.filter(user=request.user)
    context = {
        'object_list':qs
    }
    return render(request, 'recipes/list.html', context=context)

@login_required
def recipe_detial_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    context = {
        'obj':obj
    }
    return render(request, 'recipes/detail.html', context=context)




@login_required
def recipe_create_view(request):
    form = RecipeForm(request.POST or None)
    context = {
        'form':form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect(obj.get_absolute_url())

    return render(request, 'recipes/create-update.html', context=context)

@login_required
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    context = {
        'form':form,
        'obj':obj
    }
    if form.is_valid():
        form.save()
        context['message'] = 'Data Saved'
    return render(request, 'recipes/create-update.html', context=context)
```
- now to make RecipeForm, create a file in the path recipes/forms.py:
```python
from django import forms
from recipes.models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'directions']
```
- and in order for the .get_absolute_url() to work, let's do this in recipes/models.py:
```python
class Recipe(models.Model):
    ...
    def get_absolute_url(self):
    return '/pantry/recipes/'

class RecipeIngredients(models.Model):
    ...
    def get_absolute_url(self):
    return self.recipe.get_absolute_url()
```
- in the next part we are going to implement the .html files too!
## Session 58:
- <b>Warning! this session is a hard one! pay extra attention!</b>
- let's implement the urls for these apps
- this time we want to add them <b>inside the recipe folder</b> (what is the difference?), so create it:
```python
from django.urls import path
from recipes.views import (
    recipe_list_view,
    recipe_detail_view,
    recipe_create_view,
    recipe_update_view
)

# order matters, they are gonna match the order they come in. order should make sense.
app_name = 'recipes' # we can recipes:list as a reverse call or recipes:create
urlpatterns = [
    path('', recipe_list_view, name='list'),
    path('create/', recipe_create_view, name='create'),
    path('<int:id>/edit/', recipe_update_view, name='update'),
    path('<int:id>/', recipe_detail_view, name='detail')
]
```
- let's head to recipes/models.py:
```python
def get_absolute_url(self):
    return rever('recipes:detail', kwargs={'id':self.id})
```
- now head to main configuration urls.py:
```python
from django.contrib import admin
from django.urls import path, include
from .views import HomeView
from accounts.views import (
    login_view,
    logout_view,
    register_view
)

urlpatterns = [
    path('', HomeView), #index / home/ root
    path('pantry/recipes/', include('recipes.urls')), # include('recipes.urls') is the path to app and it's urls.py
    # The orders are so important, but why and how?
    path('articles/', include('articles.urls')),
    path('admin/', admin.site.urls),
    path('login/', login_view),
    path('logout/', logout_view),
    path('register/', register_view)
]
```
- now create the articles/urls.py just to make it same as recipes model:
```python
from django.urls import path
from articles.views import (
    article_search_view,
    article_create_view,
    article_detail_view
)

app_name = 'articles' # just like recipes, articles:search
urlpatterns = [
    path('', article_search_view, name='search'),
    path('create/', article_create_view, name='create'),
    path('<slug:slug>/', article_detail_view, name='detail'),
]
```
- to fix the template NoReverseMatch error, head to HomeView.html:
```html
<h3><a href='{% url "articles:create" %}'>Create Article</a></h3>
```
- and in the articles/models.py:
```python
    def get_absolute_url(self):
        # return f'/articles/{self.slug}/'
        return reverse('articles:detail', kwargs={'slug':self.slug})
```
## Session 59:
- CRUD templates for the Reicpes app
- a new approach to adding templates
- you can do both this approach and our old approach of adding recipes folder in the Template folder
- create a new forlder in the recipes folder called templates
- inside of it create a folder called recipes, and then there, list.html:
```html
<b>Blank on purpose, look for main templates dir.</b>
```
- what you can do, is to overwrite this .html file in the main directory folder
- if you make templates in the new way, apps are more self contained and easier to use later, yet more complex. 
- so to keep everything simple, all we do is to just overwrite it by creating:
- Templates/Recipes/list.html:
```html
<b>New overwrited html!</b>
```
- so in the main configuration, create other templates too. (create-update, detail)
- now set them up like this, list.html:
```html
{% extends 'Base.html' %}

{% block title %}
<h1>My Recipes</h1>
<h3><a href='{% url "recipes:create" %}'>Add Recipe</a></h3>
{% endblock title %}

{% block content %} 
<h3>{{content}}</h3>
<p>{% for x in object_list %}
<li><a href='{{ x.get_absolute_url }}'>{{ x.name }}</a></li>
{% endfor %}
</p>



{% endblock content %}
```
- create-update.html:
```html
{% extends 'Base.html' %}

{% block title %}
<h1>{{obj.name}}</h1>
{% endblock %}

{% block content %}
{% if message %}
<h2>{{message}}</h2>
{% endif %} 
<form method='POST'>
    {% csrf_token %}
    {{ form.as_p }}
    <button type='Submit'>Save</button>
</form>
<h3><a href='../../'>Back to Home</a></h3>
{% endblock %}
```
- detail.html:
```html
{% extends 'Base.html' %}

{% block title %}
<h1>{{obj.name}}</h1>
<h3><a href= '{{ obj.get_edit_url }}'>Edit</a></h3>

{% endblock %}

{% block content %}
<p>{{obj.description}}</p>
<p>{{ obj.directoins }}</p>
{% for ingredient in obj.get_ingredients_children %}
<p>{{ingredient.name}}</p>
<p>{{ingredient.as_imperial}}</p>
<p>{{ingredient.as_mks}}</p>
{% endfor %}
<h3><a href='../'>Recipe List</a></h3>
<h3><a href='../../../../'>Back to Home</a></h3>
{% endblock %}
```
- and in the HomeView.html add a link to recipes list:
```html
<h2><a href='pantry/recipes/'>Go to Recipe List</a></h2>
```
- in the recipes/models.py add this:
```python

    def get_edit_url(self):
        return reverse('recipes:update', kwargs={'id':self.id})

    def get_ingredients_children(self):
        return self.recipeingredients_set.all()
```
- <b>FVB -> CBV | function based view VS class based view
- CVB prevents redundant code</b>
- in the recipes/views.py pay attention to:
```python
@login_required
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    # instead of 'instance=obj' you could use initial={'name':'something ,...} but it
    # would overwrite everything including self.user which is not good.
    # don't mistake initial with instance
    context = {
        'form':form,
        'obj':obj
    }
    if form.is_valid():
        form.save()
        context['message'] = 'Data Saved'
    return render(request, 'recipes/create-update.html', context=context)
```
- in the next parts we tend to add recipe ingredients too
## Session 60:
- 2 forms 1 view
- head to the recipes/forms.py:
```python
from django import forms
from recipes.models import Recipe, RecipeIngredients

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'directions']

    
class RecipeIngredientsForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredients
        fields = ['name', 'quantity', 'unit']
```
- and in the recipes/views.py:
```python
from recipes.forms import RecipeForm, RecipeIngredientsForm

@login_required
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    # instead of 'instance=obj' you could use initial={'name':'something ,...} but it
    # would overwrite everything including self.user which is not good.
    # don't mistake initial with instance

    form_2 = RecipeIngredientsForm(request.POST or None)

    context = {
        'form':form,
        'form_2':form_2,
        'obj':obj
    }
    if all([form.is_valid(), form_2.is_valid()]):
        parent = form.save(commit=False)
        parent.save()
        child = form_2.save(commit=False)
        child.recipe = parent
        child.save()
        context['message'] = 'Data Saved'
    return render(request, 'recipes/create-update.html', context=context)
```
- and update the create-update.html file as below:
```html
{% block content %}
{% if message %}
<h2>{{message}}</h2>
{% endif %} 
<form method='POST'>
    {% csrf_token %}
    {{ form.as_p }}
    {% if form_2 %}
    <h3>Ingredients</h3>
    {{ form_2.as_p}}
    {% endif %}
    <button type='Submit'>Save</button>
</form>
<h3><a href='../../'>Back to Home</a></h3>
{% endblock %}
```
- but this is not working, why?
- the child parent relation is not right it seems like. because it overwrites the child name for the parents. it has something to do with instance in form defining part. we will fix it in the next part.
## Session 61:
- essentially we want to be able to properly edit all the childs of the parent
- or in other words edit all ingredients for a given recipe
- you would say that we can do this in the recipes/views.py:
```python
@login_required
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    form_2 = RecipeIngredientsForm(request.POST or None)
    # obj = recipeingredient_set.all()
    ingredient_forms = []
    for ingredient_obj in obj.recipeingreidient_set.all():
        RecipieIngredientForm(request.POST or None, instance=ingredient_obj)
    context = {
        'form':form,
        'ingredient_forms':ingredient_forms,
        'obj':obj
    }
    my_forms = all([form.is_valid() for form in ingredient_forms])
    if form.is_valid and my_forms:
        parent = form.save(commit=False)
        parent.save()
        for form_2 in ingredient_forms:
            child = form_2.save(commit=False)
            child.recipe = parent
            child.save()
        context['message'] = 'Data Saved'
    return render(request, 'recipes/create-update.html', context=context)
```
- is this the best way to do this? NO!
- one main problem of this, is we can't handle dynamicly adding new items to the recipeingredient list (+ Add Ingredient)
- the much better practice is to use: modelformset_factory
- so head to the recipes/views.py:
```python
@login_required
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    # Formset = modelformset_factory(Model, form=ModelForm, extra=0)
    RecipeIngredientsFormset = modelformset_factory(RecipeIngredients, form=RecipeIngredientsForm, extra=0)
    qs = obj.recipeingredients_set.all()
    formset = RecipeIngredientsFormset(request.POST or None, queryset=qs)
    context = {
        'form':form,
        'formset':formset,
        'obj':obj
    }
    if all([form.is_valid(), formset.is_valid()]):
        parent = form.save(commit=False)
        parent.save()
        # formset.save() when you don't 
        for form in formset:
            child = form.save(commit=False)
            if child.recipe is None:
                child.recipe = parent
            child.save()
        context['message'] = 'Data Saved'
    return render(request, 'recipes/create-update.html', context=context)
```
- and minor edits in create-update.html and detail.html
- in the next part we learn how to add additional forms (ingredients maybe?)
## Session 62:
- customizing django formfields, adding some widgets, placeholders and...
- it's a referrence related part. because there is soo sooo much to django forms.
- head to the recipes/forms.py:
```python
from django import forms
from recipes.models import Recipe, RecipeIngredients

class RecipeForm(forms.ModelForm):
    required_css_class = 'required-field' # css classes have '-' between then not '_'
    error_css_class = 'error-field'
    
    # choose the 'name' as variable cause u are handling input area called 'name'
    ''
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Recipe Name'}))
    ''
    # you will forget the line above, make sure to check django documentations 
    # choose 'description' for the same reason. 
    # choose the name you want
    ''
    description = forms.CharField(widget=forms.Textarea({'rows':'3'}))
    ''
    # interestingly, if you make a variable with a name outside your form elements
    # a new form will be created with the properties you gave it

    
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'directions']

    
class RecipeIngredientsForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredients
        fields = ['name', 'quantity', 'unit']
```
- and let's see yet another method for changing the property of your form:
```python
class RecipeForm(forms.ModelForm):
    required_css_class = 'required-field' # css classes have '-' between then not '_'
    error_css_class = 'error-field'
    
    # choose the 'name' as variable cause u are handling input area called 'name'
    ''
    # name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Recipe Name'}))
    ''
    # you will forget the line above, make sure to check django documentations 
    # choose 'description' for the same reason. 
    # choose the name you want
    ''
    # description = forms.CharField(widget=forms.Textarea({'rows':'3'}))
    ''
    # interestingly, if you make a variable with a name outside your form elements
    # a new form will be created with the properties you gave it

    # yet another method to change those things:
    # we can use both, but the lines below will overwrite others
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
            'placeholder':f'Recipe {str(field)}',
            'class':'form-control'
        }
            self.fields[str(field)].widget.attrs.update(new_data) # you can pass **new_data too, in order to unpack it
        self.fields['name'].label= 'Naaaaaame!!!!'
        self.fields['name'].widget.attrs.update({'class':'form-control-2'})
        self.fields['description'].widget.attrs.update({'rows':'2'})
```
- django crispy forms is a third party package to make these forms look prettier
## Session 63:
- rendering form fields individually and more
- so let's head to the templates/recipes/create-update.html:
```html
<form method='POST'>
    {% csrf_token %}
    {% for field in form %} 
    <div class='{% if field.field.required %}{{ form.required_css_class }}{% endif %}'>
        {{ field.label_tag }} {{ field }} 
    </div>
    {% endfor %}
    {% if formset %}
    <h3>Ingredients</h3>
    {{ formset.as_p}}
    {% endif %}
    <button type='Submit'>Save</button>
</form>
```
- just for fun, another thing you can do is to:
```html
<form method='POST'>
    {% csrf_token %}
    {% for field in form %} 
    <div class='{% if field.field.required %}{{ form.required_css_class }}{% endif %}'>
        {{ field.label_tag }} {{ field }}
    {% if field.help_text %} 
    {{ field.help_text|safe }}
    <!-- this is called template filter or template tag, you can allow for links with this -->
    {% endif %} 
    </div>
    {% endfor %}
    {% if formset %}
    <h3>Ingredients</h3>
    {{ formset.as_p}}
    {% endif %}
    <button type='Submit'>Save</button>
</form>
```
- let's do this with formset:
```html
{% extends 'Base.html' %}

{% block title %}
<h1>{{obj.name}}</h1>
{% endblock %}

{% block content %}

<style>
    .ingredient-form {
        border-bottom: 1px solid black;
    }
</style>
{% if message %}
<h2>{{message}}</h2>
{% endif %} 
<form method='POST'>
    {% csrf_token %}
    {% for field in form %} 
    <div class='{% if field.field.required %}{{ form.required_css_class }}{% endif %}'>
        {{ field.label_tag }} {{ field }}
    {% if field.help_text %} 
    {{ field.help_text|safe }}
    {% endif %} 
    </div>
    {% endfor %}
    {% if formset %}
    <h3>Ingredients</h3>
    {{ formset.management_form }}
    <!-- this is necessary in order not to hide the forms after edditing -->
    {% for form in formset %} 
    <div class='ingredient-form'>
        {{ form.as_p}}
    </div>
    {% endfor %}
    {% endif %}
    <button type='Submit'>Save</button>
</form>
<h3><a href='../'>Back</a></h3>
{% endblock %}
```
- we prefer <b>Django crispy forms</b>
## Session 64:
- how to dynamicly add new elements in the django formset via javascript
- head to the templates/recipes/create-update.html:
```html
{% extends 'Base.html' %}

{% block title %}
<h1>{{obj.name}}</h1>
{% endblock %}

{% block content %}

<style>
    .ingredient-form {
        border-bottom: 1px solid black;
    }
    .hidden {
        display: none
    }
</style>
{% if message %}
<h2>{{message}}</h2>
{% endif %} 
<form method='POST'>
    {% csrf_token %}
    {% for field in form %} 
    <div class='{% if field.field.required %}{{ form.required_css_class }}{% endif %}'>
        {{ field.label_tag }} {{ field }}
    {% if field.help_text %} 
    {{ field.help_text|safe }}
    {% endif %} 
    </div>
    {% endfor %}
    {% if formset %}
    <h3>Ingredients</h3>
    {{ formset.management_form }}
    <div id='ingredient-form-list'>
        {% for form in formset %} 
        <div class='ingredient-form'>
            {{ form.as_p}}
        </div>
        {% endfor %}
    </div>
    <div id='empty-form' class='hidden'>{{ formset.empty_form.as_p }}</div>
    <button id='add-more' type='button'>Add More</button>
    {% endif %}
    <button style='margin-top:10px;' type='Submit'>Save</button>
</form>
<h3><a href='../'>Back</a></h3>

<script>
    const addMoreBtn = document.getElementById('add-more')
    addMoreBtn.addEventListener('click', add_new_form)

    function add_new_form(event) {
        if (event) {
            event.preventDefault() // we will no longer see a console log
        }
        const formCopyTarget = document.getElementById('ingredient-form-list')
        // now add new empty form element to our html form
        const emptyFormEl = document.getElementById('empty-form').cloneNode(true)
        // reset the form class
        emptyFormEl.setAttribute('class', 'ingredient-form')
        // in order for it not to duplicate data
        emptyFormEl.setAttribute('id', '')

        formCopyTarget.append(emptyFormEl)
    } 


</script>

{% endblock %}
```
- and yet we see that it's not working, so we have to alter the formset management section:
```html
{% extends 'Base.html' %}

{% block title %}
<h1>{{obj.name}}</h1>
{% endblock %}

{% block content %}

<style>
    .ingredient-form {
        border-bottom: 1px solid black;
    }
    .hidden {
        display: none
    }
</style>
{% if message %}
<h2>{{message}}</h2>
{% endif %} 
<form method='POST'>
    {% csrf_token %}
    {% for field in form %} 
    <div class='{% if field.field.required %}{{ form.required_css_class }}{% endif %}'>
        {{ field.label_tag }} {{ field }}
    {% if field.help_text %} 
    {{ field.help_text|safe }}
    {% endif %} 
    </div>
    {% endfor %}
    {% if formset %}
    <h3>Ingredients</h3>
    {{ formset.management_form }}
    <div id='ingredient-form-list'>
        {% for form in formset %} 
        <div class='ingredient-form'>
            {{ form.as_p}}
        </div>
        {% endfor %}
    </div>
    <div id='empty-form' class='hidden'>{{ formset.empty_form.as_p }}</div>
    <button id='add-more' type='button'>Add More</button>
    {% endif %}
    <button style='margin-top:10px;' type='Submit'>Save</button>
</form>
<h3><a href='../'>Back</a></h3>

<script>
    const addMoreBtn = document.getElementById('add-more')
    const totalNewForms = document.getElementById('id_form-TOTAL_FORMS')

    addMoreBtn.addEventListener('click', add_new_form)

    function add_new_form(event) {
        if (event) {
            event.preventDefault() // we will no longer see a console log
        }
        const currentIngredientForms = document.getElementsByClassName('ingredient-form')
        const currentFormCount = currentIngredientForms.length
        const formCopyTarget = document.getElementById('ingredient-form-list')
        // now add new empty form element to our html form
        const copyEmptyFormEl = document.getElementById('empty-form').cloneNode(true)
        // reset the form class
        copyEmptyFormEl.setAttribute('class', 'ingredient-form')
        // in order for it not to duplicate data
        copyEmptyFormEl.setAttribute('id', `form-${currentFormCount}`)
        const regex = new RegExp('__prefix__', 'g')
        copyEmptyFormEl.innerHTML = copyEmptyFormEl.innerHTML.replace(regex, currentFormCount)
        totalNewForms.setAttribute('value', currentFormCount + 1)
        formCopyTarget.append(copyEmptyFormEl)
    } 


</script>

{% endblock %}
```
## Session 65:
- making dynamic forms in django formset via HTMX
- so let's head to the htmx official website: https://htmx.org/
- copy and paste this line in templates/Base.html:
```html
    <head>
        <script src="https://unpkg.com/htmx.org@1.6.1"></script>
        {% block title %}
        {% endblock title %}
    </head>
```
- now install django-htmx and add it to the requirements.txt:
```shell
pip install django-htmx
pip freeze > requirements.txt
```
- now let's head to the settings.py and add this package to our installed apps:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_htmx', # this was added
    'articles',
    'recipes'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware', # this was added
]
```
- and in the create-update.html:
```html
<form action='.' method='POST' hx-post='.' hx-swap='outerHTML'>
```
- now your page will be dynamicly change each time you hit save and won't refresh all over again.
## Session 66:
- htmx javascript django fixtures
- let's make a tepmlates/recipes/partials/detail.html:
```html
<p>{{obj.description}}</p>
<p>{{ obj.directoins }}</p>
{% for ingredient in obj.get_ingredients_children %}
<br>
<h3>{{ingredient.name}}</h3>
<p>{{ingredient.as_imperial}}</p>
<p>{{ingredient.as_mks}}</p>
{% endfor %}
<h3><a href='../'>Recipe List</a></h3>
<h3><a href='../../../../'>Back to Home</a></h3>
```
- and make the recipes/detail.html:
```html
{% extends 'Base.html' %}

{% block title %}
<h1>{{obj.name}}</h1>
<h3><a href= '{{ obj.get_edit_url }}'>Edit</a></h3>

{% endblock %}

{% block content %}
<div hx-get='{{ obj.get_hx_url }}' hx-trigger='revealed'>
    <!--This is a defulat class: 'htmx indicator'-->
    <div class='htmx-indicator'>Loading...</div>
</div>
{% endblock %}
```
- now head to the recipes/views.py:
```python
from django.http import HttpResponse 


@login_required
def recipe_detail_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    context = {
        'obj':obj
    }
    return render(request, 'recipes/detail.html', context=context)

@login_required
def recipe_detail_hx_view(request, id=None):
    try:
        obj = Recipe.objects.get(id=id, user=request.user)
    except:
        obj = None
    if obj is None:
        return HttpResponse('Not found.')    
    context = {
        'obj':obj
    }
    return render(request, 'recipes/partials/detail.html', context=context)
```
- and in the recipes/urls.py:
```python
from django.urls import path
from recipes.views import (
    recipe_list_view,
    recipe_detail_view,
    recipe_create_view,
    recipe_update_view,
    recipe_detail_hx_view
)

# order matters, they are gonna match the order they come in. order should make sense.
app_name = 'recipes' # recipes:list as a reverse call or recipes:create
urlpatterns = [
    path('', recipe_list_view, name='list'),
    path('create/', recipe_create_view, name='create'),
    path('hx/<int:id>/', recipe_detail_hx_view, name='hx-detail'),
    path('<int:id>/edit/', recipe_update_view, name='update'),
    path('<int:id>/', recipe_detail_view, name='detail')
]
```
- and in the recipes/models.py:
```python
class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('recipes:detail', kwargs={'id':self.id})
    
    
    def get_hx_url(self):
        return reverse('recipes:hx-detail', kwargs={'id':self.id})

    def get_edit_url(self):
        return reverse('recipes:update', kwargs={'id':self.id})

    def get_ingredients_children(self):
        return self.recipeingredients_set.all()
```
## Session 67:
- HTMX JavaScript Working Together with Python
- head to the create-update.html:
```html
{% extends 'Base.html' %}

{% block title %}
{% endblock %}

{% block content %}

<style>
    .ingredient-form {
        border-bottom: 1px solid black;
    }
    .hidden {
        display: none
    }
</style>

<form action='.' method='POST' hx-post='.' hx-swap='outerHTML'>
 
    <h1>{{obj.name}}</h1>

    {% csrf_token %}
    {% for field in form %} 
    <div class='{% if field.field.required %}{{ form.required_css_class }}{% endif %}'>
        {{ field.label_tag }} {{ field }}
    {% if field.help_text %} 
    {{ field.help_text|safe }}
    {% endif %} 
    </div>
    {% endfor %}
    {% if formset %}
    <h3>Ingredients</h3>
    {{ formset.management_form }}
    <div id='ingredient-form-list'>
        {% for form in formset %} 
        <div class='ingredient-form'>
            {{ form.as_p}}
        </div>
        {% endfor %}
    </div>
    <div id='empty-form' class='hidden'>{{ formset.empty_form.as_p }}</div>
    <button id='add-more' type='button'>Add More</button>
    {% endif %}
    <div class='htmx-indicator'>Loading...</div>
    <button class='htmx-inverted-indicator' style='margin-top:10px;' type='Submit'>Save</button>
    {% if message %}
    <h2 style='color:red;'>Data Saved!</h2>
    {% endif %} 
    <h3><a href='../'>Back</a></h3>

</form>

<script>
    document.addEventListener('click', (event)=>{
        if (event.target.id == 'add-more') {
            add_new_form(event)
        }
    })

    function add_new_form(event) {
        if (event) {
            event.preventDefault() // we will no longer see a console log
        }
        const totalNewForms = document.getElementById('id_form-TOTAL_FORMS')
        const currentIngredientForms = document.getElementsByClassName('ingredient-form')
        const currentFormCount = currentIngredientForms.length
        const formCopyTarget = document.getElementById('ingredient-form-list')
        // now add new empty form element to our html form
        const copyEmptyFormEl = document.getElementById('empty-form').cloneNode(true)
        // reset the form class
        copyEmptyFormEl.setAttribute('class', 'ingredient-form')
        // in order for it not to duplicate data
        copyEmptyFormEl.setAttribute('id', `form-${currentFormCount}`)
        const regex = new RegExp('__prefix__', 'g')
        copyEmptyFormEl.innerHTML = copyEmptyFormEl.innerHTML.replace(regex, currentFormCount)
        totalNewForms.setAttribute('value', currentFormCount + 1)
        formCopyTarget.append(copyEmptyFormEl)
    } 


</script>

{% endblock %}
```
- and some changes in views.py: and Base.html:
```html
<!DOCTYPE html>
<html>
    <head>
        <script src="https://unpkg.com/htmx.org@1.6.1"></script>
        <style>
            .htmx-indicator {
                display: none;
            }
            .htmx-request .htmx-indicator {
                display: inline;
            }
            .htmx-inverted-indicator {
                display: inline;
            }
            .htmx-request .htmx-inverted-indicator {
                display: none;
            }
        </style>
        {% block title %}
        {% endblock title %}
    </head>
    <body>
        {% block content %}
        {% endblock content %}
    </body>
</html>
```
```python
@login_required
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    # Formset = modelformset_factory(Model, form=ModelForm, extra=0)
    RecipeIngredientsFormset = modelformset_factory(RecipeIngredients, form=RecipeIngredientsForm, extra=0)
    qs = obj.recipeingredients_set.all()
    formset = RecipeIngredientsFormset(request.POST or None, queryset=qs)
    context = {
        'form':form,
        'formset':formset,
        'obj':obj
    }
    if all([form.is_valid(), formset.is_valid()]):
        parent = form.save(commit=False)
        parent.save()
        # formset.save() when you don't 
        for form in formset:
            child = form.save(commit=False)
            child.recipe = parent
            child.save()
        context['message'] = True
    return render(request, 'recipes/create-update.html', context=context)
```
