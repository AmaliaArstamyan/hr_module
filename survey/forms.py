from django import forms
from django.contrib.auth.models import User

ROLE_CHOICES = [
    ('HR', 'HR'),
    ('TeamLead', 'Team Lead'),
    ('Employee', 'Employee'),
]

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Role")

    class Meta:
        model = User
        fields = ['username', 'email', 'role']

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
