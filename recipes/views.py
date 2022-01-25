from django.shortcuts import render, get_object_or_404, redirect
from recipes.models import Recipe
from django.contrib.auth.decorators import login_required
from recipes.forms import RecipeForm, RecipeIngredientsForm
# CURD -> Create Retrieve Update and Delete
# FVB -> CBV | function based view VS class based view
# CVB prevents redundant code
@login_required
def recipe_list_view(request):
    qs = Recipe.objects.filter(user=request.user)
    context = {
        'object_list':qs
    }
    return render(request, 'recipes/list.html', context=context)

@login_required
def recipe_detail_view(request, id=None):
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