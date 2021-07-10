from django.contrib import admin

from .models import (
    IstochnikiFinansirovaniya,
    Napravleniya,
    TubesRegistration,
    Issledovaniya,
    Result,
    FrequencyOfUseResearches,
    CustomResearchOrdering,
    RMISOrgs,
    RMISServiceInactive,
    Diagnoses,
    TypeJob,
    EmployeeJob,
    KeyValue,
    PersonContract,
    ExternalOrganization,
    DirectionsHistory,
)

admin.site.register(IstochnikiFinansirovaniya)


@admin.register(Napravleniya)
class CardAdmin(admin.ModelAdmin):
    raw_id_fields = (
        'client',
        'case',
        'parent',
        'parent_auto_gen',
        'parent_slave_hosp',
    )
    search_fields = ('pk',)


@admin.register(Issledovaniya)
class IssAdmin(admin.ModelAdmin):
    raw_id_fields = (
        'napravleniye',
        'research',
        'parent',
        'tubes',
    )
    search_fields = ('napravleniye__pk',)


class ResTypeJob(admin.ModelAdmin):
    list_display = (
        'title',
        'value',
        'hide',
    )
    list_display_links = ('title',)
    search_fields = ('title',)


class ResEmployeeJob(admin.ModelAdmin):
    list_display = (
        'type_job',
        'doc_execute',
        'count',
        'date_job',
        'time_save',
    )
    list_display_links = ('doc_execute',)
    search_fields = ('doc_execute__fio',)


class ResKeyValue(admin.ModelAdmin):
    list_display = (
        'key',
        'value',
    )
    list_display_links = ('value',)
    search_fields = ('value',)


class ResDiagnoses(admin.ModelAdmin):
    search_fields = ('code',)


class ResPersonContract(admin.ModelAdmin):
    list_display = (
        'num_contract',
        'sum_contract',
        'patient_data',
        'patient_card',
        'dir_list',
        'protect_code',
    )
    search_fields = ('num_contract',)


class ResDirectionsHistory(admin.ModelAdmin):
    raw_id_fields = (
        'direction',
        'old_card',
        'new_card',
    )
    list_display = (
        'direction_num',
        'old_fio_born',
        'new_fio_born',
        'date_change',
        'who_change',
    )
    search_fields = ('direction__pk',)

    def direction_num(self, obj):
        if obj.direction:
            return obj.direction.pk
        else:
            return ""


admin.site.register(TubesRegistration)
admin.site.register(Result)
admin.site.register(FrequencyOfUseResearches)
admin.site.register(CustomResearchOrdering)
admin.site.register(ExternalOrganization)
admin.site.register(RMISOrgs)
admin.site.register(RMISServiceInactive)
admin.site.register(Diagnoses, ResDiagnoses)
admin.site.register(TypeJob, ResTypeJob)
admin.site.register(EmployeeJob, ResEmployeeJob)
admin.site.register(KeyValue, ResKeyValue)
admin.site.register(PersonContract, ResPersonContract)
admin.site.register(DirectionsHistory, ResDirectionsHistory)
