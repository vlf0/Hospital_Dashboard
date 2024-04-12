from django.contrib import admin
from .models import Departments


class DepartmentsAdmin(admin.ModelAdmin):

    change_form_template = 'dashboard/admin/change_form.html'

    pass


admin.site.register(Departments, DepartmentsAdmin)

