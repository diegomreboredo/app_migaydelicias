from django.db import models
from django.contrib.auth.models import User

from empresas.models import Empresa


class UsuarioEmpresa(models.Model):

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="empresa_usuario"
    )

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="usuarios"
    )

    class Meta:
        verbose_name = "Usuario Empresa"
        verbose_name_plural = "Usuarios Empresas"

    def __str__(self):
        return (
            f"{self.usuario.username} - "
            f"{self.empresa.nombre}"
        )