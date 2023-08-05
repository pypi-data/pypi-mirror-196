from django.contrib import admin
from djangoldp.admin import DjangoLDPAdmin
from .models import (
    Application,
)


# class EmptyAdmin(admin.ModelAdmin):
#     def get_model_perms(self, request):
#         return {}


class ApplicationAdmin(DjangoLDPAdmin):
    list_display = ("urlid", "friendly_name", "short_description")
    exclude = ("urlid", "slug", "is_backlink", "allow_create_backlink")
    # inlines = []
    search_fields = ["urlid", "friendly_name", "short_description"]
    ordering = ["slug"]


admin.site.register(Application, ApplicationAdmin)
