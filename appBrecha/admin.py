
from django.contrib import admin
from .models import Contact
from django import forms


class ContactForm(forms.ModelForm):
    class Meta:
        widgets = {                       
            'phone': "phone",
        }

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    form = ContactForm