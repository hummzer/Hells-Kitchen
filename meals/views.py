from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView  # Added DetailView
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q  # Added for complex queries
import random  # Added for random selection
from .models import Recipe, Category, Ingredient
from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)
from django.conf import settings
import re
from django.views.generic import DetailView  # Re-add to imports

class DetailView(DetailView):
    model = Recipe
    template_name = 'meals/detail.html'
    context_object_name = 'recipe'
    extra_context = {'active_nav': 'home'}

class RecipeView(View):
    def get(self, request):
        recipes = Recipe.objects.all()
        return render(request, 'meals/index.html', {
            'recipes': recipes,
            'active_nav': 'home'
        })

class CreateMeal(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'meals/create.html', {
            'categories': categories,
            'active_nav': 'create'
        })

    def post(self, request):
        try:
            recipe = Recipe.objects.create(
                title=request.POST['title'],
                instructions=request.POST['instructions'],
                category_id=request.POST['category'],
                portions=1,
                prep_time=0,
                cook_time=0
            )
            ingredients_text = request.POST.get('ingredients', '')
            for line in ingredients_text.split('\n'):
                line = line.strip()
                if line:
                    match = re.match(r'^(\d*\.?\d*)\s*(\w+)?\s*(.*)$', line)
                    if match:
                        quantity, units, name = match.groups()
                        quantity = float(quantity) if quantity else None
                        Ingredient.objects.create(
                            recipe=recipe,
                            name=name or 'Unknown',
                            quantity=quantity,
                            units=units if units in [choice[0] for choice in Ingredient.UNIT_CHOICES] else None
                        )
            return JsonResponse({'status': 'success', 'message': 'Meal Saved'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

class FavoritesView(ListView):
    model = Recipe
    template_name = 'meals/favorites.html'
    context_object_name = 'recipes'
    extra_context = {'active_nav': 'favorites'}

    def get_queryset(self):
        return Recipe.objects.filter(is_favorite=True)

class ChooseMeal(View):
    def get(self, request):
        # Get recipes that are either favorites or any created recipe
        eligible_recipes = Recipe.objects.filter(Q(is_favorite=True) | Q(id__gte=1))
        if not eligible_recipes.exists():
            return JsonResponse({
                'status': 'error',
                'message': 'No meals available to choose. Add some recipes or mark them as favorites!'
            }, status=404)

        # Select a random recipe
        recipe = random.choice(eligible_recipes)

        # Prepare ingredients list
        ingredients = [
            str(ingredient) for ingredient in recipe.ingredients.all()
        ]

        # Return recipe details as JSON
        return JsonResponse({
            'status': 'success',
            'recipe': {
                'id': recipe.id,
                'title': recipe.title,
                'category': recipe.category.name if recipe.category else 'No category',
                'instructions': recipe.instructions,
                'ingredients': ingredients,
                'portions': recipe.portions or 1,
                'total_time': recipe.get_total_time(),
                'is_favorite': recipe.is_favorite
            }
        })

@csrf_exempt
def generate_instructions(request):
    if request.method == 'POST':
        meal_name = request.POST.get('meal_name')
        try:
            response = client.chat.completions.create(model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a recipe assistant. Provide a concise list of cooking instructions for the given meal."},
                {"role": "user", "content": f"Provide step-by-step instructions for preparing {meal_name}."}
            ],
            max_tokens=200)
            instructions = response.choices[0].message.content
            return JsonResponse({'instructions': instructions})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def generate_ingredients(request):
    if request.method == 'POST':
        meal_name = request.POST.get('meal_name')
        try:
            response = client.chat.completions.create(model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a recipe assistant. Provide a concise list of ingredients for the given meal."},
                {"role": "user", "content": f"Provide a list of ingredients for preparing {meal_name}."}
            ],
            max_tokens=100)
            ingredients = response.choices[0].message.content
            return JsonResponse({'ingredients': ingredients})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)
