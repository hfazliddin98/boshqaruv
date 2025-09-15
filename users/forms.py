from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Users, Struktura
from users.choices import RoleChoice,   ALLOWED_USER_MAP

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

class UserCreateForm(UserCreationForm):
    last_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Familya'}),
        label="Familya"
    )
    first_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ism'}),
        label="Ism"
    )

    sharif = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sharif'}),
        label="Sharif"
    )
    role = forms.ChoiceField(
        choices=[],  # choices bo‘sh, __init__da to‘ldiriladi
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Rol"
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Foydalanuvchi nomi'}),
        label="Foydalanuvchi nomi"
    )
    password1 = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parol'}),
        min_length=8,
        required=True,
        error_messages={
            'required': "Parolni kiriting",
            'min_length': "Parol kamida 8 ta belgidan iborat bo‘lishi kerak!"
        }
    )
    password2 = forms.CharField(
        label="Parolni tasdiqlang",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parolni tasdiqlang'}),
        min_length=8,
        required=True,
        error_messages={
            'required': "Parolni tasdiqlang",
            'min_length': "Parol kamida 8 ta belgidan iborat bo‘lishi kerak!"
        }
    )
    is_active = forms.BooleanField(
        label='Aktiv foydalanuvchi',
        required=True,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Users
        fields = ('username', 'last_name', 'first_name', 'sharif', 'role', 'struktura', 'is_active', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        target_role = kwargs.pop('target_role', None)
        super().__init__(*args, **kwargs)

        # Faqat target_role ni ko'rsatamiz, boshqa rollarni emas
        if target_role:
            self.fields['role'].choices = [
                (target_role, dict(RoleChoice.choices).get(target_role, target_role))
            ]
            self.fields['role'].initial = target_role
            # Target role ga mos strukturalarni ko'rsatamiz
            self.fields['struktura'].queryset = Struktura.objects.filter(role=target_role)
        else:
            # Agar target_role berilmagan bo'lsa, barcha rollarni ko'rsatamiz
            self.fields['role'].choices = RoleChoice.choices
            self.fields['struktura'].queryset = Struktura.objects.all()

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Parollar mos emas!")
        if password1 and len(password1) < 8:
            raise forms.ValidationError("Parol kamida 8 ta belgidan iborat bo‘lishi kerak!")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("password1")
        if new_password:
            user.parol = new_password  # oddiy parol maydoni uchun
            user.set_password(new_password)  # Django auth uchun
        if commit:
            user.save()
        return user
    
    

class UserUpdateForm(UserChangeForm):
    last_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Familya'}),
        label="Familya"
    )
    first_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ism'}),
        label="Ism"
    )
    sharif = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sharif'}),
        label="Sharif"
    )
    struktura = forms.ModelChoiceField(
        queryset=Struktura.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Struktura"
    )
    role = forms.ChoiceField(
        choices=[],
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Rol"
    )
    password1 = forms.CharField(
        label='Yangi parol',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Yangi parol'}),
        required=True,
        min_length=8
    )
    password2 = forms.CharField(
        label='Yangi parolni tasdiqlang',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Yangi parolni tasdiqlang'}),
        required=True,
        min_length=8
    )
    is_active = forms.BooleanField(
        label='Aktiv foydalanuvchi',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Users
        fields = ('username', 'last_name', 'first_name', 'sharif', 'role', 'struktura', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        target_role = kwargs.pop('target_role', None)
        super().__init__(*args, **kwargs)

        # Har doim barcha rollarni ko'rsatamiz
        self.fields['role'].choices = RoleChoice.choices
        
        if target_role:
            print(f"Initializing FoydalanuvchiUpdateForm with target_role: {target_role}")
            self.fields['role'].initial = target_role
            # Tanlangan rolga mos strukturalarni ko'rsatamiz
            self.fields['struktura'].queryset = Struktura.objects.filter(role=target_role)
        else:
            # Hech qanday rol tanlanmagan bo'lsa, barcha strukturalarni ko'rsatamiz
            self.fields['struktura'].queryset = Struktura.objects.all()

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Parollar mos emas!")
            if password1 and len(password1) < 8:
                raise forms.ValidationError("Parol kamida 8 ta belgidan iborat bo‘lishi kerak!")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("password1")
        if new_password:
            user.parol = new_password  # oddiy parol maydoni uchun
            user.set_password(new_password)  # Django auth uchun
        if commit:
            user.save()
        return user

class FoydalanuvchiCreateForm(UserCreationForm):
    last_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Familya'}),
        label="Familya"
    )
    first_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ism'}),
        label="Ism"
    )

    sharif = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sharif'}),
        label="Sharif"
    )
    role = forms.ChoiceField(
        choices=RoleChoice.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Lavozim/Rol"
    )
    yaratgan_user = forms.ModelChoiceField(
        queryset=Users.objects.filter(is_superuser=False),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Yaratgan foydalanuvchi"
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Foydalanuvchi nomi'}),
        label="Foydalanuvchi nomi"
    )
    password1 = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parol'}),
        min_length=8,
        required=True,
        error_messages={
            'required': "Parolni kiriting",
            'min_length': "Parol kamida 8 ta belgidan iborat bo‘lishi kerak!"
        }
    )
    password2 = forms.CharField(
        label="Parolni tasdiqlang",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parolni tasdiqlang'}),
        min_length=8,
        required=True,
        error_messages={
            'required': "Parolni tasdiqlang",
            'min_length': "Parol kamida 8 ta belgidan iborat bo‘lishi kerak!"
        }
    )
    is_active = forms.BooleanField(
        label='Aktiv foydalanuvchi',
        required=True,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Users
        fields = ('username', 'last_name', 'first_name', 'sharif', 'role', 'yaratgan_user', 'struktura', 'is_active', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        target_role = kwargs.pop('target_role', None)
        super().__init__(*args, **kwargs)

        # Har doim barcha rollarni ko'rsatamiz
        self.fields['role'].choices = RoleChoice.choices
        
        if target_role:
            self.fields['role'].initial = target_role
            # Tanlangan rolga mos strukturalarni ko'rsatamiz
            self.fields['struktura'].queryset = Struktura.objects.filter(role=target_role)
        else:
            # Hech qanday rol tanlanmagan bo'lsa, barcha strukturalarni ko'rsatamiz
            self.fields['struktura'].queryset = Struktura.objects.all()

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Parollar mos emas!")
        if password1 and len(password1) < 8:
            raise forms.ValidationError("Parol kamida 8 ta belgidan iborat bo‘lishi kerak!")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("password1")
        if new_password:
            user.parol = new_password  # oddiy parol maydoni uchun
            user.set_password(new_password)  # Django auth uchun
        if commit:
            user.save()
        return user
    
    

class FoydalanuvchiUpdateForm(UserChangeForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Foydalanuvchi nomi'}),
        label="Foydalanuvchi nomi"
    )
    last_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Familya'}),
        label="Familya"
    )
    first_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ism'}),
        label="Ism"
    )
    sharif = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sharif'}),
        label="Sharif"
    )
    struktura = forms.ModelChoiceField(
        queryset=Struktura.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Struktura"
    )
    role = forms.ChoiceField(
        choices=RoleChoice.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Lavozim/Rol"
    )
    password1 = forms.CharField(
        label='Yangi parol',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Yangi parol'}),
        required=True,
        min_length=8
    )
    password2 = forms.CharField(
        label='Yangi parolni tasdiqlang',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Yangi parolni tasdiqlang'}),
        required=True,
        min_length=8
    )
    is_active = forms.BooleanField(
        label='Aktiv foydalanuvchi',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Users
        fields = ('username', 'last_name', 'first_name', 'sharif', 'role', 'struktura', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        target_role = kwargs.pop('target_role', None)
        super().__init__(*args, **kwargs)

        # Har doim barcha rollarni ko'rsatamiz
        self.fields['role'].choices = RoleChoice.choices
        
        # AJAX uchun har doim barcha strukturalarni ko'rsatamiz
        self.fields['struktura'].queryset = Struktura.objects.all()
        
        if target_role:
            self.fields['role'].initial = target_role

    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Bo'sh joylarni ruxsat berish, faqat unique tekshirish
        if username:
            # Faqat bo'sh username tekshirish
            username = username.strip()  # Boshi va oxiridagi bo'sh joylarni olib tashlash
            
            if not username:
                raise forms.ValidationError("Foydalanuvchi nomi bo'sh bo'lishi mumkin emas!")
            
            # Unique tekshirish (update uchun)
            if self.instance and self.instance.pk:
                if Users.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                    raise forms.ValidationError("Bu foydalanuvchi nomi allaqachon mavjud!")
            else:
                if Users.objects.filter(username=username).exists():
                    raise forms.ValidationError("Bu foydalanuvchi nomi allaqachon mavjud!")
        
        return username

    def clean_struktura(self):
        """
        AJAX orqali tanlangan strukturani tekshirish
        """
        struktura = self.cleaned_data.get('struktura')
        role = self.cleaned_data.get('role')
        
        if struktura and role:
            # Tanlangan struktura tanlangan rolga mos ekanligini tekshiramiz
            if struktura.role != role:
                raise forms.ValidationError(f"Tanlangan struktura '{struktura.name}' '{role}' roli uchun emas!")
        
        return struktura

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Parollar mos emas!")
            if password1 and len(password1) < 8:
                raise forms.ValidationError("Parol kamida 8 ta belgidan iborat bo‘lishi kerak!")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("password1")
        if new_password:
            user.parol = new_password  # oddiy parol maydoni uchun
            user.set_password(new_password)  # Django auth uchun
        if commit:
            user.save()
        return user



class StrukturaCreateForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Struktura nomini kiriting'}),
        label="Struktura nomi"
    )
    role = forms.ChoiceField(
        choices=RoleChoice.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Lavozim/Rol"
    )
    is_active = forms.BooleanField(
        label='Aktiv struktura',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Struktura
        fields = ['name', 'role', 'is_active']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        role = cleaned_data.get("role")

        if not name or not role:
            raise forms.ValidationError("Barcha maydonlar to'ldirilishi shart!")

        return cleaned_data
    
class StrukturaUpdateForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Struktura nomini kiriting'}),
        label="Struktura nomi"
    )
    role = forms.ChoiceField(
        choices=RoleChoice.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Lavozim/Rol"
    )
    is_active = forms.BooleanField(
        label='Aktiv struktura',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Struktura
        fields = ['name', 'role', 'is_active']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        role = cleaned_data.get("role")

        if not name or not role:
            raise forms.ValidationError("Barcha maydonlar to'ldirilishi shart!")

        return cleaned_data
