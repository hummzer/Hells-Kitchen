import datetime
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields
from meals.models import Recipe, Ingredient, Category

class CategoryResource(ModelResource):
    class Meta:
        queryset = Category.objects.all()
        allowed_methods = ['get']
        authorization = Authorization()

class IngredientResource(ModelResource):
    recipe = fields.ToOneField('meals.api.resources.RecipeResource', 'recipe')
    
    class Meta:
        queryset = Ingredient.objects.all()
        allowed_methods = ['get']
        authorization = Authorization()

class RecipeResource(ModelResource):
    ingredients = fields.ToManyField(IngredientResource, 'ingredients', full=True)
    category = fields.ToOneField(CategoryResource, 'category', full=True)
    
    class Meta:
        queryset = Recipe.objects.all()
        allowed_methods = ['get']
        authorization = Authorization()

class DailyMenuResource(ModelResource):  # Replaces MenuResource
    class Meta:
        queryset = Recipe.objects.order_by('?')[:3]
        allowed_methods = ['get']
        authorization = Authorization()
