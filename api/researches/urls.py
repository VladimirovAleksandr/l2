from django.urls import path
from . import views

urlpatterns = [
    path('templates', views.get_researches_templates),
    path('all', views.get_researches),
    path('by-department', views.researches_by_department),
    path('params', views.researches_params),
    path('update', views.researches_update),
    path('details', views.researches_details),
    path('paraclinic_details', views.paraclinic_details),
    path('hosp-service-details', views.hospital_service_details),
    path('fast-templates', views.fast_templates),
    path('fast-template-data', views.fast_template_data),
    path('fast-template-save', views.fast_template_save),
    path('fraction-title', views.fraction_title),
    path('field-title', views.field_title),
    path('fields-and-groups-titles', views.fields_and_groups_titles),
    path('descriptive-research', views.descriptive_research),
    path('research-dispensary', views.research_dispensary),
    path('research-specialities', views.research_specialities),
    path('save-dispensary-data', views.save_dispensary_data),
    path('load-research-by-diagnos', views.load_research_by_diagnos),
    path('by-direction-params', views.by_direction_params),
    path('get-direction-params', views.get_direction_params),
    path('localization', views.localization),
    path('localization/save', views.localization_save),
]
