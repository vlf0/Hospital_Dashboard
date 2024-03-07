from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.cache import cache
from django.shortcuts import redirect
from django.contrib import admin
from django.conf import settings
from .models import Profiles, PlanNumbers
from .kis_data import ensure_cashing
from .consumers import NotificationConsumer
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
        trigger_notification()

    def add_view(self, request, form_url="", extra_context=None):
        """Call custom function and make you stay on the same page."""
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


def trigger_notification():
    channel_layer = get_channel_layer()
    print(channel_layer)
    async_to_sync(channel_layer.group_send)(
        'test',
        {
            'type': 'test.send_notification',
            # 'message': 'Notification from trigger_notification',
        }
    )
    print('ok')
