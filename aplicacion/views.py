from django.shortcuts import render, redirect
from django.core import serializers
import json
from microsoft_authentication.auth.auth_decorators import microsoft_login_required
from django.views.generic import TemplateView
import requests
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from django.http import HttpResponseRedirect
from .models import Director
import xlsxwriter
from django.http import HttpResponse

# Create your views here.
def home(request):
    if "token_cache" not in request.session.keys():
        return render(request, "aplicacion/index.html")
    else:
        return redirect("formulario")

@microsoft_login_required()
def formulario(request):
    complete_session(request=request)
    usuario_nivel = request.session['user_data']['NIVEL_DESC']
    if usuario_nivel == 'DOCENTE':
        return redirect('docente')
    else:
        if usuario_nivel == 'DIRECTOR':
            return redirect('director')
        else:
            return redirect('microsoft_authentication/logout/')

@microsoft_login_required()
def hello(request):
    complete_session(request=request)
    return render(request, "aplicacion/hello.html", {
        'data': request.session["user_data"]
    })

@microsoft_login_required()
def docente(request):
    if is_docente(request):
        return render(request, "aplicacion/docente.html",{
            "nombre_usuario": request.session["user_data"]["NOMBRE_USUARIO"],
            "cedula_usuario": request.session["user_data"]["CEDULA_USUARIO"],
            "correo_usuario": request.session["user_data"]["CORREO_USUARIO"],
        })
    else:
        redirect('formulario')

@microsoft_login_required()
def director(request):
    if is_director(request):
        return render(request, "aplicacion/director.html",{
            "nombre_usuario": request.session["user_data"]["NOMBRE_USUARIO"],
            "cedula_usuario": request.session["user_data"]["CEDULA_USUARIO"],
            "correo_usuario": request.session["user_data"]["CORREO_USUARIO"],
            "cod_siace": request.session["user_data"]["COD_SIACE"],
            "nombre_escuela": request.session["user_data"]["NOMBRE_ESCUELA"],
            "distrito": request.session["user_data"]["DISTRITO"],
            "provincia": request.session["user_data"]["PROVINCIA"],
            "corregimiento": request.session["user_data"]["CORREGIMIENTO"],
            "latitud_longitud": request.session["user_data"]["LATITUD_LONGITUD"],
            "nivel": request.session["user_data"]["Nivel"][0]["Nivel_educativo"],
        })
    else:
        return redirect('formulario')

def director_bd(request):
    contexto = {'director': Director.objects.all()}
    return render(request, "aplicacion/director_bd.html", contexto)

def export_director(request):
    # Obtener los datos para exportar
    director = Director.objects.all()

    # Crear un nuevo libro de trabajo de Excel
    workbook = xlsxwriter.Workbook('formulario_director.xlsx')
    worksheet = workbook.add_worksheet()

    # Escribir los encabezados de las columnas
    headers = [
        'Nombre', 'Apellido', 'Cédula', 'Teléfono Oficina', 'Teléfono Personal',
        'Correo Institucional', 'Correo Personal 1', 'Correo Personal 2', 'Código SIACE',
        'Nombre Centro Educativo', 'Región Educativa', 'Provincia', 'Dirección',
        'Nivel Escolar', 'Matrícula Total', 'Grado 1', 'Femenino 1', 'Masculino 1',
        'Grado 2', 'Femenino 2', 'Masculino 2', 'Grado 3', 'Femenino 3', 'Masculino 3',
        'Grado 4', 'Femenino 4', 'Masculino 4', 'Total Docentes', 'Docentes 1', 'Docentes 2',
        'Docentes 3', 'Docentes 4', 'Estudiantes Salón', 'Docentes Asignatura',
        'Participa PPB', 'Estudiantes Nivel PPB', 'Docentes Capacitados PPB',
        'Docentes Aprobados PPB', 'Docentes Capacitación Exterior', 'Códigos Plan Estudio',
        'Planes Estudio', 'Asignaturas Inglés Plan Estudios', 'Asignaturas Inglés Dictadas',
        'Planes Clase', 'Horas Inglés', 'Horas Teóricas', 'Horas Prácticas',
        'Actividades Propio Centro', 'Actividades MEDUCA Centro', 'Actividades Externas Centro',
        'Detalle Actividades Anual', 'Cantidad Estudiantes Actividades Externas 1',
        'Cantidad Estudiantes Actividades Externas 2', 'Cantidad Estudiantes Actividades Externas 3',
        'Cantidad Estudiantes Actividades Externas 4', 'After School Existencia',
        'After School Descripción', 'After School Participación 1', 'After School Participación 2',
        'After School Participación 3', 'After School Participación 4', 'After School Recursos'
    ]
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    # Escribir los datos de los directores en el archivo Excel
    for row, d in enumerate(director):
        worksheet.write(row + 1, 0, d.nombre)
        worksheet.write(row + 1, 1, d.apellido)
        worksheet.write(row + 1, 2, d.cedula)
        worksheet.write(row + 1, 3, d.telefono_oficina)
        worksheet.write(row + 1, 4, d.telefono_personal)
        worksheet.write(row + 1, 5, d.correo_institucional)
        worksheet.write(row + 1, 6, d.correo_personal1)
        worksheet.write(row + 1, 7, d.correo_personal2)
        worksheet.write(row + 1, 8, d.codigo_siace)
        worksheet.write(row + 1, 9, d.nombre_centro_educativo)
        worksheet.write(row + 1, 10, d.region_educativa)
        worksheet.write(row + 1, 11, d.provincia)
        worksheet.write(row + 1, 12, d.direccion)
        worksheet.write(row + 1, 13, d.nivel_escolar)
        worksheet.write(row + 1, 14, d.matricula_total)
        worksheet.write(row + 1, 15, d.grado1)
        worksheet.write(row + 1, 16, d.femenino1)
        worksheet.write(row + 1, 17, d.masculino1)
        worksheet.write(row + 1, 18, d.grado2)
        worksheet.write(row + 1, 19, d.femenino2)
        worksheet.write(row + 1, 20, d.masculino2)
        worksheet.write(row + 1, 21, d.grado3)
        worksheet.write(row + 1, 22, d.femenino3)
        worksheet.write(row + 1, 23, d.masculino3)
        worksheet.write(row + 1, 24, d.grado4)
        worksheet.write(row + 1, 25, d.femenino4)
        worksheet.write(row + 1, 26, d.masculino4)
        worksheet.write(row + 1, 27, d.total_docentes)
        worksheet.write(row + 1, 28, d.docentes1)
        worksheet.write(row + 1, 29, d.docentes2)
        worksheet.write(row + 1, 30, d.docentes3)
        worksheet.write(row + 1, 31, d.docentes4)
        worksheet.write(row + 1, 32, d.estudiantes_salon)
        worksheet.write(row + 1, 33, d.docentes_asignatura)
        worksheet.write(row + 1, 34, d.participa_ppb)
        worksheet.write(row + 1, 35, d.estudiantes_nivel_ppb)
        worksheet.write(row + 1, 36, d.docentes_capacitados_ppb)
        worksheet.write(row + 1, 37, d.docentes_aprobados_ppb)
        worksheet.write(row + 1, 38, d.docentes_capacitacion_exterior)
        worksheet.write(row + 1, 39, d.codigos_plan_estudio)
        worksheet.write(row + 1, 40, d.planes_estudio)
        worksheet.write(row + 1, 41, d.asignaturas_ingles_plan_estudios)
        worksheet.write(row + 1, 42, d.asignaturas_ingles_dictadas)
        worksheet.write(row + 1, 43, d.planes_clase)
        worksheet.write(row + 1, 44, d.horas_ingles)
        worksheet.write(row + 1, 45, d.horas_teoricas)
        worksheet.write(row + 1, 46, d.horas_practicas)
        worksheet.write(row + 1, 47, d.actividades_propio_centro)
        worksheet.write(row + 1, 48, d.actividades_meduca_centro)
        worksheet.write(row + 1, 49, d.actividades_externas_centro)
        worksheet.write(row + 1, 50, d.detalle_actividades_anual)
        worksheet.write(row + 1, 51, d.cantidad_estudiantes_actividades_externas_1)
        worksheet.write(row + 1, 52, d.cantidad_estudiantes_actividades_externas_2)
        worksheet.write(row + 1, 53, d.cantidad_estudiantes_actividades_externas_3)
        worksheet.write(row + 1, 54, d.cantidad_estudiantes_actividades_externas_4)
        worksheet.write(row + 1, 55, d.after_school_existencia)
        worksheet.write(row + 1, 56, d.after_school_descripcion)
        worksheet.write(row + 1, 57, d.after_school_participacion_1)
        worksheet.write(row + 1, 58, d.after_school_participacion_2)
        worksheet.write(row + 1, 59, d.after_school_participacion_3)
        worksheet.write(row + 1, 60, d.after_school_participacion_4)
        worksheet.write(row + 1, 61, d.after_school_recursos)

    # Cerrar el libro de trabajo
    workbook.close()

    # Devolver el archivo Excel como respuesta HTTP para descargar
    with open('formulario_director.xlsx', 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="formulario_director.xlsx"'
    return response

def form_director(request):
    if request.method == 'POST':
        # Procesar el formulario enviado
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        cedula = request.POST.get('cedula')
        telefono_oficina = request.POST.get('telefono_oficina')
        telefono_personal = request.POST.get('telefono_personal')
        correo_institucional = request.POST.get('correo_institucional')
        correo_personal1 = request.POST.get('correo_personal1')
        correo_personal2 = request.POST.get('correo_personal2')
        codigo_siace = request.POST.get('codigo_siace')
        nombre_centro_educativo = request.POST.get('nombre_centro_educativo')
        region_educativa = request.POST.get('region_educativa')
        provincia = request.POST.get('provincia')
        direccion = request.POST.get('direccion')
        nivel_escolar = request.POST.get('nivel_escolar')
        matricula_total = request.POST.get('matricula_total')
        grado1 = request.POST.get('grado1')
        femenino1 = request.POST.get('femenino1')
        masculino1 = request.POST.get('masculino1')
        grado2 = request.POST.get('grado2')
        femenino2 = request.POST.get('femenino2')
        masculino2 = request.POST.get('masculino2')
        grado3 = request.POST.get('grado3')
        femenino3 = request.POST.get('femenino3')
        masculino3 = request.POST.get('masculino3')
        grado4 = request.POST.get('grado4')
        femenino4 = request.POST.get('femenino4')
        masculino4 = request.POST.get('masculino4')
        total_docentes = request.POST.get('total_docentes')
        docentes1 = request.POST.get('docentes1')
        docentes2 = request.POST.get('docentes2')
        docentes3 = request.POST.get('docentes3')
        docentes4 = request.POST.get('docentes4')
        estudiantes_salon = request.POST.get('estudiantes_salon')
        docentes_asignatura = request.POST.get('docentes_asignatura')
        participa_ppb = request.POST.get('participa_ppb')
        estudiantes_nivel_ppb = request.POST.get('estudiantes_nivel_ppb')
        docentes_capacitados_ppb = request.POST.get('docentes_capacitados_ppb')
        docentes_aprobados_ppb = request.POST.get('docentes_aprobados_ppb')
        docentes_capacitacion_exterior = request.POST.get('docentes_capacitacion_exterior')
        codigos_plan_estudio = request.POST.get('codigos_plan_estudio')
        planes_estudio = request.POST.get('planes_estudio')
        asignaturas_ingles_plan_estudios = request.POST.get('asignaturas_ingles_plan_estudios')
        asignaturas_ingles_dictadas = request.POST.get('asignaturas_ingles_dictadas')
        planes_clase = request.POST.get('planes_clase')
        horas_ingles = request.POST.get('horas_ingles')
        horas_teoricas = request.POST.get('horas_teoricas')
        horas_practicas = request.POST.get('horas_practicas')
        actividades_propio_centro = request.POST.get('actividades_propio_centro')
        actividades_meduca_centro = request.POST.get('actividades_meduca_centro')
        actividades_externas_centro = request.POST.get('actividades_externas_centro')
        detalle_actividades_anual = request.POST.get('detalle_actividades_anual')
        cantidad_estudiantes_actividades_externas_1 = request.POST.get('cantidad_estudiantes_actividades_externas_1')
        cantidad_estudiantes_actividades_externas_2 = request.POST.get('cantidad_estudiantes_actividades_externas_2')
        cantidad_estudiantes_actividades_externas_3 = request.POST.get('cantidad_estudiantes_actividades_externas_3')
        cantidad_estudiantes_actividades_externas_4 = request.POST.get('cantidad_estudiantes_actividades_externas_4')
        after_school_existencia = request.POST.get('after_school_existencia')
        after_school_descripcion = request.POST.get('after_school_descripcion')
        after_school_participacion_1 = request.POST.get('after_school_participacion_1')
        after_school_participacion_2 = request.POST.get('after_school_participacion_2')
        after_school_participacion_3 = request.POST.get('after_school_participacion_3')
        after_school_participacion_4 = request.POST.get('after_school_participacion_4')
        after_school_recursos = request.POST.get('after_school_recursos')

        # Crear una instancia del modelo Director con los datos obtenidos
        director = Director(
            nombre=nombre,
            apellido=apellido,
            cedula=cedula,
            telefono_oficina=telefono_oficina,
            telefono_personal=telefono_personal,
            correo_institucional=correo_institucional,
            correo_personal1=correo_personal1,
            correo_personal2=correo_personal2,
            codigo_siace=codigo_siace,
            nombre_centro_educativo=nombre_centro_educativo,
            region_educativa=region_educativa,
            provincia=provincia,
            direccion=direccion,
            nivel_escolar=nivel_escolar,
            matricula_total=matricula_total,
            grado1=grado1,
            femenino1=femenino1,
            masculino1=masculino1,
            grado2=grado2,
            femenino2=femenino2,
            masculino2=masculino2,
            grado3=grado3,
            femenino3=femenino3,
            masculino3=masculino3,
            grado4=grado4,
            femenino4=femenino4,
            masculino4=masculino4,
            total_docentes=total_docentes,
            docentes1=docentes1,
            docentes2=docentes2,
            docentes3=docentes3,
            docentes4=docentes4,
            estudiantes_salon=estudiantes_salon,
            docentes_asignatura=docentes_asignatura,
            participa_ppb=participa_ppb,
            estudiantes_nivel_ppb=estudiantes_nivel_ppb,
            docentes_capacitados_ppb=docentes_capacitados_ppb,
            docentes_aprobados_ppb=docentes_aprobados_ppb,
            docentes_capacitacion_exterior=docentes_capacitacion_exterior,
            codigos_plan_estudio=codigos_plan_estudio,
            planes_estudio=planes_estudio,
            asignaturas_ingles_plan_estudios=asignaturas_ingles_plan_estudios,
            asignaturas_ingles_dictadas=asignaturas_ingles_dictadas,
            planes_clase=planes_clase,
            horas_ingles=horas_ingles,
            horas_teoricas=horas_teoricas,
            horas_practicas=horas_practicas,
            actividades_propio_centro=actividades_propio_centro,
            actividades_meduca_centro=actividades_meduca_centro,
            actividades_externas_centro=actividades_externas_centro,
            detalle_actividades_anual=detalle_actividades_anual,
            cantidad_estudiantes_actividades_externas_1=cantidad_estudiantes_actividades_externas_1,
            cantidad_estudiantes_actividades_externas_2=cantidad_estudiantes_actividades_externas_2,
            cantidad_estudiantes_actividades_externas_3=cantidad_estudiantes_actividades_externas_3,
            cantidad_estudiantes_actividades_externas_4=cantidad_estudiantes_actividades_externas_4,
            after_school_existencia=after_school_existencia,
            after_school_descripcion=after_school_descripcion,
            after_school_participacion_1=after_school_participacion_1,
            after_school_participacion_2=after_school_participacion_2,
            after_school_participacion_3=after_school_participacion_3,
            after_school_participacion_4=after_school_participacion_4,
            after_school_recursos=after_school_recursos
        )
        # Guardar el objeto Director en la base de datos
        director.save()

        # Redireccionar a alguna página o hacer alguna otra acción después de procesar el formulario
        return HttpResponseRedirect('/gracias/')

    # Si el método de solicitud es GET o el formulario no es válido, simplemente renderiza el formulario vacío
    return render(request, 'aplicacion/director.html')

@microsoft_login_required()
def coordinador_5(request):
    return render(request, "aplicacion/coordinador_5.html")

@microsoft_login_required()
def tecnologia_6(request):
    return render(request, "aplicacion/tecnologia_6.html")

@microsoft_login_required()
def otros_docentes_7(request):
    return render(request, "aplicacion/otros_docentes_7.html")

@microsoft_login_required()
def lengua_8(request):
    return render(request, "aplicacion/lengua_8.html")

@microsoft_login_required()
def ester_9(request):
    return render(request, "aplicacion/ESTER_9.html")

class logout_page(TemplateView):
    template_name = 'admin/logout.html'

def complete_session(request):
    if "user_data" not in request.session.keys():
        session_data = json.loads(request.session["token_cache"])
        access_token_dict = session_data["AccessToken"]
        account_dict = session_data["Account"]
        token_data_id = next(iter(access_token_dict))
        account_data_id = next(iter(account_dict))
        account = account_dict[account_data_id]["username"]
        access_token = access_token_dict[token_data_id]["secret"]

        url = f"https://formulario-api-aeekxgs7da-uc.a.run.app/api/user/{account}"
        headers = {'Authorization': access_token}
        response = requests.get(url, headers = headers)
        response_json = response.json()
        request.session["user_data"] = response_json
        
def is_docente(request):
    return request.session['user_data']['NIVEL_DESC'] == 'DOCENTE'

def is_director(request):
    return request.session['user_data']['NIVEL_DESC'] == 'DIRECTOR'
# def make_redirect(request):
#     sesion_data = serializers.deserialize('json', request.session["token_cache"])

# def request_user_data(token):
#     return token
class CreateUser(LoginRequiredMixin, CreateView):
    model = User
    fields = ['email', 'first_name', 'last_name', 'password']
    template_name = 'aplicacion/crear_user.html'
    success_url = reverse_lazy('user')

class UpdateUser(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['email', 'first_name', 'last_name', 'password']
    template_name = 'aplicacion/actualizar_user.html'
    success_url = reverse_lazy('user')

class DeleteUser(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'aplicacion/eliminar_user.html'
    success_url = reverse_lazy('user')

def user(request):
    users = User.objects.all()
    return render(request, 'admin/user.html', {'users': users})

def editar_user(request, pk):
    users = User.objects.all()
    return render(request, 'admin/editar_user.html', {'users': users})

def eliminar_user(request, pk):
    users = User.objects.all()
    return render(request, 'admin/eliminar_user.html', {'users': users})