import re

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from .models import Blog
from . import globals

xss_pattern = re.compile(
    r'''(?:
    <script.*?>.*?</script>|          # Basic script tags
    <.*?javascript:.*?>|              # Elements with JavaScript protocol
    <.*?on\w+.*?=.*?>|                # HTML elements with event handlers
    <\?.*?\?>|                        # PHP tags
    <.*?src=['"].*?javascript:.*?>|   # Using javascript: protocol in src attribute of tags
    <.*?href=['"].*?javascript:.*?>|  # Using javascript: protocol in href attribute of tags
    <.*?style=['"].*?expression\(.*?\).*?>|  # CSS expression
    <.*?style=['"].*?url\(['"]?javascript:.*?\).*?>| # CSS url() with JavaScript
    <.*?(\bon\w+|style|background|src|href|data|action)=['"]?\s*javascript:.*?>| # Common attributes for inline JavaScript
    <.*?(\bon\w+|style|background|src|href|data|action)=['"]?\s*.*?>| # Common attributes for inline JavaScript wider
    ['"]?\s*javascript:.*?(;|<|\s)|   # Loose JavaScript protocol occurrences
    <iframe.*?src=['"].*?>|           # Iframe with src
    <frame.*?src=['"].*?>|            # Frame with src
    <.*?data=['"].*?javascript:.*?>|  # Using javascript: protocol in data attribute
    <.*?background=['"].*?javascript:.*?>| # Using javascript: in background
    <.*?formaction=['"].*?javascript:.*?>  # Using javascript: in formaction
    )''',
    re.IGNORECASE | re.VERBOSE)


class IndexView(generic.ListView):
    template_name = "xss_app/index.html"
    context_object_name = "blog_post_list"

    def __init__(self):
        self.object_list = None
        self.part1_completed = None
        self.performed_reflected_xss = None
        self.part1_message = None
        self.part2_completed = None
        self.performed_stored_xss = None
        self.part2_message = None

    def dispatch(self, request, *args, **kwargs):
        self.part1_completed = globals.PART1_COMPLETED
        self.performed_reflected_xss = globals.PERFORMED_REFLECTED_ATTACK
        self.part2_completed = globals.PART2_COMPLETED
        self.performed_stored_xss = globals.PERFORMED_STORED_ATTACK
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Blog.objects.order_by("-pub_date")[:10]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['part1_completed'] = self.part1_completed
        context['performed_reflected_xss'] = self.performed_reflected_xss
        context['part1_message'] = self.part1_message
        context['part2_completed'] = self.part2_completed
        context['performed_stored_xss'] = self.performed_stored_xss
        context['part2_message'] = self.part2_message
        return context

    def post(self, request, *args, **kwargs):
        # INPUTS USED FOR EXERCISE 1 SUBMISSION (OR DEFAULT)
        user_input_cookie = request.POST.get('cookieInput')
        real_cookie = request.POST.get('realCookie', 'default=')
        csrf_value = real_cookie.split('=')[1]

        # INPUT USED FOR EXERCISE 2 SUBMISSION
        user_input_secret = request.POST.get('secretInput')

        # CHECK EXERCISE 1 CRITERIA
        if user_input_cookie == csrf_value and self.performed_reflected_xss:
            globals.PART1_COMPLETED = True
            self.part1_message = True

        # CHECK EXERCISE 2 CRITERIA
        if user_input_secret == globals.STORED_SECRET and self.performed_stored_xss:
            globals.PART2_COMPLETED = True
            self.part2_message = True

        # SET UPDATED VALUES AND RETURN CONTEXT
        self.part1_completed = globals.PART1_COMPLETED
        self.part2_completed = globals.PART2_COMPLETED
        self.object_list = self.get_queryset()
        return render(request, "xss_app/index.html", self.get_context_data(**kwargs))


class DetailView(generic.DetailView):
    model = Blog
    template_name = "xss_app/detail.html"

    def get_object(self):
        blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
        if blog.malicious_headline:
            globals.PERFORMED_STORED_ATTACK = True
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


class BlogPostCreateView(generic.CreateView):
    model = Blog
    template_name = "xss_app/create.html"
    fields = ["headline", "content"]

    def form_valid(self, form):
        headline = form.cleaned_data.get("headline")
        content = form.cleaned_data.get('content')

        if headline and content:
            if xss_pattern.search(content) and not xss_pattern.search(headline):
                form.instance.headline = "Ha! The rendering of blog post content on this wall is safe!"
                form.instance.malicious_content = True
            if xss_pattern.search(headline):
                form.instance.content = "Ha! The rendering of blog post headlines on this wall is safe!"
                form.instance.malicious_headline = True
            form.instance.author = self.request.user.username if self.request.user.is_authenticated else "Anonymous"

        return super(BlogPostCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('xss_app:index') + '#blogposts'


class ResetAllPostsView(generic.View):
    def post(self, request, *args, **kwargs):
        Blog.objects.filter(pk__gte=4).delete()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('xss_app:index') + '#exercise2'


class ResetExercise1View(generic.View):
    # Do I want it to reset both or find a way to have exercise 2 completed and exercise 1 reset?
    def post(self, request, *args, **kwargs):
        globals.PART1_COMPLETED = False
        globals.PERFORMED_REFLECTED_ATTACK = False
        globals.PART2_COMPLETED = False
        globals.PERFORMED_STORED_ATTACK = False

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('xss_app:index') + '#search'


class ResetExercise2View(generic.View):
    def post(self, request, *args, **kwargs):
        globals.PART2_COMPLETED = False
        globals.PERFORMED_STORED_ATTACK = False

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('xss_app:index') + '#blogposts'