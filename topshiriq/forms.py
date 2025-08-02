from django import forms
from topshiriq.models import RektorTopshiriq, RektorTopshiriqFile

class RektorTopshiriqCreateForm(forms.ModelForm):
    class Meta:
        model = RektorTopshiriq
        fields = ['bajaruvchi_user', 'title', 'body', 'xolat', 'boshlanish_vaqti', 'tugash_vaqti', 'izoh']
        widgets = {
            'bajaruvchi_user': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'xolat': forms.Select(attrs={'class': 'form-control'}),
            'boshlanish_vaqti': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'tugash_vaqti': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'izoh': forms.Textarea(attrs={'class': 'form-control'}),
        }

    



class RektorTopshiriqUpdateForm(forms.ModelForm):
    class Meta:
        model = RektorTopshiriq
        fields = ['bajaruvchi_user', 'title', 'body', 'xolat', 'boshlanish_vaqti', 'tugash_vaqti', 'izoh']
        widgets = {
            'bajaruvchi_user': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'xolat': forms.Select(attrs={'class': 'form-control'}),
            'boshlanish_vaqti': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'tugash_vaqti': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'izoh': forms.Textarea(attrs={'class': 'form-control'}),        
        }
    
