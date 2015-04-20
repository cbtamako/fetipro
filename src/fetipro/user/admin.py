# encoding=utf-8

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm, UserCreationForm
from django.contrib.admin.forms import AdminPasswordChangeForm

from fetipro.user.models import User
from django.forms.models import ModelForm


class UserChangeForm(DjangoUserChangeForm):

    class Meta:
        model = User
        fields = "__all__"


class UserAdmin(DjangoUserAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ("個人情報", {'fields': ('display_name', 'email')}),
        ("権限", {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ("時刻", {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('username', 'email', 'display_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'display_name', 'email')
    ordering = ('username',)
    # filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)
