from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, Genre


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User Admin"""
    list_display = ['email', 'name', 'username', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    search_fields = ['email', 'name', 'username']
    ordering = ['-date_joined']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'username')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'username', 'password1', 'password2'),
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """User Profile Admin"""
    list_display = ['user', 'bio_preview', 'genres_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'user__name', 'bio']
    filter_horizontal = ['favorite_genres']

    def bio_preview(self, obj):
        return obj.bio[:50] + '...' if len(obj.bio) > 50 else obj.bio

    bio_preview.short_description = 'Bio'

    def genres_count(self, obj):
        return obj.favorite_genres.count()

    genres_count.short_description = 'Favorite Genres'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Genre Admin"""
    list_display = ['name', 'slug', 'users_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

    def users_count(self, obj):
        return obj.users.count()

    users_count.short_description = 'Users'