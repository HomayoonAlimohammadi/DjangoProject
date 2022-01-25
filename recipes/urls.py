from django.urls import path
from recipes.views import (
    recipe_list_view,
    recipe_detail_view,
    recipe_create_view,
    recipe_update_view
)

# order matters, they are gonna match the order they come in. order should make sense.
app_name = 'recipes' # recipes:list as a reverse call or recipes:create
urlpatterns = [
    path('', recipe_list_view, name='list'),
    path('create/', recipe_create_view, name='create'),
    path('<int:id>/edit/', recipe_update_view, name='update'),
    path('<int:id>/', recipe_detail_view, name='detail')
]