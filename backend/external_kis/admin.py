from django.contrib import admin
from .models import KISProfiles


class KISProfilesAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in obj._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # Override method for get filtered queryset
    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     return queryset.filter()


admin.site.register(KISProfiles, KISProfilesAdmin)
