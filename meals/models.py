from django.db import models
from django.core.validators import MinValueValidator
import math
from fractions import Fraction
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    instructions = models.TextField()
    portions = models.PositiveIntegerField(default=1, blank=True, null=True)
    prep_time = models.PositiveIntegerField(help_text="Prep time in minutes", blank=True, null=True)
    cook_time = models.PositiveIntegerField(help_text="Cook time in minutes", blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recipes'
    )
    is_favorite = models.BooleanField(default=False)
    last_cooked = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title
    
    def get_total_time(self):
        return (self.prep_time or 0) + (self.cook_time or 0)

class Ingredient(models.Model):
    UNIT_CHOICES = [
        ('g', 'grams'),
        ('kg', 'kilograms'),
        ('ml', 'milliliters'),
        ('l', 'liters'),
        ('tsp', 'teaspoons'),
        ('tbsp', 'tablespoons'),
        ('cup', 'cups'),
        ('item', 'items'),
    ]
    
    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE, 
        related_name='ingredients'
    )
    name = models.CharField(max_length=100)
    quantity = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0)]
    )
    units = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        blank=True,
        null=True
    )
    notes = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        desc = ""
        
        if self.quantity is not None:
            whole_num = math.floor(self.quantity)
            decimal = self.quantity - whole_num

            if whole_num > 0.0:
                desc += str(whole_num) + " "

            if decimal > 0.0:
                small_num = Fraction(decimal).limit_denominator(8)
                desc += str(small_num) + " "
        
        if self.units:
            desc += f"{self.units} "
        
        desc += self.name
        
        if self.notes:
            desc += f", {self.notes}"
            
        return desc.strip()
