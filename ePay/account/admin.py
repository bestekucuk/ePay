from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

#admin.site.register(CustomUser)

class UserAdminConfig(UserAdmin):
    ordering=('email',)

    list_display=('email','first_name', 'last_name','balance','para_birimi_secimi','is_active','is_staff','is_superuser')
    fieldsets = (
        (None, {
            "fields": ('email','first_name', 'last_name','para_birimi_secimi','balance'),}),
            ('Permissions',{'fields':('is_active','is_staff')})
    )
    add_fieldsets = (
        (None, {
            "classes":('wide',),
            "fields": (
                'email','first_name', 'last_name','para_birimi_secimi','is_active','is_staff','password1','password2'
            ),
        }),
    )
    readonly_fields = ['balance']  # balance alanını readonly olarak ayarla

admin.site.register(CustomUser,UserAdminConfig)