from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User,Profile
# Register your models here.

class CustumUserAdmin(UserAdmin):
    """
    this class shows us how to exhibit admin panel
    """
    model = User
    list_display = ('email','is_superuser','is_active','is_verified')
    list_filter = ('email','is_superuser','is_active','is_verified')
    search_fields = ('email','is_active')
    ordering = ('email',)
    fieldsets = (
        ('Authentication', {
            "fields": (
                "email", "password"),}),
        ('Permissions', {
            "fields": (
                "is_staff", "is_superuser","is_active","is_verified"),}),
        ('Group Permissions', {
            "fields": (
                "groups", "user_permissions"),}),
        ('Important date', {
            "fields": (
                "last_login",),})
    )
    
    
    add_fieldsets = (
        (None, {
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_verified","is_active","groups", "user_permissions"
            )}
        ),
    )
    
    




admin.site.register(User,CustumUserAdmin)
admin.site.register(Profile)