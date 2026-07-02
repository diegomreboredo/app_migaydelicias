from django.db import models
from empresas.models import Empresa
from categorias.models import Categoria
from django.core.exceptions import ValidationError
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile

class Producto(models.Model):
    empresa = models.ForeignKey(
    Empresa,
    on_delete=models.CASCADE,
    related_name="productos"
    )

    categoria = models.ForeignKey(
    Categoria,
    on_delete=models.PROTECT,
    related_name="productos"
    )

    nombre = models.CharField(
        max_length=100
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    imagen = models.ImageField(
        upload_to="productos/",
        blank=True,
        null=True
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    stock_minimo = models.PositiveIntegerField(
        default=0
    )
    
    stock_reservado = models.PositiveIntegerField(
        default=0
    )

    activo = models.BooleanField(
        default=True
    )

    creado = models.DateTimeField(
        auto_now_add=True
    )

    actualizado = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["nombre"]
        
    @property
    def stock_disponible(self):
        return self.stock - self.stock_reservado
        
    def clean(self):
      if self.categoria_id and self.empresa_id:
          if self.categoria.empresa != self.empresa:
              raise ValidationError(
                  "La categoría debe pertenecer a la misma empresa que el producto."
              )
              
    def save(self, *args, **kwargs):

      if self.imagen:
  
          img = Image.open(self.imagen)
  
          if img.mode != "RGB":
              img = img.convert("RGB")
  
          img.thumbnail((800, 800))
  
          output = BytesIO()
  
          img.save(
          output,
          format="WEBP",
          quality=85,
          method=6
      )
  
          output.seek(0)
  
          nombre = self.imagen.name.rsplit(".", 1)[0] + ".webp"
  
          self.imagen.save(
              nombre,
              ContentFile(output.read()),
              save=False
          )

      super().save(*args, **kwargs)

    def __str__(self):
      return f"{self.nombre} ({self.empresa.nombre})"