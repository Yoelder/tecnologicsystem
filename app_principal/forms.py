from django import forms
from .models import Usuario, Student, School, Stage, Evaluation, EvaluationIndex
from .models import ClaveProfesor  # Importa el modelo ClaveProfesor si no lo tienes ya

#registro de inicio 
import re  # Importar para las expresiones regulares
class RegistroForm(forms.ModelForm):
    confirmar_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['nombre', 'correo', 'tipo_usuario', 'clave_profesor', 'password']
        widgets = {
            'password': forms.PasswordInput(),
            'clave_profesor': forms.PasswordInput(),
        }

    # Validación personalizada para la contraseña
    def clean_password(self):
        password = self.cleaned_data.get("password")

        # Validar que la contraseña tenga al menos 8 caracteres
        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")

        # Verificar que contenga letras
        if not re.search(r'[A-Za-z]', password):
            raise forms.ValidationError("La contraseña debe contener al menos una letra.")

        # Verificar que contenga números
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError("La contraseña debe contener al menos un número.")

        # Verificar que contenga caracteres especiales o puntos
        if not re.search(r'[\W.]', password):
            raise forms.ValidationError("La contraseña debe contener al menos un carácter especial o un punto.")

        return password

    # Validación personalizada para el nombre de usuario (solo letras y números)
    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")

        # Verificar si el nombre de usuario ya está registrado
        if Usuario.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError("El nombre de usuario ya está registrado. Por favor, elige otro.")

        # Validar que el nombre solo contenga letras y números (sin caracteres especiales)
        if not re.match(r'^[A-Za-z0-9]+$', nombre):
            raise forms.ValidationError("El nombre de usuario solo puede contener letras y números, sin caracteres especiales.")

        return nombre

    # Validación personalizada para el correo electrónico
    def clean_correo(self):
        correo = self.cleaned_data.get("correo")

        # Verificar si el correo ya está registrado
        if Usuario.objects.filter(correo=correo).exists():
            raise forms.ValidationError("El correo electrónico ya está registrado. Por favor, usa otro.")
        
        return correo

    # Validación general del formulario
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar_password = cleaned_data.get("confirmar_password")
        tipo_usuario = cleaned_data.get("tipo_usuario")
        clave_profesor = cleaned_data.get("clave_profesor")

        # Validar que las contraseñas coincidan
        if password and confirmar_password and password != confirmar_password:
            self.add_error('confirmar_password', "Las contraseñas no coinciden.")

        # Obtener la clave de profesor desde la base de datos si es profesor
        if tipo_usuario == 'profesor':
            try:
                clave = ClaveProfesor.objects.latest('fecha_creacion').clave  # Obtener la clave más reciente
            except ClaveProfesor.DoesNotExist:
                raise forms.ValidationError("No hay clave de profesor registrada en el sistema.")
            
            if clave_profesor != clave:
                self.add_error('clave_profesor', "Clave de profesor incorrecta.")

        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["password"])
        if commit:
            usuario.save()
        return usuario





from .models import Usuario


# Formulario de USUARIOS
class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, required=False, label="Confirmar contraseña")

    class Meta:
        model = Usuario
        fields = ('nombre', 'correo', 'tipo_usuario', 'password')

    # Validación personalizada para el nombre de usuario (solo letras y números)
    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")

        # Verificar si el nombre de usuario ya está registrado
        if Usuario.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError("El nombre de usuario ya está registrado. Por favor, elige otro.")

        # Validar que el nombre solo contenga letras y números (sin caracteres especiales)
        if not re.match(r'^[A-Za-z0-9]+$', nombre):
            raise forms.ValidationError("El nombre de usuario solo puede contener letras y números, sin caracteres especiales.")

        return nombre

    # Validación personalizada para el correo electrónico
    def clean_correo(self):
        correo = self.cleaned_data.get("correo")
        
        # Verificar si el correo ya está registrado
        if Usuario.objects.filter(correo=correo).exists():
            raise forms.ValidationError("El correo electrónico ya está registrado. Por favor, usa otro.")
        
        return correo

    # Validación personalizada para la contraseña
    def clean_password(self):
        password = self.cleaned_data.get("password")

        # Validar que la contraseña tenga al menos 8 caracteres
        if password and len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres, incluir letras, números y caracteres especiales.")

        # Verificar que contenga letras
        if not re.search(r'[A-Za-z]', password):
            raise forms.ValidationError("La contraseña debe contener al menos una letra.")

        # Verificar que contenga números
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError("La contraseña debe contener al menos un número.")

        # Verificar que contenga caracteres especiales o puntos
        if not re.search(r'[\W.]', password):
            raise forms.ValidationError("La contraseña debe contener al menos un carácter especial o un punto.")

        return password

    # Validación de coincidencia de contraseñas
    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        
        if password and password2 and password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        
        return password2

    # Validación general (opcional)
    def clean(self):
        cleaned_data = super().clean()
        
        # Aquí podrías agregar validaciones adicionales si fuera necesario
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user












# Formularios relacionados con la evaluación
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['nombre', 'edad', 'curso', 'grado', 'grupo', 'clase']

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['nombre']

class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ['nombre']

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['student', 'school', 'stage', 'fecha']

class EvaluationIndexForm(forms.ModelForm):
    class Meta:
        model = EvaluationIndex
        fields = ['evaluation', 'indice', 'valor', 'evaluacion', 'puntuacion']

from django import forms
from .models import Student, Evaluation
import re

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['nombre', 'edad', 'grado', 'grupo', 'curso', 'clase']  # Asegúrate de que los campos estén aquí

    # Validación personalizada para 'grado' (formato: uno o dos números seguidos de "mo")
    def clean_grado(self):
        grado = self.cleaned_data.get('grado')
        if not re.match(r'^\d{1,2}mo$', grado):
            raise forms.ValidationError("El campo 'grado' debe tener un formato de uno o dos números seguido de 'mo' (ej: 12mo).")
        return grado

    # Validación personalizada para 'grupo' (uno o dos números o una letra)
    def clean_grupo(self):
        grupo = self.cleaned_data.get('grupo')
        if not re.match(r'^[A-Za-z0-9]{1,2}$', grupo):
            raise forms.ValidationError("El campo 'grupo' debe tener uno o dos números o una letra.")
        return grupo

    # Validación personalizada para 'curso' (formato: 2024/2025)
    def clean_curso(self):
        curso = self.cleaned_data.get('curso')
        if not re.match(r'^\d{4}/\d{4}$', curso):
            raise forms.ValidationError("El campo 'curso' debe tener el formato '2024/2025'.")
        return curso


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['school', 'stage', 'fecha']

    # Hacemos que 'stage' y 'fecha' no sean modificables
    def __init__(self, *args, **kwargs):
        super(EvaluationForm, self).__init__(*args, **kwargs)
        self.fields['stage'].disabled = True
        self.fields['fecha'].disabled = True

