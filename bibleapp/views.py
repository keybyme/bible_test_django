from django.shortcuts import render, redirect
from .models import Libros, Capitulos, Versiculos
from django.db.models import Q 
from django.db import connection
from django.db.models import Func
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank, SearchHeadline

# Define the Unaccent function for use in annotations
class Unaccent(Func):
    function = 'unaccent'
    template = "%(function)s(%(expressions)s)"

def unaccent_string(value):
    """Helper function to unaccent a string using raw SQL."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT unaccent(%s);", [value])
        return cursor.fetchone()[0]

 

def results(request):
    choice = request.GET.get('choice')  
    c = unaccent_string(choice)
    vector = SearchVector(Unaccent('contenido'))
    query = SearchQuery(c)
    search_headline = SearchHeadline('contenido',query) 
    
    verse = Versiculos.objects.annotate(search=vector).annotate(headline=search_headline).filter(search=c) 

    context = {
        'verse':verse, 
        'count':verse.count()
    }
    return render(request, "partials/results.html", context)


def get_chapter(request, book, chapter):
    book_by_chapter = Libros.objects.get(l_libro_desc=book)
    chapter_by_chapter = Capitulos.objects.get(c_idlibro=book_by_chapter, c_capitulo_desc=chapter)
    verse_by_chapter = Versiculos.objects.filter(v_idcapitulo=chapter_by_chapter) 
    all_chapter = Capitulos.objects.filter(c_idlibro=book_by_chapter) 
    print(all_chapter.count()) 

    # print("book:" ,book ," chapter: " , chapter)
    # print("===============\n", book_by_chapter.l_libro_desc)
    # print("===============\n", chapter_by_chapter.c_capitulo_desc)
     
    
    prev = request.POST.get('prev')
    next = request.POST.get('next') 
    new_book_value = Libros.objects.get(id=book_by_chapter.id) 
    num = all_chapter.count() 
    num2 = all_chapter.count() 
    
    if request.method == "POST": 
        if prev == 'prev': 
            num = int(chapter)-1
            print(f'number calculated for', num)   
            if num <= 0:
                new_book_value1 = Libros.objects.get(id=new_book_value.id-1) #gets book count for previous book
                new_chapter_value1 = Capitulos.objects.filter(c_idlibro=new_book_value1).count()#gets chapter count for previous chapter
                return redirect('get_chapter',new_book_value1.l_libro_desc,new_chapter_value1)
            return redirect('get_chapter',book_by_chapter.l_libro_desc,chapter_by_chapter.c_capitulo_desc-1)
        if next == 'next':
            num =+ int(chapter)+1
            print(f'number calculated for', num) 
            if num > num2:
                new_book_value1 = Libros.objects.get(id=new_book_value.id+1) #gets book count for previous book
                return redirect('get_chapter',new_book_value1.l_libro_desc,1)
            return redirect('get_chapter',book_by_chapter.l_libro_desc,chapter_by_chapter.c_capitulo_desc+1)

    context = {
        "contenido":verse_by_chapter,
        'book':book_by_chapter,
        'chapter':chapter_by_chapter,

    }
    return render(request, "get-chapter.html", context)
 

def index(request):  
    choice = request.GET.get('choice') 
    if choice:
        return render(request, "partials/results.html", {'choice':choice})
    return render(request, "index.html")
