from django.shortcuts import render, redirect, get_object_or_404
from .models import Documento
from .forms import DocumentoForm
from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def lista_documentos(request):
    # --- CAPA DE FILTRADO MULTIUSUARIO ---
    if request.user.is_superuser:
        # El administrador ve absolutamente todo
        documentos = Documento.objects.all().order_by("-id")
    elif hasattr(request.user, 'conductor'):
        # El conductor solo ve sus documentos personales
        documentos = Documento.objects.filter(conductor=request.user.conductor).order_by("-id")
    else:
        # Por si existe un usuario que no sea ni admin ni conductor (seguridad extra)
        documentos = Documento.objects.none()

    hoy = date.today()

    for documento in documentos:
        if documento.fecha_vencimiento:
            dias = (documento.fecha_vencimiento - hoy).days
            documento.dias_restantes = dias

            if dias < 0:
                documento.estado = "vencido"
            elif dias <= 7:
                documento.estado = "vencido"  # O "proximo" según tu regla de negocio
            elif dias <= 30:
                documento.estado = "proximo"
            else:
                documento.estado = "vigente"
        else:
            documento.estado = "sin_fecha"
            documento.dias_restantes = None

    return render(
        request,
        "documentos/lista.html",
        {
            "documentos": documentos
        }
    )

@login_required
def crear_documento(request):
    if request.method == "POST":
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            # --- ASIGNACIÓN AUTOMÁTICA DE CONDUCTOR ---
            documento = form.save(commit=False)
            if not request.user.is_superuser:
                # Si es un conductor, el sistema le asigna su propio perfil sin preguntar
                documento.conductor = request.user.conductor
            documento.save()
            return redirect("documentos:lista_documentos")
    else:
        form = DocumentoForm()

    return render(
        request,
        "documentos/formulario.html",
        {
            "form": form,
            "titulo": "Registrar Nuevo Documento"
        }
    )

@login_required
def editar_documento(request, pk):
    # --- CAPA DE SEGURIDAD EN URL ---
    # Evita que un conductor edite un documento de otro cambiando la ID en la URL
    if request.user.is_superuser:
        documento = get_object_or_404(Documento, pk=pk)
    else:
        documento = get_object_or_404(Documento, pk=pk, conductor=request.user.conductor)

    if request.method == "POST":
        form = DocumentoForm(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            form.save()
            return redirect("documentos:lista_documentos")
    else:
        form = DocumentoForm(instance=documento)

    return render(
        request,
        "documentos/formulario.html",
        {
            "form": form,
            "documento": documento,
            "titulo": "Editar Documento"
        }
    )

@login_required
def renovar_documento(request, pk):
    # --- CAPA DE SEGURIDAD EN URL ---
    if request.user.is_superuser:
        documento = get_object_or_404(Documento, pk=pk)
    else:
        documento = get_object_or_404(Documento, pk=pk, conductor=request.user.conductor)

    if request.method == "POST":
        documento.fecha_vencimiento = request.POST.get("fecha_vencimiento")

        if request.FILES.get("imagen"):
            documento.imagen = request.FILES["imagen"]

        if request.FILES.get("pdf"):
            documento.pdf = request.FILES["pdf"]

        documento.save()
        messages.success(request, "Documento renovado correctamente.")
        return redirect("documentos:lista_documentos")

    return render(
        request,
        "documentos/renovar.html",
        {
            "documento": documento
        }
    )

@login_required
def eliminar_documento(request, pk):
    # --- CAPA DE SEGURIDAD EN URL ---
    if request.user.is_superuser:
        documento = get_object_or_404(Documento, pk=pk)
    else:
        documento = get_object_or_404(Documento, pk=pk, conductor=request.user.conductor)

    if request.method == "POST":
        documento.delete()
        return redirect("documentos:lista_documentos")

    return render(
        request,
        "documentos/eliminar.html",
        {
            "documento": documento
        }
    )