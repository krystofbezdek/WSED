from django.db import connection
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
        return Question.objects.order_by("-pub_date")[:10]


class DetailView(generic.DetailView):
    model = Question
    template_name = "xss_app/detail.html"


class SearchResultsView(generic.ListView):
    model = Question
    template_name = "xss_app/search.html"

    def get_queryset(self):
        query = self.request.GET.get("q") # supply 'hello' OR 1 = 1 --;

        # SAFE
        # param = f'%{query}%'
        # object_list = Question.objects.raw("SELECT * FROM xss_app_question WHERE question_text LIKE %s", [param])

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM xss_app_question WHERE question_text = '" + query + "'")
            rows = cursor.fetchall()

        results = []
        for row in rows:
            row_data = {
                "id": row[0],
                "question_text": row[1],
                "pub_date": row[2]
            }
            results.append(row_data)
        return results

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get("q")
        return context


class QuestionCreateView(generic.CreateView):
    model = Question
    template_name = "xss_app/create.html"
    fields = ["question_text"]