from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import SigninForm, SignupForm
from .models import MaieuclicUser


# Register your models here.
class MaieuclicUserAdmin(UserAdmin):
    add_form = SignupForm
    # form = CustomUserChangeForm
    model = MaieuclicUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': ('email', 'password', 'pwd_confirm', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(MaieuclicUser, MaieuclicUserAdmin)
