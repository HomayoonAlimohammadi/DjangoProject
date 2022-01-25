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
