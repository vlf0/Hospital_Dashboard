from django.core.cache import cache
from django.shortcuts import redirect
from django.contrib import admin
from .models import Profiles, PlanNumbers
from .kis_data import ensure_cashing
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

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def save_model(self, request, obj, form, change) -> None:
        """Override method so that perform renewing data in cache."""
        super().save_model(request, obj, form, change)
        cache.delete('dmk')
        ensure_cashing()


class PlanNumbersAdmin(admin.ModelAdmin):

    change_list_template = 'data/admin/change_list.html'

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change) -> None:
        """Override method so that perform renewing data in cache."""
        super().save_model(request, obj, form, change)
        cache.delete('dmk')
        ensure_cashing()

    def add_view(self, request, form_url="", extra_context=None):
        self.update_plan_model()
        return redirect('/admin/data/plannumbers/')

    def update_plan_model(self):
        """
        Clean all data from accum model and create new set of row.

        Each New row is creating according each matched row from Profiles model.
        It allows maintained actuality of data, so you don't need thinking about this,
        because it is doing automatically.
        """
        PlanNumbers.objects.truncate_data()
        main_instances = Profiles.objects.all()
        for i in main_instances:
            PlanNumbers.objects.create(plan=0, profile_id=i.id)


admin.site.register(Profiles, ProfilesAdmin)
admin.site.register(PlanNumbers, PlanNumbersAdmin)
