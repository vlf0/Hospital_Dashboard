from django.contrib import admin
from .models import Profiles, PlanNumbers
from .caching import Cacher
from .consumers import trigger_notification
from django_celery_beat.models import (
    IntervalSchedule,
    CrontabSchedule,
    SolarSchedule,
    ClockedSchedule,
    PeriodicTask,
)

admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)


class ProfilesAdmin(admin.ModelAdmin):

    change_list_template = 'data/admin/change_list.html'
    change_form_template = 'data/admin/change_form.html'

    # def change_view(self, request, object_id, form_url="", extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['kis_profiles'] = KISProfileChosingForm(initial={'id': 1, 'name': 'test'})
    #     return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def save_model(self, request, obj, form, change) -> None:
        """Override method so that perform renewing data in cache."""
        super().save_model(request, obj, form, change)
        PlanNumbers.objects.get_or_create(profile=obj, defaults={'profile': obj, 'plan': 0})
        Cacher().dmk_cache()
        trigger_notification()

    def delete_model(self, request, obj) -> None:
        super().delete_model(request, obj)
        Cacher().dmk_cache()
        trigger_notification()


class PlanNumbersAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change) -> None:
        """Override method so that perform renewing data in cache."""
        super().save_model(request, obj, form, change)
        Cacher().dmk_cache()
        trigger_notification()

    def delete_model(self, request, obj) -> None:
        super().delete_model(request, obj)
        Cacher().dmk_cache()
        trigger_notification()


admin.site.register(Profiles, ProfilesAdmin)
admin.site.register(PlanNumbers, PlanNumbersAdmin)

