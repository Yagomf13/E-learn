import re
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Curso
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Curso, Usuarios
from django.contrib.auth.models import User
from datetime import datetime, timedelta

def IndexView(request):
    """Página de inicio"""
    cursos = Curso.objects.all() if request.user.is_authenticated else []
    user = request.user if request.user.is_authenticated else None
    usuario = None

    if user:
        try:
            usuario = user.usuarios  # Intenta acceder al objeto Usuarios asociado al User
        except Usuarios.DoesNotExist:
            print("No existe un objeto Usuarios asociado a este usuario")

    context = {'cursos': cursos, 'user': user, 'usuario': usuario}
    return render(request, "index.html", context=context)


# def LoginView(request):
    """Página de login"""
    # return render(request, "login.html")

# Ejemplo de vista de login personalizada
def LoginView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        contraseña = request.POST.get('password')
        print(email, contraseña)
        user = authenticate(request, username=email, password=contraseña)
        if user is not None:
            login(request, user)
            return redirect('/')  # Redirige a la página principal después del login exitoso
        else:
            # Manejar caso de login fallido
            # Puedes mostrar un mensaje de error o redirigir de nuevo al login
            return render(request, 'login.html', {'error_message': 'Credenciales inválidas.'})
    
    # Si el método no es POST, renderiza el formulario de login vacío
    return render(request, 'login.html')

def RegisterView(request):
    """Página de register"""
    return render(request, "register.html")

def crear_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        contraseña = request.POST.get('contraseña')
        birthday = request.POST.get('birthday')
        
        # Verifica si ya existe un usuario con el mismo email
        if User.objects.filter(username=email).exists():
            messages.error(request, 'El correo ya se esta utilizando.')
            return render(request, 'register.html', {'email_error': 'El usuario ya existe.', 'nombre': nombre, 'apellido': apellido, 'email': email, 'birthday': birthday})
        
        for field_name, field_value in [('nombre', nombre), ('apellido', apellido)]:
            if not field_value or not re.match(r'^[a-zA-Z áéíóúùìòàè]+$', field_value):
                messages.error(request, f'El {field_name} solo debe contener letras.')
                return render(request, 'register.html', {'form_error': f'El {field_name} solo debe contener letras.', 'nombre': nombre, 'apellido': apellido, 'email': email, 'birthday': birthday})
        
        try:
            birth_date = datetime.strptime(birthday, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Formato de fecha inválido.')
            return render(request, 'register.html', {'form_error': 'Formato de fecha inválido.', 'nombre': nombre, 'apellido': apellido, 'email': email, 'birthday': birthday})
        
        # Valida que la fecha de nacimiento sea anterior al día actual y menor de 120 años en el pasado
        today = datetime.now().date()
        max_birth_date = today - timedelta(days=365 * 120)
        
        if birth_date >= today:
            messages.error(request, 'La fecha de nacimiento debe ser anterior al día actual.')
            return render(request, 'register.html', {'form_error': 'La fecha de nacimiento debe ser anterior al día actual.', 'nombre': nombre, 'apellido': apellido, 'email': email, 'birthday': birthday})

        if birth_date <= max_birth_date:
            messages.error(request, 'La fecha de nacimiento debe ser menor de 120 años en el pasado.')
            return render(request, 'register.html', {'form_error': 'La fecha de nacimiento debe ser menor de 120 años en el pasado.', 'nombre': nombre, 'apellido': apellido, 'email': email, 'birthday': birthday})

        # Validación de contraseña segura
        if len(contraseña) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return render(request, 'register.html', {'form_error': 'La contraseña debe tener al menos 8 caracteres.', 'nombre': nombre, 'apellido': apellido, 'email': email, 'birthday': birthday})

        if not re.search(r'[A-Z]', contraseña):
            messages.error(request, 'La contraseña debe contener al menos una letra mayúscula.')
            return render(request, 'register.html', {'form_error': 'La contraseña debe contener al menos una letra mayúscula.', 'nombre': nombre, 'apellido': apellido, 'email': email, 'birthday': birthday})

        if not re.search(r'[a-z]', contraseña):
            messages.error(request, 'La contraseña debe contener al menos una letra minúscula.')
            return render(request, 'register.html', {'form_error': 'La contraseña debe contener al menos una letra minúscula.', 'nombre': nombre, 'apellido': apellido, 'email': email, 'birthday': birthday})

        if not re.search(r'\d', contraseña):
            messages.error(request, 'La contraseña debe contener al menos un número.')
            return render(request, 'register.html', {'form_error': 'La contraseña debe contener al menos un número.', 'nombre': nombre, 'apellido': apellido, 'email': email, 'birthday': birthday})

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', contraseña):
            messages.error(request, 'La contraseña debe contener al menos un caracter especial (!@#$%^&*(),.?":{}|<>).')
            return render(request, 'register.html', {'form_error': 'La contraseña debe contener al menos un caracter especial.', 'nombre': nombre, 'apellido': apellido, 'email': email, 'birthday': birthday})
   
        # Crea un usuario en el modelo de usuario de Django
        user = User.objects.create_user(username=email, email=email, password=contraseña)
        
        # Crea una instancia de Usuarios asociada a este usuario
        usuario = Usuarios(user=user, nombre=nombre, apellido=apellido, email=email, contraseña=contraseña, birthday=birth_date)
        
        usuario.save()  # Guarda el usuario en la base de datos

        # Autentica al usuario recién creado y realiza el login
        user = authenticate(username=email, password=contraseña)
        if user is not None:
            login(request, user)
            
            # Agrega el mensaje de éxito
            messages.success(request, 'Usuario registrado y logeado exitosamente.')

            # Redirige a la página principal
            return redirect('/')

    # Si el método no es POST, renderiza el formulario vacío
    return render(request, 'register.html')

@login_required
def cursos_view(request):
    cursos = Curso.objects.all()
    return render(request, 'cursos.html', {'cursos': cursos})

def UserView(request):
    """Página de user"""
    user = request.user if request.user.is_authenticated else None
    usuario = None

    if user:
        try:
            usuario = user.usuarios  # Intenta acceder al objeto Usuarios asociado al User
        except Usuarios.DoesNotExist:
            print("No existe un objeto Usuarios asociado a este usuario")

    context = {'user': user, 'usuario': usuario}
    return render(request, "user.html", context=context)

def LogoutView(request):
    logout(request)
    return redirect('/')