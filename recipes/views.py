from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from recipes.models import Recipe, RecipeIngredients
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory # ModelForm for querysets
from recipes.forms import RecipeForm, RecipeIngredientsForm, RecipeIngredientsImageForm
from django.http import HttpResponse 
from django.http import Http404
from recipes.services import extract_text_via_ocr_service

# CRUD -> Create Retrieve Update and Delete
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
def recipe_delete_view(request, id=None):
    try:
        obj = Recipe.objects.get(id=id, user=request.user)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse('Not Found')
        raise Http404
    if request.method == 'POST': 
        obj.delete()
        success_url = reverse('recipes:list')
        if request.htmx:
            headers = {
                'HX-Redirect' : success_url
            }
            return HttpResponse('Success', headers=headers)
        return redirect(success_url)
    context = {
        'obj':obj
    }
    return render(request, 'recipes/delete.html', context=context)

    

@login_required
def recipe_ingredient_delete_view(request, parent_id=None, id=None):
    try:
        obj = RecipeIngredients.objects.get(recipe__id=parent_id, recipe__user=request.user, id=id)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse('Not Found')
        raise Http404
    if request.method == 'POST': 
        name = obj.name
        obj.delete()
        success_url = reverse('recipes:detail', kwargs={'id':parent_id})
        if request.htmx:
            return render(request, 'recipes/partials/ingredient-inline-delete-response.html', context={'name': name})
        return redirect(success_url)
    context = {
        'obj':obj
    }
    return render(request, 'recipes/delete.html', context=context)

@login_required
def recipe_detail_hx_view(request, id=None):
    if not request.htmx:
        raise Http404 
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
        if request.htmx:
            headers = {
                'HX-Redirect': obj.get_absolute_url() 
            }
            return HttpResponse('Created', headers=headers)

            # context = {
            #     'object':obj
            # }
            # return render(request, 'recipes/partials/detail.html', context=context)

        return redirect(obj.get_absolute_url())

    return render(request, 'recipes/create-update.html', context=context)

@login_required
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    new_ingredient_url = reverse('recipes:hx-ingredient-create', kwargs={'parent_id': id}) 
    context = {
        'form':form,
        'obj':obj,
        'new_ingredient_url':new_ingredient_url
    }
    if form.is_valid():
        form.save()
        context['message'] = True

    ### Adding Image Form:
    form_2 = RecipeIngredientsImageForm(request.POST or None, request.FILES or None)
    try:
        parent_obj = Recipe.objects.get(id=id, user=request.user)
    except:
        parent_obj = None
    if parent_obj is None:
        raise Http404
    if form_2.is_valid():
        obj_2 = form_2.save(commit = False)
        obj_2.recipe = parent_obj
        # obj.recipe_id = parent_id
        obj_2.save()
        # result = extract_text_via_ocr_service(obj.image)
        # obj.extracted = result
    context['image_form'] = form_2

    ###


    if request.htmx:
        return render(request, 'recipes/partials/forms.html', context)
    return render(request, 'recipes/create-update.html', context=context)


@login_required
def recipe_ingredient_update_hx_view(request, parent_id=None, id=None):
    if not request.htmx:
        raise Http404 
    try:
        parent_obj = Recipe.objects.get(id=parent_id, user=request.user)
    except:
        parent_obj = None
    if parent_obj is None:
           return HttpResponse('Not found.')
    
    instance = None
    if id is not None:
        try:
            instance = RecipeIngredients.objects.get(recipe=parent_obj, id=id)
        except:
            instance = None
    
    form = RecipeIngredientsForm(request.POST or None, instance=instance)
    url = instance.get_hx_edit_url() if instance else reverse('recipes:hx-ingredient-create', kwargs={'parent_id':parent_obj.id}) 
    context = {
        'url':url,
        'object': instance,
        'form': form
    }
    if form.is_valid():
        new_obj = form.save(commit=False)
        if instance is None:
            new_obj.recipe = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, 'recipes/partials/ingredient-inline.html', context=context)

    return render(request, 'recipes/partials/ingredient-form.html', context=context)



def recipe_ingredient_image_upload_view(request, parent_id):
    template_name = 'recipes/upload-image.html'
    if request.htmx:
        template_name = 'recipes/partials/image-upload-form.html'
    form = RecipeIngredientsImageForm(request.POST or None, request.FILES or None)
    try:
        parent_obj = Recipe.objects.get(id=parent_id, user=request.user)
    except:
        parent_obj = None
    if parent_obj is None:
        raise Http404
    if form.is_valid():
        obj = form.save(commit = False)
        obj.recipe = parent_obj
        # obj.recipe_id = parent_id
        obj.save()
        # result = extract_text_via_ocr_service(obj.image)
        # obj.extracted = result
    context = {
        'image_form': form
    }
    return render(request, template_name, context = context) 