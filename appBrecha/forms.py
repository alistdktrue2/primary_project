from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import UserCreationForm
from .models import Contact

class ContactForm(forms.ModelForm):
    phone = PhoneNumberField(region="PE")
    password_confirmation = forms.CharField(max_length=128, widget=forms.PasswordInput())

    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'phone', 'password', 'password_confirmation']

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password_confirmation

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Contact.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

