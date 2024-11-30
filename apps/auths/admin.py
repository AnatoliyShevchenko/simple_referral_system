# Django
from django.contrib import admin
from django.contrib.auth.hashers import make_password

# Local
from .models import User


class UserAdmin(admin.ModelAdmin):

    model = User
    list_display = (
        "phone", "is_active", "is_staff", "is_superuser"
    )

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.password = make_password(
                form.cleaned_data['password']
            )
        super().save_model(request, obj, form, change)
        

admin.site.register(User, UserAdmin)
