def obtener_empresa(request):
    return request.user.empresa_usuario.empresa