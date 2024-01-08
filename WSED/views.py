from django.views import generic


class HomeView(generic.ListView):
    template_name = 'WSED/home.html'
    context_object_name = 'nothing'

    def get_queryset(self):
        return []
