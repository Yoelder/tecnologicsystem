
from django.shortcuts import render,redirect
from django.contrib.auth import logout ,login
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout ,login
from django.shortcuts import render
from django.http import JsonResponse

from django.contrib.auth.views import LoginView


from .decorators import admin_required,profesor_required

class CustomAdminLoginView(LoginView):
    template_name = 'registration/login.html'  # Define tu propia plantilla


#from app1.models import Curso
@login_required(login_url='/login/')
def home(request):
    # Obtener el usuario autenticado
    usuario = request.user

    # Pasar el usuario al contexto
    context = {
        'usuario': usuario
    }

    return render(request, 'home.html', context)

@login_required(login_url='/login/')
def multimedia(request):
    
    return render(request, 'multimedia2.html')
@login_required(login_url='/login/')
def formulario(request):
    
    return render(request, 'formulario_inicial.html')
@login_required(login_url='/login/')
def saberes(request):
    
    return render(request, 'saber2.html')
    #registro

@login_required(login_url='/login/')
def formulario2(request):
    
    return render(request, 'Formulario2.html')
@login_required(login_url='/login/')    
def formulario3(request):
        
    return render(request, 'Formulario3.html')

@login_required(login_url='/login/')
def formulario4(request):
        
    return render(request, 'formulario4.html')

@login_required(login_url='/login/')
def formulas(request):
        
    return render(request, 'calcular.html')    

@login_required(login_url='/login/')
def resumen(request):
    tipo_usuario = request.user.tipo_usuario
    context = {'tipo_usuario': tipo_usuario}
    return render(request, 'grafico_resumen.html',context) 

@login_required(login_url='/login/')
def evaluar(request):
        
    return render(request, 'evaluar.html')  
#para chat con IA

# Lista de claves API
API_KEY_LIST=[
'AIzaSyBQlSAqu8n9ncLLk83T76NO93RpzSw3LVc',
'AIzaSyAzyAwlNuh7LDBMwNNVIw7DSoth-iSzO4Q',
'AIzaSyCw_H0UyOTcOs2Al1wGpPzeqlrXf50Lmdo',
'AIzaSyC5BTO1i9PQMSE0zV0EDeivmooV40L9sDA',
'AIzaSyCvweiFctY0tJkHGfsUdMPoEVoQtVHb8Bg',
'AIzaSyACcyWgcrloI5nJ6p5NeiVT5j8xMOYgq5Y']

API_HOST = "generativelanguage.googleapis.com"
import http.client
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache  # Usar caché para almacenar el índice de la clave API



API_HOST = "generativelanguage.googleapis.com"

def chat(request):
    if request.method == "POST":
        user_message = request.POST.get("message")

        # Obtener el historial de la sesión o inicializarlo si no existe
        conversation_history = request.session.get('conversation_history', [])

        # Prompt inicial con restricciones y enfoque de conversación
        initial_prompt = """Eres un asistente que responde de manera directa y formal. 
                            Evita respuestas de contenido ofensivo o político. Solo responde 
                            lo relacionado con educación física y deporte."""

        # Agregar el prompt inicial al historial si es la primera interacción
        if not conversation_history:
            conversation_history.append({"text": initial_prompt})

        # Agregar el mensaje del usuario al historial
        conversation_history.append({"text": user_message})

        # Limitar el historial a las últimas 20 entradas (10 preguntas y 10 respuestas)
        if len(conversation_history) > 41:  # 1 entrada inicial + 20 pares de Q&A = 41
            conversation_history = conversation_history[-41:]

        # Configurar el cuerpo de la solicitud JSON con todo el historial de la conversación
        data = {
            "contents": [
                {
                    "parts": conversation_history
                }
            ]
        }

        headers = {
            'Content-Type': 'application/json'
        }

        # Obtener el índice de la clave API desde la caché, o iniciar en 0
        current_index = cache.get('api_key_index', 0)
        api_key = API_KEY_LIST[current_index]
        
        # Actualizar el índice para la próxima solicitud
        next_index = (current_index + 1) % len(API_KEY_LIST)
        cache.set('api_key_index', next_index)

        API_URL = f"/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

        # Establecer la conexión HTTP con el servidor
        conn = http.client.HTTPSConnection(API_HOST)

        # Convertir el diccionario de datos a JSON
        json_data = json.dumps(data)

        # Enviar la solicitud POST
        conn.request("POST", API_URL, body=json_data, headers=headers)

        # Obtener la respuesta
        response = conn.getresponse()
        response_data = response.read()
        conn.close()

        # Procesar la respuesta
        if response.status == 200:
            response_json = json.loads(response_data)
            if "candidates" in response_json and response_json["candidates"]:
                ai_response = response_json["candidates"][0]["content"]["parts"][0]["text"]
            else:
                ai_response = "Lo siento, no se pudo obtener una respuesta adecuada de la API."
        else:
            ai_response = f"Error: {response.status} - {response_data.decode('utf-8')}"

        # Agregar la respuesta de la IA al historial
        conversation_history.append({"text": ai_response})

        # Guardar el historial actualizado en la sesión
        request.session['conversation_history'] = conversation_history

        return JsonResponse({"response": ai_response.replace('*', ' ')})

    return render(request, "chat.html")


from django.core.mail import send_mail
from django.http import HttpResponse

@login_required(login_url='/login/')
def enviar_correo(request):
    #print(request.POST)
    if request.method == 'POST':
        asunto = request.POST['txtAsunto']
        mail=request.POST['txtEmail']
        mensaje = request.POST['txtMensaje']+"\ncorreo: "+mail
        # Dirección de correo electrónico desde la que se enviará el correo
        correo_desde = 'tecnologicsystemnew@gmail.com'

        # Lista de destinatarios
        destinatarios = ['yoelder996@gmail.com']

        # Enviar correo
        send_mail(asunto, mensaje, correo_desde, destinatarios,fail_silently=False)
        messages.success(request, 'Tu mensaje ha sido enviado con éxito. ¡Gracias!')
        # Puedes redirigir a una página de éxito o realizar otras acciones después de enviar el correo
        return redirect('formulariogm')
    #print(request.method)
    return HttpResponse(request,'Error.')
@login_required(login_url='/login/')
def formulariogm(request):
    print(request.POST)
    return render(request,'email2.html')

# usuarios/views.py

# usuarios/views.py
# usuarios/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroForm

def registro_usuario(request):


    if request.method == 'POST':
        form = RegistroForm(request.POST)
        #print("Datos enviados en POST:", request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
            return redirect('login')
        else:
            #messages.error(request, "Por favor, corrige los errores en el formulario.")
            None
            #print(form.errors)  # Para depuración
            
    else:
        form = RegistroForm()


    return render(request, 'registration/registro.html', {'form': form})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Usuario
from .forms import UsuarioForm
from django.contrib import messages

 # Importa el decorador


# Vista para listar los usuarios y gestionar la clave de profesor
from .models import Usuario, ClaveProfesor

@profesor_required
def lista_usuarios(request):
    # Obtener el término de búsqueda
    busqueda = request.GET.get('busqueda', '')

    # Filtrar usuarios en base a la búsqueda
    usuarios = Usuario.objects.all()

    if busqueda:
        usuarios = usuarios.filter(
            Q(nombre__icontains=busqueda) | Q(correo__icontains=busqueda)
        )

    # Obtener la clave de profesor más reciente
    clave_profesor = ClaveProfesor.objects.latest('fecha_creacion').clave if ClaveProfesor.objects.exists() else ''

    # Manejar la actualización de la clave de profesor
    if request.method == 'POST' and 'nueva_clave' in request.POST:
        nueva_clave = request.POST.get('nueva_clave')
        if nueva_clave:
            ClaveProfesor.objects.create(clave=nueva_clave)  # Crear nueva clave
            messages.success(request, "Clave de profesor actualizada correctamente.")
            return redirect('lista_usuarios')  # Redirige para evitar reenvío de formulario

    context = {
        'usuarios': usuarios,
        'clave_profesor': clave_profesor,
        'busqueda': busqueda  # Pasamos el valor de búsqueda al contexto
    }
    return render(request, 'admin_custom/lista_usuarios.html', context)



@profesor_required
def agregar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario añadido con éxito.')
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'admin_custom/agregar_usuario.html', {'form': form})


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Usuario
from .forms import UsuarioForm

@profesor_required
@login_required


@login_required
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    # Verificar si el usuario actual es administrador
    if usuario.is_admin and not request.user.is_admin:
        messages.error(request, 'No tienes permisos para editar a un administrador.')
        return redirect('lista_usuarios')

    # Verificar si el usuario actual es profesor
    if request.user.tipo_usuario == Usuario.PROFESOR:
        # Si el profesor intenta editar a otro profesor o administrador, denegar acceso
        if usuario.tipo_usuario == Usuario.PROFESOR and usuario != request.user:
            messages.error(request, 'No tienes permisos para editar a otros profesores.')
            return redirect('lista_usuarios')

        # Permitir que los profesores editen su propia cuenta
        if usuario == request.user:
            if request.method == 'POST':
                form = UsuarioForm(request.POST, instance=usuario)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Tu cuenta ha sido actualizada con éxito.')
                    return redirect('lista_usuarios')
            else:
                form = UsuarioForm(instance=usuario)
        
        # Permitir a los profesores editar cuentas de estudiantes
        elif usuario.tipo_usuario == Usuario.ESTUDIANTE:
            if request.method == 'POST':
                form = UsuarioForm(request.POST, instance=usuario)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Cuenta del estudiante actualizada con éxito.')
                    return redirect('lista_usuarios')
            else:
                form = UsuarioForm(instance=usuario)

        # Bloquear la edición de otros profesores o administradores
        else:
            messages.error(request, 'No tienes permisos para editar este usuario.')
            return redirect('lista_usuarios')

    # Si es administrador, puede editar cualquier cosa
    elif request.user.is_admin:
        if request.method == 'POST':
            form = UsuarioForm(request.POST, instance=usuario)
            if form.is_valid():
                form.save()
                messages.success(request, 'Usuario actualizado con éxito.')
                return redirect('lista_usuarios')
        else:
            form = UsuarioForm(instance=usuario)

    return render(request, 'admin_custom/editar_usuario.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Usuario

@profesor_required
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    # Verificar si el usuario actual es profesor
    if request.user.tipo_usuario == Usuario.PROFESOR:
        # Los profesores solo pueden eliminar estudiantes
        if usuario.tipo_usuario != Usuario.ESTUDIANTE:
            messages.error(request, 'No tienes permisos para eliminar a este usuario.')
            return redirect('lista_usuarios')

    # Verificar si el usuario es administrador y no permitir su eliminación, excepto por otro administrador
    if usuario.is_admin and not request.user.is_admin:
        messages.error(request, 'No tienes permisos para eliminar a un administrador.')
        return redirect('lista_usuarios')

    # Permitir la eliminación si se cumplen las reglas anteriores
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado con éxito.')
        return redirect('lista_usuarios')

    return render(request, 'admin_custom/eliminar_usuario.html', {'usuario': usuario})

@profesor_required
def administrar(request):
    
    return render(request, 'administrar.html')


# para trazas

from .models import Navegacion

@profesor_required
def trazas(request):

    usuario = request.GET.get('usuario')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    url = request.GET.get('url')

    trazas = Navegacion.objects.all()

    if usuario:
        trazas = trazas.filter(usuario__nombre__icontains=usuario)

    if fecha_inicio:
        trazas = trazas.filter(timestamp__gte=fecha_inicio)
    if fecha_fin:
        trazas = trazas.filter(timestamp__lte=fecha_fin)

    if url:
        trazas = trazas.filter(url__icontains=url)

    context = {
        'trazas': trazas,
        'usuarios': Usuario.objects.all(),
    }
    return render(request, 'trazas.html', context)

   
from django.shortcuts import render, redirect
from datetime import date
from .models import Student, School, Evaluation, EvaluationIndex, Stage  # Importa todos los modelos necesarios
from django.shortcuts import render, redirect
from .models import Student, School, Evaluation, EvaluationIndex, Stage

@profesor_required
@login_required(login_url='/login/')
def guardar_datos_completos(request):
    if request.method == 'POST':
        # Guardar datos del estudiante
        nombre_estudiante = request.POST.get('nombre_estudiante')
        edad = request.POST.get('edad')
        curso = request.POST.get('curso')
        grado_grupo = request.POST.get('grado_grupo')
        clase = request.POST.get('clase')
        
        estudiante = Student(
            nombre=nombre_estudiante,
            edad=edad,
            curso=curso,
            grado=grado_grupo.split('-')[0],
            grupo=grado_grupo.split('-')[1],
            clase=clase
        )
        estudiante.save()

        # Guardar datos de la escuela
        nombre_escuela = request.POST.get('nombre_escuela')
        escuela, created = School.objects.get_or_create(nombre=nombre_escuela)

        # Guardar datos de la evaluación
        fecha = request.POST.get('fecha')
        stage_id = request.POST.get('stage')
        etapa = Stage.objects.get(id=stage_id)
        
        evaluacion = Evaluation(
            student=estudiante,
            school=escuela,
            stage=etapa,
            fecha=fecha
        )
        evaluacion.save()

        # Guardar los índices de evaluación
        for i in range(1, 5):
            indice = request.POST.get(f'indice_{i}')
            valor = request.POST.get(f'valor_{i}')
            evaluacion_cualitativa = request.POST.get(f'evaluacion_{i}')
            puntuacion = request.POST.get(f'puntuacion_{i}')

            indice_evaluacion = EvaluationIndex(
                evaluation=evaluacion,
                indice=indice,
                valor=valor,
                evaluacion=evaluacion_cualitativa,
                puntuacion=puntuacion
            )
            indice_evaluacion.save()

        return redirect('/home/')  # O a otra URL según tu aplicación

    return render(request, 'create_evaluation.html')  # Renderizar el template si no es POST

from django.shortcuts import render, get_object_or_404
from .models import Evaluation, Student



@login_required(login_url='/login/')
# Vista para listar las evaluaciones con filtros
def listar_evaluaciones(request):
    evaluaciones = Evaluation.objects.all()

    nombre_estudiante = request.GET.get('nombre_estudiante', '')
    nombre_escuela = request.GET.get('nombre_escuela', '')
    fecha = request.GET.get('fecha', '')
    grado = request.GET.get('grado', '')
    grupo = request.GET.get('grupo', '')
    edad = request.GET.get('edad', '')
    etapa = request.GET.get('etapa', '')
    tipo_usuario = request.user.tipo_usuario
    if nombre_estudiante:
        evaluaciones = evaluaciones.filter(student__nombre__icontains=nombre_estudiante)
    if nombre_escuela:
        evaluaciones = evaluaciones.filter(school__nombre__icontains=nombre_escuela)
    if fecha:
        evaluaciones = evaluaciones.filter(fecha=fecha)
    if grado:
        evaluaciones = evaluaciones.filter(student__grado__icontains=grado)
    if grupo:
        evaluaciones = evaluaciones.filter(student__grupo__icontains=grupo)
    if edad:
        evaluaciones = evaluaciones.filter(student__edad=edad)
    if etapa:
        evaluaciones = evaluaciones.filter(stage__nombre=etapa)

    context = {
        'evaluaciones': evaluaciones,
        'nombre_estudiante': nombre_estudiante,
        'nombre_escuela': nombre_escuela,
        'fecha': fecha,
        'grado': grado,
        'grupo': grupo,
        'edad': edad,
        'etapa': etapa,
        'etapas': Stage.objects.all(),
        'tipo_usuario': tipo_usuario,
    }
    #print(tipo_usuario)
    return render(request, 'listar_evaluaciones.html', context)

# Vista para mostrar todos los detalles de un estudiante
@login_required(login_url='/login/')
def detalles_estudiante(request, estudiante_id):
    estudiante = get_object_or_404(Student, id=estudiante_id)
    evaluaciones = Evaluation.objects.filter(student=estudiante)

    context = {
        'estudiante': estudiante,
        'evaluaciones': evaluaciones,
    }

    return render(request, 'detalles_estudiante.html', context)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student
@login_required(login_url='/login/')
@profesor_required
@csrf_exempt  # Desactivar la verificación CSRF para pruebas, pero es mejor utilizar CSRF tokens
def eliminar_estudiante_ajax(request, estudiante_id):
    if request.method == 'POST':
        # Obtener el estudiante o devolver un error
        try:
            estudiante = Student.objects.get(id=estudiante_id)
            estudiante.delete()  # Eliminar el estudiante
            return JsonResponse({'status': 'success', 'message': 'Estudiante eliminado correctamente'})
        except Student.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Estudiante no encontrado'}, status=404)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)




import pandas as pd
from django.http import HttpResponse
from .models import Evaluation

@login_required(login_url='/login/')
# Vista para exportar a Excel
def exportar_evaluaciones(request):
    evaluaciones = Evaluation.objects.all()

    # Aplicar los filtros si existen
    nombre_estudiante = request.GET.get('nombre_estudiante', '')
    nombre_escuela = request.GET.get('nombre_escuela', '')
    fecha = request.GET.get('fecha', '')
    grado = request.GET.get('grado', '')
    grupo = request.GET.get('grupo', '')
    edad = request.GET.get('edad', '')
    etapa = request.GET.get('etapa', '')

    if nombre_estudiante:
        evaluaciones = evaluaciones.filter(student__nombre__icontains=nombre_estudiante)
    if nombre_escuela:
        evaluaciones = evaluaciones.filter(school__nombre__icontains=nombre_escuela)
    if fecha:
        evaluaciones = evaluaciones.filter(fecha=fecha)
    if grado:
        evaluaciones = evaluaciones.filter(student__grado__icontains=grado)
    if grupo:
        evaluaciones = evaluaciones.filter(student__grupo__icontains=grupo)
    if edad:
        evaluaciones = evaluaciones.filter(student__edad=edad)
    if etapa:
        evaluaciones = evaluaciones.filter(stage__nombre=etapa)

    # Crear un diccionario para almacenar los datos de cada estudiante y sus índices
    data = []

    for evaluacion in evaluaciones:
        # Diccionario que representará una fila por estudiante
        row = {
            'Estudiante': evaluacion.student.nombre,
            'Escuela': evaluacion.school.nombre,
            'Fecha': evaluacion.fecha,
            'Grado': evaluacion.student.grado,
            'Grupo': evaluacion.student.grupo,
            'Edad': evaluacion.student.edad,
            'Etapa': evaluacion.stage.nombre,
        }
        
        # Obtener todos los índices de evaluación del estudiante y agregarlos en formato de columnas
        indices = evaluacion.indices.all()
        for indice in indices:
            # Crear las columnas para cada índice: Valor, Evaluación, y Puntuación
            row[f'{indice.indice} Valor'] = indice.valor
            row[f'{indice.indice} Evaluación'] = indice.evaluacion
            row[f'{indice.indice} Puntuación'] = indice.puntuacion
        
        # Agregar la fila con todos los datos
        data.append(row)

    # Convertir a DataFrame usando pandas
    df = pd.DataFrame(data)

    # Crear respuesta HTTP para descargar el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=evaluaciones.xlsx'

    # Usar ExcelWriter para permitir el filtrado en Excel
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Evaluaciones')

        # Obtener el workbook y worksheet para habilitar el filtrado
        workbook = writer.book
        worksheet = writer.sheets['Evaluaciones']
        
        # Habilitar el filtrado en la primera fila (encabezados)
        worksheet.auto_filter.ref = worksheet.dimensions

    return response
from django.shortcuts import render
from .models import Usuario, Evaluation

@login_required(login_url='/login/')
def usuarios_grafico(request):
  # Total de evaluaciones
    total_evaluaciones = Evaluation.objects.count()

    context = {
        'total_evaluaciones': total_evaluaciones,
        'estudiantes_count': Usuario.objects.filter(tipo_usuario='estudiante').count(),
        'profesores_count': Usuario.objects.filter(tipo_usuario='profesor').count(),
        'admins_count': Usuario.objects.filter(is_admin=True).count()
    }

    return render(request, 'usuarios_grafico.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from .forms import StudentForm, EvaluationForm
from .models import Student, Evaluation
from django.contrib.auth.decorators import login_required

@profesor_required
@login_required(login_url='/login/')
def editar_evaluacion(request, evaluacion_id):
    evaluacion = get_object_or_404(Evaluation, id=evaluacion_id)
    estudiante = evaluacion.student

    if request.method == 'POST':
        student_form = StudentForm(request.POST, instance=estudiante)
        evaluation_form = EvaluationForm(request.POST, instance=evaluacion)

        if student_form.is_valid() and evaluation_form.is_valid():
            student_form.save()
            evaluation_form.save()
            return redirect('detalles_estudiante', estudiante_id=estudiante.id)  # Redirige a la vista de detalles del estudiante
    else:
        student_form = StudentForm(instance=estudiante)
        evaluation_form = EvaluationForm(instance=evaluacion)

    context = {
        'student_form': student_form,
        'evaluation_form': evaluation_form,
        'estudiante': estudiante,
        'evaluacion': evaluacion,
    }

    return render(request, 'editar_evaluacion.html', context)


@login_required(login_url='/login/')
def ayuda(request):
        
    return render(request, 'ayuda.html')