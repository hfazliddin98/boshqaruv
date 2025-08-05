from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from users.models import Users, Bolim, Fakultet
from users.choices import RoleChoice


# --- Foydalanuvchi Kirish ---
class KirishForm(forms.Form):
    username = forms.CharField(
        label='Foydalanuvchi nomi',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Parol',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8
    )

# --- Foydalanuvchi Yaratish ---
class UserCreateForm(forms.Form):
    username = forms.CharField(
        label='Foydalanuvchi nomi',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='Familiya',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        label='Ism',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    bolim = forms.ModelChoiceField(
        label='Bo‘lim',
        queryset=Bolim.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label='Yangi parol',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8
    )
    password2 = forms.CharField(
        label='Parolni tasdiqlang',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    is_active = forms.BooleanField(
        label='Aktiv foydalanuvchi',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if not password1 or not password2:
            raise ValidationError("Ikkala parol maydoni to'ldirilishi shart!")

        if password1 != password2:
            raise ValidationError("Parollar mos emas!")

        cleaned_data['password'] = make_password(password1)  # haslangan
        cleaned_data['parol'] = password1  # agar ochiq holatda saqlamoqchi bo‘lsangiz
        return cleaned_data

    def save(self, role):
        user = Users.objects.create(
            username=self.cleaned_data['username'],
            last_name=self.cleaned_data['last_name'],
            first_name=self.cleaned_data['first_name'],
            bolim=self.cleaned_data['bolim'],
            password=self.cleaned_data['password'],  # hashed
            parol=self.cleaned_data['parol'],        # plain text (xavfsizlikka qarab qaror qabul qiling)
            is_active=self.cleaned_data['is_active'],
            role=role
        )
        return user

# --- Foydalanuvchi Yangilash ---
class UserUpdateForm(forms.Form):
    username = forms.CharField(
        label='Foydalanuvchi nomi',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='Familiya',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        label='Ism',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    bolim = forms.ModelChoiceField(
        label='Bo‘lim',
        queryset=Users.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label='Yangi parol',
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8
    )
    password2 = forms.CharField(
        label='Parolni tasdiqlang',
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    is_active = forms.BooleanField(
        label='Aktiv foydalanuvchi',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def __init__(self, *args, **kwargs):
        user_instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

        # `bolim` querysetini to'ldirish
        from .models import Bolim
        self.fields['bolim'].queryset = Bolim.objects.all()

        # Agar `instance` mavjud bo'lsa, formani to'ldirib ko'rsatamiz
        if user_instance:
            self.fields['username'].initial = user_instance.username
            self.fields['last_name'].initial = user_instance.last_name
            self.fields['first_name'].initial = user_instance.first_name
            self.fields['bolim'].initial = user_instance.bolim
            self.fields['is_active'].initial = user_instance.is_active

        self.instance = user_instance

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                raise ValidationError("Parollar mos emas!")

            # Parolni ochiq saqlamoqchi bo‘lsangiz (masalan: `parol` degan maydonga)
            cleaned_data['parol'] = password1  # ochiq saqlanadigan maydon (agar mavjud bo‘lsa)

            # Hashlangan parolni tayyorlaymiz
            cleaned_data['password'] = make_password(password1)

        return cleaned_data

    def save(self):
        user = self.instance
        user.username = self.cleaned_data['username']
        user.last_name = self.cleaned_data['last_name']
        user.first_name = self.cleaned_data['first_name']
        user.bolim = self.cleaned_data['bolim']
        user.is_active = self.cleaned_data['is_active']
        
        if self.cleaned_data.get('password'):
            user.password = self.cleaned_data['password']
        
        # Agar sizda `parol` degan ochiq maydon bo‘lsa, uni ham saqlang
        if 'parol' in self.cleaned_data:
            user.parol = self.cleaned_data['parol']
        
        user.save()
        return user

# --- BO'LIM BOSHLIG'I YARATISH ---
class BolimBoshliqCreateForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Yangi parol',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8
    )
    password2 = forms.CharField(
        label='Parolni tasdiqlang',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Users
        fields = ['username', 'last_name', 'first_name', 'bolim', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bolim': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bolim'].queryset = Bolim.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if not password1 or not password2:
            raise ValidationError("Ikkala parol maydoni to'ldirilishi shart!")
        if password1 != password2:
            raise ValidationError("Parollar mos emas!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = RoleChoice.BOLIM_BOSHLIGI
        user.set_password(self.cleaned_data['password1'])
        user.parol = self.cleaned_data['password1']
        if commit:
            user.save()
        return user

# --- BO'LIM BOSHLIG'I YANGILASH ---
class BolimBoshliqUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Yangi parol',
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8
    )
    password2 = forms.CharField(
        label='Parolni tasdiqlang',
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Users
        fields = ['username', 'last_name', 'first_name', 'bolim', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bolim': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bolim'].queryset = Bolim.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 or password2:
            if password1 != password2:
                raise ValidationError("Parollar mos emas!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get('password1')
        if password1:
            user.set_password(password1)
            user.parol = password1
        if commit:
            user.save()
        return user

# --- DEKAN YARATISH ---
class DekanCreateForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Yangi parol',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8
    )
    password2 = forms.CharField(
        label='Parolni tasdiqlang',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Users
        fields = ['username', 'last_name', 'first_name', 'fakultet', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'fakultet': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fakultet'].queryset = Fakultet.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if not password1 or not password2:
            raise ValidationError("Ikkala parol maydoni to'ldirilishi shart!")
        if password1 != password2:
            raise ValidationError("Parollar mos emas!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = RoleChoice.DEKAN
        user.set_password(self.cleaned_data['password1'])
        user.parol = self.cleaned_data['password1']
        if commit:
            user.save()
        return user

# --- DEKAN YANGILASH ---
class DekanUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Yangi parol',
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8
    )
    password2 = forms.CharField(
        label='Parolni tasdiqlang',
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Users
        fields = ['username', 'last_name', 'first_name', 'fakultet', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'fakultet': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fakultet'].queryset = Fakultet.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 or password2:
            if password1 != password2:
                raise ValidationError("Parollar mos emas!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get('password1')
        if password1:
            user.set_password(password1)
            user.parol = password1
        if commit:
            user.save()
        return user
