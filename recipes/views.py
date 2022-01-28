from django.shortcuts import render, get_object_or_404, redirect
from recipes.models import Recipe, RecipeIngredients
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory # ModelForm for querysets
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