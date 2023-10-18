
from django.contrib import admin
from .models import Contact
from django import forms
from phonenumber_field.widgets import PhoneNumberPrefixWidget

class ContactForm(forms.ModelForm):
    class Meta:
        widgets = {                          # Here
            'phone': PhoneNumberPrefixWidget(initial='US'),
        }

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    form = ContactForm