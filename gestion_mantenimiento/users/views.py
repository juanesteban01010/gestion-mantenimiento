from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('custom_login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def custom_login(request):
    # Maps each account type to the required group name
    TIPO_CUENTA_GROUP = {
        'jefe_de_area': 'Admin',
        'administrador': 'Cliente',
        'tecnico': 'Tecnico',
    }

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            tipo_cuenta = form.cleaned_data.get('tipo_cuenta')
            co = form.cleaned_data.get('co')

            # Superusers bypass group validation and can log in with any account type
            required_group = TIPO_CUENTA_GROUP.get(tipo_cuenta)
            if not user.is_superuser and required_group and not user.groups.filter(name=required_group).exists():
                form.add_error(
                    'tipo_cuenta',
                    f'Tu usuario no pertenece al grupo requerido para este tipo de cuenta ({required_group}).',
                )
            else:
                auth_login(request, user)
                request.session['tipo_cuenta'] = tipo_cuenta
                request.session['co'] = co
                return redirect('dashboard')  # Redirige a la página de inicio después del inicio de sesión
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('custom_login')

def group_required(*group_names):
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)

@group_required('Admin')
def admin_view(request):
    return render(request, 'users/admin_view.html')
