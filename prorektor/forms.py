from django import forms
from prorektor.models import ProrektorTopshiriq, ProrektorTopshiriqJavob, ProrektorTopshiriqJavobFile



# Prorektor topshiriqlari
class ProrektorTopshiriqCreateForm(forms.ModelForm):
    class Meta:
        model = ProrektorTopshiriq
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

class ProrektorTopshiriqUpdateForm(forms.ModelForm):
    class Meta:
        model = ProrektorTopshiriq
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

class ProrektorTopshiriqJavobForm(forms.ModelForm):
    class Meta:
        model = ProrektorTopshiriqJavob
        fields = ['title', 'body']  # yoki faqat ['body'] agar sarlavha kerak bo'lmasa
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Javob sarlavhasi"}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': "Javob matni"}),
        }

