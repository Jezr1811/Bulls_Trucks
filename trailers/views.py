from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Trailer
from .forms import TrailerForm


@login_required
def lista_trailers(request):

    trailers = Trailer.objects.all()

    return render(
        request,
        "trailers/lista.html",
        {
            "trailers": trailers
        }
    )


@login_required
def crear_trailer(request):

    if request.method == "POST":

        form = TrailerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("trailers:lista_trailers")

    else:

        form = TrailerForm()

    return render(
        request,
        "trailers/formulario.html",
        {
            "form": form
        }
    )


@login_required
def editar_trailer(request, pk):

    trailer = get_object_or_404(Trailer, pk=pk)

    if request.method == "POST":

        form = TrailerForm(
            request.POST,
            instance=trailer
        )

        if form.is_valid():
            form.save()
            return redirect("trailers:lista_trailers")

    else:

        form = TrailerForm(instance=trailer)

    return render(
        request,
        "trailers/formulario.html",
        {
            "form": form
        }
    )


@login_required
def eliminar_trailer(request, pk):

    trailer = get_object_or_404(Trailer, pk=pk)

    if request.method == "POST":

        trailer.delete()
        return redirect("trailers:lista_trailers")

    return render(
        request,
        "trailers/eliminar.html",
        {
            "trailer": trailer
        }
    )
