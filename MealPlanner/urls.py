from django.urls import path, include
from django.contrib import admin
from tastypie.api import Api
from meals import views
from meals.api.resources import RecipeResource, DailyMenuResource  # Changed from MenuResource

v1_api = Api(api_name='v1')
v1_api.register(RecipeResource())
v1_api.register(DailyMenuResource())  # Register our new resource

urlpatterns = [
    path('', views.RecipeView.as_view()),
    path('admin/', admin.site.urls),
    path('meals/', include('meals.urls')),
    path('api/', include(v1_api.urls)),
]
