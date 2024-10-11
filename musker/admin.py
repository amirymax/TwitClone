from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Meep

# Unregister Groups
admin.site.unregister(Group)


class ProfileInline(admin.StackedInline):
    model = Profile

# Extend User model
class UserAdmin(admin.ModelAdmin):
    user = User

    fields = ['username']
    inlines = [ProfileInline]

# Unregister initial user
admin.site.unregister(User)

# Reregister user and Profile
admin.site.register(User, UserAdmin)
# admin.site.register(Profile)

# Register Meeps
admin.site.register(Meep)