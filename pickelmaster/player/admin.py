from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from player.models import PlayerModel


class PlayerModelAdmin(UserAdmin):
    # inlines = [EnrollmentInline]      # Commented out to see if this corrects the heavy CPU usage in the Admin Panel.  Confirm before removing.
    search_fields = ('username', 'email', )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Pickel Player', {'fields': ('aka', )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(PlayerModel, PlayerModelAdmin)
