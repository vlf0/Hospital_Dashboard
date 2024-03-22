from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.cache import cache
from django.contrib import admin
from .models import Profiles, PlanNumbers
from .caching import Cacher
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

    def save_model(self, request, obj, form, change) -> None:
        """Override method so that perform renewing data in cache."""
        super().save_model(request, obj, form, change)
        profile_plan, created = PlanNumbers.objects.get_or_create(profile=obj, defaults={'active': obj.active,
                                                                                         'plan': 0})
        if not created:
            profile_plan.active = obj.active
            profile_plan.save()
        cache.delete('dmk')
        Cacher().dmk_cache()
        trigger_notification()


class PlanNumbersAdmin(admin.ModelAdmin):

    change_list_template = 'data/admin/change_list.html'

    def save_model(self, request, obj, form, change) -> None:
        """Override method so that perform renewing data in cache."""
        super().save_model(request, obj, form, change)
        cache.delete('dmk')
        Cacher().dmk_cache()
        trigger_notification()


admin.site.register(Profiles, ProfilesAdmin)
admin.site.register(PlanNumbers, PlanNumbersAdmin)


def trigger_notification():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'plan',
        {
            'type': 'send_notification',
            'message': 'Updated',
        }
    )

