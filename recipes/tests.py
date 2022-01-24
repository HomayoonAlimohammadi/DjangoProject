from webbrowser import get
from wsgiref import validate
from django.test import TestCase
from django.contrib.auth import get_user_model
from recipes.models import Recipe, RecipeIngredients
from django.core.exceptions import ValidationError

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
        self.recipe_ingredient_a = RecipeIngredients.objects.create(
            recipe= self.recipe_a,
            name = 'Chicken',
            quantity='1/2',
            unit='pounds'
        )
        self.recipe_ingredient_b = RecipeIngredients.objects.create(
            recipe= self.recipe_a,
            name = 'Chicken',
            quantity='aldsfka',
            unit='pounds'
        )

    def test_user_count(self):
        qs = User.objects.all()
        self.assertEqual(qs.count(), 1)
    
    def test_user_recipe_reverse_count(self):
        user = self.user_a
        qs = user.recipe_set.all()
        self.assertEqual(qs.count(), 1)

    def test_user_recipe_forward_count(self):
        user = self.user_a
        qs = Recipe.objects.filter(user=user)
        self.assertEqual(qs.count(), 1)

    def test_user_recipe_ingredient_reverse_count(self):
        recipe = self.recipe_a
        qs = recipe.recipeingredients_set.all()
        self.assertEqual(qs.count(), 2)

    def test_user_recipe_ingredient_forward_count(self):
        recipe = self.recipe_a
        qs = RecipeIngredients.objects.filter(recipe=recipe)
        self.assertEqual(qs.count(), 2)

    def test_user_two_level_relation(self):
        user = self.user_a
        recipe = self.recipe_a
        # recipe__user is a two level relation 
        # why can't you write user__recipe=recipe? maybe because the hierarchy?
        qs = RecipeIngredients.objects.filter(recipe__user=user)
        self.assertEqual(qs.count(), 2)

    def test_user_two_level_reverse_relation(self):
        user = self.user_a
        recipeingredient_ids = user.recipe_set.all().values_list('recipeingredients', flat=True)
        # qs = RecipeIngredients.objects.filter(recipe__user=user)
        self.assertEqual(recipeingredient_ids.count(), 2)

    def test_user_two_level_relation_via_recipes(self):
        user = self.user_a
        ids = user.recipe_set.all().values_list('id', flat=True)
        qs = RecipeIngredients.objects.filter(recipe__id__in=ids)
        self.assertEqual(qs.count(), 2)

    def test_unit_measure_validation_error(self):
        invalid_unit = ['nada', 'something random']
        with self.assertRaises(ValidationError):
            for unit in invalid_unit:
                ingredient = RecipeIngredients(
                    name = 'New',
                    quantity = 10,
                    recipe = self.recipe_a,
                    unit = unit
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
    
    def test_quantity_as_float(self):
        self.assertIsNotNone(self.recipe_ingredient_a.quantity_as_float)
        self.assertIsNone(self.recipe_ingredient_b.quantity_as_float)
        
    
