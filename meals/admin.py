from django.contrib import admin
from meals.models import Recipe, Ingredient, Category

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 3
    fields = ('name', 'quantity', 'units', 'notes')
    classes = ('collapse',)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline]
    list_display = ('title', 'category', 'portions', 'is_favorite', 'last_cooked')
    list_filter = ('category', 'is_favorite')
    search_fields = ('title', 'instructions')
    fieldsets = (
        (None, {
            'fields': ('title', 'category', 'is_favorite')
        }),
        ('Details', {
            'fields': ('portions', 'prep_time', 'cook_time', 'instructions'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity_with_units', 'recipe')
    list_filter = ('recipe__category',)
    search_fields = ('name', 'recipe__title')
    
    def quantity_with_units(self, obj):
        if obj.quantity and obj.units:
            return f"{obj.quantity} {obj.units}"
        elif obj.quantity:
            return str(obj.quantity)
        return "-"
    quantity_with_units.short_description = 'Quantity'
