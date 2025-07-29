from  django import forms
from django.shortcuts import redirect, render
from users.models import Users
from users.choices import RoleChoice


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['username', 'last_name', 'first_name', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user