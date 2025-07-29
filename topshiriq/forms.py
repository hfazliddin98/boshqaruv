from django import forms
from topshiriq.models import RektorToposhiriq


class RektorToposhiriqForm(forms.ModelForm):
    class Meta:
        model = RektorToposhiriq
        fields = ['title', 'body', 'status', 'xolat', 'izoh']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4}),
        }

    # Fayllarni formga qo‘shamiz (modelga emas!)
    files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False,
        label="Fayllar"
    )
