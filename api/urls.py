from django.urls import path, include

from . import views

urlpatterns = [
    path('send', views.send),
    path('endpoint', views.endpoint),
    path('departments', views.departments),
    path('bases', views.bases),
    path('laborants', views.laborants),
    path('current-user-info', views.current_user_info),
    path('directive-from', views.directive_from),
    path('load-users-by-group', views.load_docprofile_by_group),
    path('users', views.users_view),
    path('user', views.user_view),
    path('user-save', views.user_save_view),
    path('user-location', views.user_location),
    path('user-get-reserve', views.user_get_reserve),
    path('user-fill-slot', views.user_fill_slot),
    path('statistics-tickets/types', views.statistics_tickets_types),
    path('statistics-tickets/send', views.statistics_tickets_send),
    path('statistics-tickets/get', views.statistics_tickets_get),
    path('statistics-tickets/invalidate', views.statistics_tickets_invalidate),
    path('mkb10', views.mkb10),
    path('methods-of-taking', views.methods_of_taking),
    path('key-value', views.key_value),
    path('vich_code', views.vich_code),
    path('flg', views.flg),
    path('search-template', views.search_template),
    path('load-templates', views.load_templates),
    path('get-template', views.get_template),
    path('templates/update', views.update_template),
    path('modules', views.modules_view),
    path('autocomplete', views.autocomplete),
    path('job-types', views.job_types),
    path('job-save', views.job_save),
    path('job-list', views.job_list),
    path('job-cancel', views.job_cancel),
    path('reader-status', views.reader_status),
    path('reader-status-update', views.reader_status_update),
    path('actual-districts', views.actual_districts),
    path('hospitals', views.hospitals),
    path('researches/', include('api.researches.urls')),
    path('patients/', include('api.patients.urls')),
    path('directions/', include('api.directions.urls')),
    path('stationar/', include('api.stationar.urls')),
    path('bacteria/', include('api.bacteria.urls')),
    path('laboratory/', include('api.laboratory.urls')),
    path('plans/', include('api.plans.urls')),
    path('doctor-call/', include('api.doctor_call.urls')),
    path('list-wait/', include('api.list_wait.urls')),
    path('procedural-list/', include('api.procedure_list.urls')),
]
