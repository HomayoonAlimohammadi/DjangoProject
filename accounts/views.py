from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/admin')
    else:
        form = AuthenticationForm(request)
    context = {
        'form':form
    }
    return render(request, 'Accounts/Login.html', context=context)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/login/')  
    context = {}    
    return render(request, 'Accounts/Logout.html', context=context)

def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        return redirect('/login')
    context = {
        'form': form
    }
    return render(request, 'Accounts/Register.html', context=context)