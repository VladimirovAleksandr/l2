from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('search/directions', views.results_search_directions),
    path('enter', views.enter),
    path('get', views.result_get),
    path('pdf', views.result_print),
    path('preview', TemplateView.as_view(template_name='dashboard/results_preview.html')),
    path('results', TemplateView.as_view(template_name='dashboard/results.html')),
    path('journal', views.result_journal_print),
    path('journal_table', views.result_journal_table_print),
    path('filter', views.result_filter),
    path('day', views.get_day_results),
]
