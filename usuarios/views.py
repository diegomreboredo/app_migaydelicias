from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)


class UsuarioLoginView(LoginView):
    template_name = "usuarios/login.html"


class UsuarioLogoutView(LogoutView):
    pass