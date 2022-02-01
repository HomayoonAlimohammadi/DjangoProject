"""TryDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from .views import HomeView

from accounts.views import (
    login_view,
    logout_view,
    register_view
)
from search.views import (
    search_view
)

urlpatterns = [
    path('', HomeView), #index / home/ root
    path('pantry/recipes/', include('recipes.urls')), # include('recipes.urls') is the path to app and it's urls.py
    # The orders are so important, but why and how?
    path('articles/', include('articles.urls')),
    path('search/', search_view, name='search'),
    path('admin/', admin.site.urls),
    path('login/', login_view),
    path('logout/', logout_view),
    path('register/', register_view)
]
