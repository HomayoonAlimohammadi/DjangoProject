from django.urls import path
from recipes.views import (
    recipe_list_view,
    recipe_detail_view,
    recipe_create_view,
    recipe_update_view,
    recipe_detail_hx_view,
    recipe_ingredient_update_hx_view,
    recipe_delete_view,
    recipe_ingredient_delete_view,
    recipe_ingredient_image_upload_view
)

# order matters, they are gonna match the order they come in. order should make sense.
app_name = 'recipes' # recipes:list as a reverse call or recipes:create
urlpatterns = [
    path('', recipe_list_view, name='list'),
    path('create/', recipe_create_view, name='create'),
    path('hx/<int:parent_id>/ingredient/<int:id>/', recipe_ingredient_update_hx_view, name='hx-ingredient-detail'),
    path('hx/<int:parent_id>/ingredient/', recipe_ingredient_update_hx_view, name='hx-ingredient-create'),
    path('hx/<int:id>/', recipe_detail_hx_view, name='hx-detail'),
    path('<int:parent_id>/image-upload/', recipe_ingredient_image_upload_view),
    path('<int:parent_id>/ingredient/<int:id>/delete/', recipe_ingredient_delete_view, name='ingredient-delete'),
    path('<int:id>/delete/', recipe_delete_view, name='delete'),
    path('<int:id>/edit/', recipe_update_view, name='update'),
    path('<int:id>/', recipe_detail_view, name='detail')
]
# make sure to put '/' in the end of the urls, otherwise it won't work properly.