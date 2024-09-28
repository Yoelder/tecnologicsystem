"""cargas_fisicas URL Configuration


"""
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from app_principal.views import home,multimedia,formulario,saberes,registro_usuario,administrar,trazas,resumen,evaluar,ayuda,\
formulario2,lista_usuarios,agregar_usuario,usuarios_grafico,editar_usuario,eliminar_usuario,formulas,formulario4,formulario3,chat,formulariogm,enviar_correo,editar_evaluacion
    
from django.shortcuts import render

from django.urls import path
from app_principal.views import exportar_evaluaciones,guardar_datos_completos,eliminar_estudiante_ajax,listar_evaluaciones,detalles_estudiante


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),# url login
    path('home/',(home) , name='login'),# principal
    path('multimedia/',(multimedia) , name='multimedia'),# muestra de ejecicios
    path('formulario/',(formulario) , name='formulario'),# 
    path('saberes/',(saberes) , name='saberes'),# saberes
    path('formulario2/',(formulario2) , name='formulario2'),# 
    path('formulario3/',(formulario3) , name='formulario3'),# 
    path('formulario4/',(formulario4) , name='formulario4'),# 

    path('resumen/',(resumen) , name='resumen'),#Formulario resumen
    path('evaluar/',(evaluar) , name='evaluar'),#Evaluar
    path('chat/',(chat) , name='chat'),#url chat con IA
    path("formulariogm/contactar/",(enviar_correo),name='contactar'),#url de contacto correo
    path("formulariogm/",(formulariogm),name='formulariogm'),#url de contacto correo
    path("formulas/",(formulas),name='formulas'),
    
    path('logout/', LogoutView.as_view(next_page='/login'), name='logout'),  # URL para cerrar sesión
    path('usuarios/registro/', (registro_usuario), name='registro'),  # URL para el registro
    path('usuarios/', (lista_usuarios), name='lista_usuarios'),
    path('usuarios/agregar/', (agregar_usuario), name='agregar_usuario'),
    path('usuarios/editar/<int:usuario_id>/', (editar_usuario), name='editar_usuario'),
    path('usuarios/eliminar/<int:usuario_id>/',(eliminar_usuario), name='eliminar_usuario'),

    path('administrar/', (administrar), name='administrar'),  # Panel de administracion personalizado 
    path('trazas/', (trazas), name='trazas'),  # Administracion de trazas 
    path('guardar-datos/', (guardar_datos_completos), name='guardar_datos_completos'),
    path('evaluaciones/', (listar_evaluaciones), name='listar_evaluaciones'),
    path('estudiante/<int:estudiante_id>/', (detalles_estudiante), name='detalles_estudiante'),
    path('estudiante/eliminar/<int:estudiante_id>/', (eliminar_estudiante_ajax), name='eliminar_estudiante'),  # Endpoint para eliminación vía AJAX
    path('exportar_evaluaciones/', (exportar_evaluaciones), name='exportar_evaluaciones'),
    path('usuarios-grafico/', (usuarios_grafico), name='usuarios_grafico'),
    path('evaluacion/editar/<int:evaluacion_id>/',(editar_evaluacion), name='editar_evaluacion'),
    path('ayuda/', (ayuda), name='ayuda')
   ]

