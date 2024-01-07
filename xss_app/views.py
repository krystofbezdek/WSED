from unittest import loader

# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse, HttpResponseRedirect
# from django.urls import reverse
from django.views import generic
from django.db.models import Q

from .models import Question


# Define model by queryset or model =
class IndexView(generic.ListView):
    template_name = "xss_app/index.html" # Specify like this or it uses default like <app name>/<model name>_detail.html
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "xss_app/detail.html"


class SearchResultsView(generic.ListView):
    model = Question
    template_name = "xss_app/search.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Question.objects.filter(
            Q(question_text__icontains=query)
        )
        return object_list

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get("q")
        return context


class QuestionCreateView(generic.CreateView):
    model = Question
    template_name = "xss_app/create.html"
    fields = ["question_text"]