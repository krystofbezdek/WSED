from django.db import connection
from unittest import loader

# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse, HttpResponseRedirect
# from django.urls import reverse
from django.views import generic
# from django.db.models import Q

from .models import Blog


# Define model by queryset or model =
class IndexView(generic.ListView):
    template_name = "xss_app/index.html" # Specify like this or it uses default like <app name>/<model name>_detail.html
    context_object_name = "blog_post_list"

    def get_queryset(self):
        return Blog.objects.order_by("-pub_date")[:10]


class DetailView(generic.DetailView):
    model = Blog
    template_name = "xss_app/detail.html"


class SearchResultsView(generic.ListView):
    model = Blog
    template_name = "xss_app/search.html"

    def get_queryset(self):
        query = self.request.GET.get("q") # supply 'hello' OR 1 = 1 --;

        # SAFE
        # param = f'%{query}%'
        # object_list = Blog.objects.raw("SELECT * FROM xss_app_blog WHERE headline LIKE %s", [param])

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM xss_app_blog WHERE headline = '" + query + "'")
            rows = cursor.fetchall()

        results = []
        for row in rows:
            row_data = {
                "id": row[0],
                "headline": row[1],
                "blog_post_text": row[2],
                "author": row[3],
                "pub_date": row[4]
            }
            results.append(row_data)
        return results

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get("q")
        return context


class BlogPostCreateView(generic.CreateView):
    model = Blog
    template_name = "xss_app/create.html"
    fields = ["headline", "blog_post_text", "author"]