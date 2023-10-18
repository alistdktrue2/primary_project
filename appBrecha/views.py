from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import ContactForm
from .models import Contact
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import HttpResponseRedirect
from urllib.parse import urlencode

def home_view(request):
    return render(request, 'index.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')


def register_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['password_confirmation']:
                try:
                    # Create contact
                    contact = Contact(
                        full_name=form.cleaned_data['full_name'],
                        email=form.cleaned_data['email'],
                        phone=form.cleaned_data['phone'],
                        password=form.cleaned_data['password'],
                        password_confirmation=form.cleaned_data['password_confirmation'],
                        plan=form.cleaned_data['plan'],
                    )
                    contact.save()

                    # Register user
                    user = get_user_model().objects.create_user(username=contact.email, password=contact.password)

                    # Assign contact to user
                    contact.user = user
                    contact.save()

                    # Log in user
                    login(request, user)
                    return redirect('dashboard_view')
                except Exception as e:
                    error_message=e
                    if error_message:
                        error_message_encoded = urlencode({'error': error_message})
                        redirect_url = reverse('home_view') + '?' + error_message_encoded
                        return HttpResponseRedirect(redirect_url)
                    else:
                        return redirect('home_view')  # Redirigir a la página de registro
            else:
                execute_script = True
                return redirect('/', error='Passwords do not match')
        else:
            execute_script = True
            print(form.errors)
            return redirect('home_view', error=form.errors)
    else:
        form = ContactForm()
        return render(request, 'index.html', {'form': form})



@login_required
def signout(request):
	logout(request)
	return redirect('home')




def login_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)


        if user is not None:
            login(request, user)
            return redirect('dashboard_view')
        else:
            # Agrega una variable de contexto para indicar si se debe ejecutar el script
            execute_script_login = True
            return render(request, 'index.html', {
                'form': form,
                'error': 'Username or password is incorrect',
                'execute_script': execute_script_login
            })

    return render(request, 'index.html', {'form': form})
        