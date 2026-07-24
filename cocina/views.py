from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def panel_cocina(request):

    return render(
        request,
        "cocina/panel.html"
    )