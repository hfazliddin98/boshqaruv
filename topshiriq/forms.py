# from django import forms
# from topshiriq.models import (
#     RektorTopshiriq, ProrektorBolimTopshiriq, ProrektorDekanTopshiriq,
#     RektorTopshiriqJavob, RektorTopshiriqJavobFile
# )

# # Rektor topshiriqlari
# class RektorTopshiriqCreateForm(forms.ModelForm):
#     class Meta:
#         model = RektorTopshiriq
#         fields = ['bajaruvchi_user', 'title', 'body', 'xolat', 'boshlanish_vaqti', 'tugash_vaqti', 'izoh']
#         widgets = {
#             'bajaruvchi_user': forms.Select(attrs={'class': 'form-control'}),
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
#             'xolat': forms.Select(attrs={'class': 'form-control'}),
#             'boshlanish_vaqti': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
#             'tugash_vaqti': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
#             'izoh': forms.Textarea(attrs={'class': 'form-control'}),
#         }

# class RektorTopshiriqUpdateForm(forms.ModelForm):
#     class Meta:
#         model = RektorTopshiriq
#         fields = ['bajaruvchi_user', 'title', 'body', 'xolat', 'boshlanish_vaqti', 'tugash_vaqti', 'izoh']
#         widgets = {
#             'bajaruvchi_user': forms.Select(attrs={'class': 'form-control'}),
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
#             'xolat': forms.Select(attrs={'class': 'form-control'}),
#             'boshlanish_vaqti': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
#             'tugash_vaqti': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
#             'izoh': forms.Textarea(attrs={'class': 'form-control'}),
#         }

# # Prorektor bo‘lim topshiriqlari
# class ProrektorBolimTopshiriqForm(forms.ModelForm):
#     class Meta:
#         model = ProrektorBolimTopshiriq
#         fields = ['bajaruvchi_user', 'title', 'body', 'xolat', 'boshlanish_vaqti', 'tugash_vaqti', 'izoh']
#         widgets = {
#             'bajaruvchi_user': forms.Select(attrs={'class': 'form-control'}),
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
#             'xolat': forms.Select(attrs={'class': 'form-control'}),
#             'boshlanish_vaqti': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
#             'tugash_vaqti': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
#             'izoh': forms.Textarea(attrs={'class': 'form-control'}),
#         }

# # Prorektor dekan topshiriqlari
# class ProrektorDekanTopshiriqForm(forms.ModelForm):
#     class Meta:
#         model = ProrektorDekanTopshiriq
#         fields = ['bajaruvchi_user', 'title', 'body', 'xolat', 'boshlanish_vaqti', 'tugash_vaqti', 'izoh']
#         widgets = {
#             'bajaruvchi_user': forms.Select(attrs={'class': 'form-control'}),
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
#             'xolat': forms.Select(attrs={'class': 'form-control'}),
#             'boshlanish_vaqti': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
#             'tugash_vaqti': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
#             'izoh': forms.Textarea(attrs={'class': 'form-control'}),
#         }

# class RektorTopshiriqJavobForm(forms.ModelForm):
#     class Meta:
#         model = RektorTopshiriqJavob
#         fields = ['title', 'body']  # yoki faqat ['body'] agar sarlavha kerak bo'lmasa
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Javob sarlavhasi"}),
#             'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': "Javob matni"}),
#         }

