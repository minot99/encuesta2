from django.urls import path, include
from .views import *
from . import views

urlpatterns = [
    path('', home, name="home"),
    path('formulario/', formulario, name="formulario"),
    path('microsoft_authentication/', include('microsoft_authentication.urls')),
    path('hello/', hello, name="hello"),
    path('docente/', docente, name="docente"),
    path('director/', director, name="director"),
    path('coordinador_5/', coordinador_5, name="coordinador_5"),
    path('tecnologia_6/', tecnologia_6, name="tecnologia_6"),
    path('otros_docentes_7/', otros_docentes_7, name="otros_docentes_7"),
    path('lengua_8/', lengua_8, name="lengua_8"),
    path('ester_9/', ester_9, name="ester_9"),
    path('user/', user, name="user"),
    path('editar_user/<int:pk>/', views.editar_user, name='editar_user'),
    path('eliminar_user/<int:pk>/', views.eliminar_user, name='eliminar_user'),
    path("__reload__/", include("django_browser_reload.urls")),
    path('logout/', views.logout_page.as_view(), name='logout-page'),
    path('form_director/', form_director, name='form_director'),
    path('director_bd/', director_bd, name='director_bd'),
    path('export_director/', export_director, name='export_director'),
    #path('form_docente/', form_docente, name='form_docente'),
    #path('docente_bd/', docente_bd, name='docente_bd'),
    #path('export_docente/', export_docente, name='export_docente'),
]