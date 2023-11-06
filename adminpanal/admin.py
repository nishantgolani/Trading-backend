# admin.py

from django.contrib import admin
from .models import ParentModel, ChildModel

class ParentModelAdmin(admin.ModelAdmin):
    list_display = ['name']

    def has_module_permission(self, request):
        # Check if the user has the "full_access_parent_admin" permission
        return request.user.has_perm('app.full_access_parent_admin')

class ChildModelAdmin(admin.ModelAdmin):
    list_display = ['child_name']

    def has_module_permission(self, request):
        # Check if the user has the "limited_access_child_admin" permission
        return request.user.has_perm('app.limited_access_child_admin')

admin.site.register(ParentModel, ParentModelAdmin)
admin.site.register(ChildModel, ChildModelAdmin)
