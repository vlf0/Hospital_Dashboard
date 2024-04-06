from django.contrib import messages
from django.urls import reverse
from django.contrib import admin
from django.shortcuts import redirect
from .kis_data import KISData, QuerySets
from .models import Profiles, PlanNumbers
from .caching import Cacher
from .consumers import trigger_notification
from .forms import KISProfileChosingForm
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

    # change_list_template = 'data/admin/change_list.html'
    change_form_template = 'data/admin/change_form.html'

    fieldsets = (
        (None, {
            'fields': ('name',),
        }),
    )

    def change_view(self, request, object_id, form_url="", extra_context=None):
        """Pass custom ModelForm of external model."""
        extra_context = extra_context or {}
        extra_context['kis_profiles'] = KISProfileChosingForm()
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def add_view(self, request, form_url="", extra_context=None):
        """Pass custom ModelForm of external model."""
        extra_context = extra_context or {}
        extra_context['kis_profiles'] = KISProfileChosingForm()
        return super().add_view(request, form_url, extra_context=extra_context)

    def save_model(self, request, obj, form, change) -> None:
        """Override method so that perform renewing data in cache."""
        obj_id, obj_name = request.POST.get('id'), request.POST.get('name')
        change_url = reverse('admin:data_profiles_change', args=(obj_id,))
        method_type = request.path.split('/')[-2]
        existing_profiles = Profiles.objects.all()
        profiles_ids = [profile.profile_id for profile in existing_profiles]
        try:
            obj_id = int(obj_id)
        except ValueError:
            self.send_message(request, obj_id)
            return redirect(change_url)

        if method_type == 'add':
            if obj_id in profiles_ids:
                self.send_message(request, obj_id)
                return redirect(change_url)
            obj.profile_id = obj_id
        elif method_type == 'change':
            obj.name = obj_name
        super().save_model(request, obj, form, change)
        PlanNumbers.objects.get_or_create(profile=obj, defaults={'profile': obj, 'plan': 0})
        Cacher().dmk_cache()
        trigger_notification()

    def delete_model(self, request, obj) -> None:
        super().delete_model(request, obj)
        Cacher().dmk_cache()
        trigger_notification()

    @staticmethod
    def send_message(request, obj_id):
        message = messages.error(request, f"A profile with ID {obj_id} already exists.")
        return message


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

