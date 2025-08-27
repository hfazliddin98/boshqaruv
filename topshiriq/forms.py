from django import forms
from .models import Topshiriq, TopshiriqJavob, TopshiriqJavobFile
from django.core.exceptions import ValidationError
from users.models import Users
from users.choices import RoleChoice

class TopshiriqCreateForm(forms.ModelForm):
    class Meta:
        model = Topshiriq
        fields = ['title', 'body', 'bajaruvchi_user', 'xolat', 'boshlanish_vaqti', 'tugash_vaqti']
        widgets = {
            'boshlanish_vaqti': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'tugash_vaqti': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

class TopshiriqUpdateForm(forms.ModelForm):
    class Meta:
        model = Topshiriq
        fields = ['title', 'body', 'bajaruvchi_user', 'xolat', 'boshlanish_vaqti', 'tugash_vaqti']
        widgets = {
            'boshlanish_vaqti': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'tugash_vaqti': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.boshlanish_vaqti:
            self.initial['boshlanish_vaqti'] = self.instance.boshlanish_vaqti.strftime('%Y-%m-%dT%H:%M')
        if self.instance and self.instance.tugash_vaqti:
            self.initial['tugash_vaqti'] = self.instance.tugash_vaqti.strftime('%Y-%m-%dT%H:%M')
        # Add bootstrap class to other fields
        for k, f in self.fields.items():
            if 'class' not in f.widget.attrs:
                f.widget.attrs['class'] = 'form-control'



class TopshiriqForm(forms.ModelForm):
    class Meta:
        model = Topshiriq
        fields = ['title', 'body', 'bajaruvchi_user', 'xolat', 'boshlanish_vaqti', 'tugash_vaqti']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'bajaruvchi_user': forms.Select(attrs={'class': 'form-select'}),
            'xolat': forms.Select(attrs={'class': 'form-select'}),
            'boshlanish_vaqti': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'tugash_vaqti': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        target_role = kwargs.pop('target_role', None)
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Faqat target_role bo‘yicha userlarni ko‘rsatish
        if target_role:
            if RoleChoice.BOLIM_RAHBARI == target_role:
                print(True)
            else:
                print(False)
            # self.fields['bajaruvchi_user'].queryset = Users.objects.all()
            self.fields['bajaruvchi_user'].queryset = Users.objects.filter(role=target_role)

        # Bootstrap class qo‘shish
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        yaratuvchi = self.initial.get('user')
        bajaruvchi = cleaned_data.get('bajaruvchi_user')
        if yaratuvchi and bajaruvchi and yaratuvchi == bajaruvchi:
            raise ValidationError("O'zingizga topshiriq bera olmaysiz!")
        return cleaned_data

class TopshiriqJavobForm(forms.ModelForm):
   

    class Meta:
        model = TopshiriqJavob
        fields = ['title', 'body', 'izoh']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Javob sarlavhasi'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Javob matni'}),
            'izoh': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Izoh (ixtiyoriy)'}),
        }

    def save(self, commit=True, topshiriq=None, bajaruvchi_user=None, files=None):
        javob = super().save(commit=False)
        if topshiriq:
            javob.topshiriq = topshiriq
        if bajaruvchi_user:
            javob.bajaruvchi_user = bajaruvchi_user
        if commit:
            javob.save()
            # Fayllarni saqlash
            if files:
                for f in files.getlist('files'):
                    TopshiriqJavobFile.objects.create(javob=javob, file=f)
        return javob
    

class TopshiriqBaxolashForm(forms.ModelForm):
    class Meta:
        model = Topshiriq
        fields = ['status', 'baxo']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'baxo': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': '0', 
                'max': '100', 
                'placeholder': 'Baho (0-100)',
                'step': '1'
            }),
        }
