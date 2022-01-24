from django.contrib.auth import get_user_model
from django.contrib import admin
from recipes.models import Recipe, RecipeIngredients

admin.site.register(RecipeIngredients)
User = get_user_model()


class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredients
    extra = 0 # how many RecipeIngredients you want to have right of the bat in any recipe
    readonly_fields = ['quantity_as_float','as_mks', 'as_imperial']
    # fields = ['name', 'quantity', 'unit', 'directions', 'quantity_as_float'] # which features you want there to be shown

class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list__display = ['name', 'user'] # features to be shown in admin/Recipes
    readonly_fields = ['timestamp', 'updated'] # features that are readonly in each recipe page
    raw_id_fields = ['user'] # make this feature a raw id field, so getting rid of the enormous drop down menu

admin.site.register(Recipe, RecipeAdmin)