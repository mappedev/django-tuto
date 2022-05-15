from secrets import choice
from django.contrib import admin
from .models import Choice, Question

# Register your models here.
# * Esto muestra los inputs necesarios para crear un choice apilados uno debajo de otro
# class ChoiceInLine(admin.StackedInline):

# * De esta manera se aprovecha más el espacio de los inputs
class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3  # * Opciones extras para incluir


class QuestionAdmin(admin.ModelAdmin):
    # * Cambiar orden de cómo se muestran los inputsgg
    # fields = ["pub_date", "question_text"]

    # * Cambiar orden y agregar un título
    fieldsets = [
        (None, {"fields": ["pub_date"]}),
        ("Date information", {"fields": ["question_text"]}),
    ]

    # * Incluir Choice directamente
    inlines = [ChoiceInLine]

    # * Campos a mostrar
    list_display = ("question_text", "pub_date", "was_published_recently")

    # * Permite indicar por cuáles campos filtrar. Los filtros dependerán del tipo de dato a filtrar
    list_filter = ["pub_date"]

    # * Agrega un buscador para los campos indicados
    search_fields = ["question_text"]
    # ! CONSEJO IMPORTANTE: mientras menos campos mejor, para evitar tanto trabajo a la base de datos


admin.site.register(Question, QuestionAdmin)
