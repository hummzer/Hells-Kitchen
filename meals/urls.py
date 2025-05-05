from django.urls import path
from meals import views

urlpatterns = [
    path('', views.RecipeView.as_view(), name='home'),
    path('create/', views.CreateMeal.as_view(), name='create'),
    path('<int:recipe_id>/', views.DetailView.as_view(), name='detail'),
    path('favorites/', views.FavoritesView.as_view(), name='favorites'),
    path('choose/', views.ChooseMeal.as_view(), name='choose'),
    path('generate-instructions/', views.generate_instructions, name='generate_instructions'),
    path('generate-ingredients/', views.generate_ingredients, name='generate_ingredients'),

]
