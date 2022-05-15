from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import F
from django.views import generic
from django.utils import timezone
from .models import Choice, Question

# from django.template import loader # * forma completa de hacerlo
from django.shortcuts import get_object_or_404, render  # * forma con shortcut

# Create your views here.
class IndexView(generic.ListView):
    context_object_name = "latest_question_list"  # * question_list es el contexto por defecto en generic.ListView por el modelo
    template_name = "polls/index.html"

    def get_queryset(self):
        # * Return the last five published questions

        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )[:5]


# * Primera forma
# def index(req):
#     latest_question_list = Question.objects.order_by("pub_date")[:5]
#     # template = loader.get_template("polls/index.html") # * forma completa de hacerlo
#     context = {"latest_question_list": latest_question_list}
#     # output = ", ".join([q.question_text for q in latest_question_list])
#     # return HttpResponse(template.render(context, req)) # * forma completa de hacerlo
#     return render(req, "polls/index.html", context)


class DetailView(generic.DetailView):
    # * question es el contexto por defecto en generic.DetailView por el modelo
    template_name = "polls/detail.html"
    model = Question

    def get_queryset(self):
        # * Excludes any questions that aren't published yet.
        return Question.objects.filter(pub_date__lte=timezone.now())


# * Primera forma
# def detail(req, question_id):
#     # * Forma completa imperativa
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     # return render(req, "polls/detail.html", {"question": question})

#     # * Forma declarativa con shortcut
#     question = get_object_or_404(Question, pk=question_id)
#     return render(req, "polls/detail.html", {"question": question})

# * También hay una get_list_or_404() función, que funciona igual get_object_or_404(), excepto que usa filter()en lugar de get(). Se levanta Http404si la lista está vacía.


class ResultsView(generic.DetailView):
    template_name = "polls/results.html"
    model = Question

    def get_queryset(self):
        # * Excludes any questions that aren't published yet.
        return Question.objects.filter(pub_date__lte=timezone.now())


# * Primera forma
# def results(req, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(req, "polls/results.html", {"question": question})


def vote(req, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=req.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            req,
            "polls/detail.html",
            {"question": question, "error_message": "You did not select a choice"},
        )
    else:
        # * F en este momento se está usando para evitar una condición de carrera en caso de que dos datos se intenten modificar o crear al mismo tiempo
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # * IMPORTANT!
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))
