from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

class Subasta(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio_salida = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField()
    # puedes añadir un campo "creador" si conectas con usuarios

class Puja(models.Model):
    subasta = models.ForeignKey(Subasta, related_name='pujas', on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    # también puedes añadir "usuario"