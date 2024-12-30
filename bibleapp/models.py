# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models





class Libros(models.Model):
    id = models.IntegerField(primary_key=True)
    l_link = models.CharField(db_column='L_link', max_length=100, blank=True, null=True)  # Field name made lowercase.
    l_book = models.CharField(db_column='L_book', max_length=50, blank=True, null=True)  # Field name made lowercase.
    l_libro_desc = models.CharField(db_column='L_Libro_Desc', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'libros'

    def __str__(self):
        return self.l_libro_desc


class Capitulos(models.Model):
    id = models.IntegerField(primary_key=True)
    #id for chapter below
    c_capitulo_desc = models.IntegerField(db_column='C_Capitulo_Desc', blank=True, null=True)  # Field name made lowercase.
    c_idlibro = models.ForeignKey('Libros', models.DO_NOTHING, db_column='C_IdLibro')  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'capitulos'

    def __str__(self):
        return self.c_capitulo_desc
    
    
class Versiculos(models.Model):
    id = models.IntegerField(primary_key=True)
    contenido = models.TextField(blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    v_idcapitulo = models.ForeignKey(Capitulos, models.DO_NOTHING, db_column='V_IdCapitulo', blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'versiculos'

    def __str__(self):
        return self.contenido
