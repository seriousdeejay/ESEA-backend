from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (CustomUser, StakeholderGroup, Network, Organisation, Respondent, Method, Survey, Section, TextFragment,
                     Topic, DirectIndicator, IndirectIndicator, Question, QuestionOption, AnswerOption, SurveyResponse, QuestionResponse, Campaign, EseaAccount)


class NetworkAdmin(admin.ModelAdmin):
    readonly_fields = ['created_by']
    
    def get_form(self, request, obj=None, **kwargs):
        Network.created_by = request.user
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.created_by_id = request.user.id
        obj.last_modified_by = request.user
        obj.save()

admin.site.register(CustomUser, UserAdmin)
admin.site.register(StakeholderGroup)
admin.site.register(Network, NetworkAdmin)
admin.site.register(EseaAccount)
admin.site.register(Organisation)
admin.site.register(Respondent)

admin.site.register(Method)
admin.site.register(Survey)
admin.site.register(Section)
admin.site.register(TextFragment)
admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(QuestionOption)
admin.site.register(AnswerOption)
admin.site.register(DirectIndicator)
admin.site.register(IndirectIndicator)

admin.site.register(Campaign)
admin.site.register(SurveyResponse)
admin.site.register(QuestionResponse)
