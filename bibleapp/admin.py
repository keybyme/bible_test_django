from django.contrib import admin
from .models import Versiculos



class VerseAdmin(admin.ModelAdmin):
    search_fields = ['contenido']


    
admin.site.register(Versiculos,VerseAdmin)