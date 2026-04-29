from django.contrib import admin
from .models import StatusModel, TableResto, Category, MenuResto
from import_export.admin import ImportExportModelAdmin

admin.site.register(StatusModel)
admin.site.register(TableResto)

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    pass

@admin.register(MenuResto)
class MenuRestoAdmin(ImportExportModelAdmin):
    pass
