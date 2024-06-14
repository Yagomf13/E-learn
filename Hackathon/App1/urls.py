from django.urls import path
from App1.views import IndexView, LoginView, RegisterView, cursos_view, crear_usuario, UserView, LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', IndexView),
    path('login/', LoginView, name='login'),
    path('register/' , RegisterView, name='register'),
    path('cursos/', cursos_view, name='cursos'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('crear_usuario/', crear_usuario, name='crear_usuario'),
    path('user/', UserView, name='user'),
    path('logout/', LogoutView, name='logout'),
]