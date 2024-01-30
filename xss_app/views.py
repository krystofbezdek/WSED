from django.db import connection
# from unittest import loader

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.core.mail import send_mail
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


# http://127.0.0.1:8000/xss_app/search/?q=%3Cscript%3Edocument.addEventListener(%27DOMContentLoaded%27,%20(event)%20=%3E%20{%20window.location.href%20=%20%27https://www.google.com%27;%20});%3C/script%3E
class SearchResultsView(generic.ListView):
    model = Blog
    template_name = "xss_app/search.html"

    def get_queryset(self):
        query = self.request.GET.get("q") # supply anything' OR 1 = 1 --;

        # SAFE
        param = f'%{query}%'
        object_list = Blog.objects.raw("SELECT * FROM xss_app_blog WHERE headline LIKE %s", [param])

        # UNSAFE - SQL INJECTION
        # with connection.cursor() as cursor:
        #     cursor.execute("SELECT * FROM xss_app_blog WHERE headline LIKE '%" + query + "%'")
        #     rows = cursor.fetchall()
        #
        # results = []
        # for row in rows:
        #     row_data = {
        #         "id": row[0],
        #         "headline": row[1],
        #         "content": row[2],
        #         "author": row[3],
        #         "pub_date": row[4]
        #     }
        #     results.append(row_data)
        return object_list

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get("q")
        return context

# <script>function callfunc() {fetch('http://127.0.0.1:8000/xss_app/create?headline=HACKED&content=' + document.cookie).then(response => response.text()).then(data => {console.log(data);}).catch(error => {console.error('Error:', error);});}</script><div onmouseover="callfunc()">You have been hacked</div>
class BlogPostCreateView(generic.View):
    def get(self, request, *args, **kwargs):
        headline = request.GET.get('headline')
        content = request.GET.get('content')

        if headline and content:
            if ("<script>" in content or "</script>" in content) and ("<script>" not in headline or "</script>" not in headline):
                headline = "Ha! The rendering of content on this wall is safe!"
            if "<script>" in headline or "</script>" in headline:
                content = "Ha! The rendering of headlines on this wall is safe!"
            author = request.user.username if request.user.is_authenticated else "Anonymous"
            Blog.objects.create(headline=headline, content=content, author=author)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return render(request, "xss_app/create.html")

    def get_success_url(self):
        return reverse('xss_app:index') + '#blogposts'