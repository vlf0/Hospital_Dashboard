from django.contrib import admin
from .models import Departments


class DepartmentsAdmin(admin.ModelAdmin):

    # change_list_template = 'observer/admin/change_list.html'
    pass


admin.site.register(Departments, DepartmentsAdmin)

