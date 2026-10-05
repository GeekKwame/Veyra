from django.contrib import admin
from .models import User, UserProfile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'role', 'is_active', 'is_staff', 'created_at')
    search_fields = ('email', 'full_name')
    list_filter = ('role', 'is_active', 'is_staff')
    ordering = ('-created_at',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'available_hours_per_week', 'learning_style', 'public_portfolio_enabled')
