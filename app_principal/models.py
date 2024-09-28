#para registro de usuarios
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

class UsuarioManager(BaseUserManager):
    def create_user(self, nombre, correo, tipo_usuario, password=None, clave_profesor=None):
        print(clave_profesor,tipo_usuario)
        if not correo:
            raise ValueError("El usuario debe tener un correo electrónico")

        usuario = self.model(
            nombre=nombre,
            correo=self.normalize_email(correo),
            tipo_usuario=tipo_usuario
        )



        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, nombre, correo, password=None):
        usuario = self.create_user(
            nombre=nombre,
            correo=correo,
            password=password,
            tipo_usuario='admin'
        )
        usuario.is_admin = True
        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.save(using=self._db)
        return usuario

class Usuario(AbstractBaseUser, PermissionsMixin):
    ESTUDIANTE = 'estudiante'
    PROFESOR = 'profesor'

    TIPO_USUARIO_CHOICES = [
        (ESTUDIANTE, 'Estudiante'),
        (PROFESOR, 'Profesor'),
    ]

    nombre = models.CharField(max_length=255)
    correo = models.EmailField(unique=True)
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES, default=ESTUDIANTE)
    clave_profesor = models.CharField(max_length=255, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.correo

    def has_perm(self, perm, obj=None):
        """Verifica si el usuario tiene un permiso específico"""
        return True

    def has_module_perms(self, app_label):
        """Verifica si el usuario tiene permisos para la aplicación especificada"""
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin


#para trazas

from django.conf import settings  # Importa settings para usar AUTH_USER_MODEL

class Navegacion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    url = models.CharField(max_length=255)
    metodo_http = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    agente_usuario = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.usuario} visitó {self.url} el {self.timestamp}"






from django.db import models

# Tabla de Escuelas
class School(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Tabla de Períodos o Etapas
class Stage(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

# Tabla de Estudiantes
class Student(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    curso = models.CharField(max_length=50)
    grado = models.CharField(max_length=50)
    grupo = models.CharField(max_length=50)
    clase = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

# Tabla de Evaluaciones
class Evaluation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='evaluations')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='evaluations')
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='evaluations')
    fecha = models.DateField()

    def __str__(self):
        return f"Evaluación de {self.student.nombre} en {self.fecha}"

# Tabla de Índices de Evaluación
class EvaluationIndex(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='indices')
    indice = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    evaluacion = models.CharField(max_length=10)
    puntuacion = models.IntegerField()

    def __str__(self):
        return f"Índice {self.indice} de {self.evaluation.student.nombre}"


from django.db import models

class ClaveProfesor(models.Model):
    clave = models.CharField(max_length=255)  # Clave no cifrada
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación automática

    def __str__(self):
        return f"Clave: {self.clave} - Creada el: {self.fecha_creacion}"
