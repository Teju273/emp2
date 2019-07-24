from django.contrib import admin
from emp.models import User, Role, Employee

admin.site.register(Employee)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone')
    search_fields = ('id',)
    autocomplete_fields = ('role',)


admin.site.register(User, UserAdmin)


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('id',)


admin.site.register(Role, RoleAdmin)
