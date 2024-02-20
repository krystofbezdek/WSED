import re

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Blog
from . import globals

xss_pattern = re.compile(r'(?:<script.*?>.*?</script>|<.*?javascript:.*?>|<.*?on\w+.*?=.*?>|<\?.*?\?>)', re.IGNORECASE)


class IndexView(generic.ListView):
    template_name = "xss_app/index.html"
    context_object_name = "blog_post_list"

    def __init__(self):
        self.object_list = None
        self.part1_completed = globals.PART1_COMPLETED
        self.performed_reflected_xss = globals.PERFORMED_REFLECTED_ATTACK

    def get_queryset(self):
        return Blog.objects.order_by("-pub_date")[:10]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['part1_completed'] = self.part1_completed
        context['performed_reflected_xss'] = self.performed_reflected_xss
        return context

    def post(self, request, *args, **kwargs):
        user_input_cookie = request.POST.get('cookieInput')
        real_cookie = request.POST.get('realCookie')
        csrf_value = real_cookie.split('=')[1]

        if user_input_cookie == real_cookie or user_input_cookie == csrf_value and self.performed_reflected_xss:
            globals.PART1_COMPLETED = True
        else:
            globals.PART1_COMPLETED = False

        self.part1_completed = globals.PART1_COMPLETED
        self.object_list = self.get_queryset()
        return render(request, "xss_app/index.html", self.get_context_data(**kwargs))


class DetailView(generic.DetailView):
    model = Blog
    template_name = "xss_app/detail.html"

    def get_object(self):
        blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return blog

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['referer'] = self.request.META.get('HTTP_REFERER')
        return context


class SearchResultsView(generic.ListView):
    model = Blog
    template_name = "xss_app/search.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if xss_pattern.search(query):
            globals.PERFORMED_REFLECTED_ATTACK = True
        param = f'%{query}%'
        object_list = Blog.objects.raw("SELECT * FROM xss_app_blog WHERE headline LIKE %s", [param])
        return object_list

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get("q")
        return context


class BlogPostCreateView(generic.View):
    def get(self, request, *args, **kwargs):
        headline = request.GET.get('headline')
        content = request.GET.get('content')
        malicious_headline = False
        malicious_content = False

        if headline and content:
            if xss_pattern.search(content) and not xss_pattern.search(headline):
                headline = "Ha! The rendering of blog post content on this wall is safe!"
                malicious_content = True
            if xss_pattern.search(headline):
                content = "Ha! The rendering of blog post headlines on this wall is safe!"
                malicious_headline = True
            author = request.user.username if request.user.is_authenticated else "Anonymous"
            Blog.objects.create(headline=headline, content=content, author=author, malicious_headline=malicious_headline, malicious_content=malicious_content)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('xss_app:index') + '#blogposts'