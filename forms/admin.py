from django.contrib import admin

import forms.models as models
from django.forms import TextInput, Textarea
from django.db import models as dbmodels

class FormsTemplateInline(admin.TabularInline):
    model = models.FormsTemplate
    extra = 0
    formfield_overrides = {
        dbmodels.CharField: {'widget': TextInput(attrs={'size': '30'})},
        dbmodels.TextField: {'widget': Textarea(attrs={'rows': 10, 'cols': 85})},
    }

class ResFormsTemplate(admin.ModelAdmin):
    list_filter = ('form_name',)
    list_display = ('form_name','form_comment', 'section_name','is_print_section',)
    fields = [('form_name',), ('section_name','is_print_section',),'template_text']
    list_display_links = ('form_name',)

    formfield_overrides = {
        dbmodels.CharField: {'widget': TextInput(attrs={'size': '75'})},
        dbmodels.TextField: {'widget': Textarea(attrs={'rows': 12, 'cols': 125})},
    }
    def form_comment(self, obj):
        return obj.form_name.comment


class ResFormsList(admin.ModelAdmin):
    list_filter = ('form_group',)
    list_display = ('title','title_gui','form_group','type_number','is_hide')
    fields = [('form_group','type_number','is_hide',),('title',),('title_gui',),'comment']
    list_display_links = ('title','form_group',)

    formfield_overrides = {
        dbmodels.CharField: {'widget': TextInput(attrs={'size': '50'})},
    }
    inlines = [FormsTemplateInline]

class ResFormsGroup(admin.ModelAdmin):
    list_display = ('title','title_gui','is_hide')
    list_display_links = ('title',)

# Register your models here.
admin.site.register(models.FormsGroup,ResFormsGroup)
admin.site.register(models.FormsList,ResFormsList)
admin.site.register(models.FormsTemplate,ResFormsTemplate)
