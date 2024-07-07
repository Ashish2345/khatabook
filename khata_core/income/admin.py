from django.contrib import admin

from .models import Asset, AssetCategory, Depreciation


@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("category", "name", "value", "purchase_date")
    list_filter = ("category", "purchase_date")
    search_fields = ("name", "description")


@admin.register(Depreciation)
class DepreciationAdmin(admin.ModelAdmin):
    list_display = ("asset", "value", "date")
    list_filter = ("asset", "date")
    search_fields = ("description",)
