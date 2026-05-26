from django.contrib import admin
from .models import StatusModel, TableResto, Category, MenuResto, Order, OrderDetail
from import_export.admin import ImportExportModelAdmin

admin.site.register(StatusModel)
admin.site.register(TableResto)

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    pass

@admin.register(MenuResto)
class MenuRestoAdmin(ImportExportModelAdmin):
    pass

admin.site.register(Order)
admin.site.register(OrderDetail)
