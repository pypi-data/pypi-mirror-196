from django.contrib import admin
from djangoldp.admin import DjangoLDPAdmin
from .models import (
    Application,
    ApplicationTemplate,
    TemplateRequiredPackage,
    TemplateRequiredComponent,
    Federation,
    ApplicationComponent,
)


class EmptyAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


class TemplateRequiredPackageInline(admin.TabularInline):
    model = TemplateRequiredPackage
    exclude = ("urlid", "is_backlink", "allow_create_backlink")
    extra = 0


class TemplateRequiredComponentPackageInline(admin.TabularInline):
    model = TemplateRequiredComponent
    exclude = ("urlid", "is_backlink", "allow_create_backlink")
    extra = 0


class ApplicationTemplateAdmin(DjangoLDPAdmin):
    list_display = ("urlid", "friendly_name", "short_description")
    exclude = ("urlid", "slug", "is_backlink", "allow_create_backlink")
    inlines = [TemplateRequiredComponentPackageInline, TemplateRequiredPackageInline]
    search_fields = ["urlid", "friendly_name", "short_description"]
    ordering = ["slug"]


class ApplicationComponentInline(admin.TabularInline):
    model = ApplicationComponent
    exclude = ("urlid", "is_backlink", "allow_create_backlink")
    extra = 0


class FederationInline(admin.TabularInline):
    model = Federation
    fk_name = "application"
    exclude = ("urlid", "is_backlink", "allow_create_backlink")
    extra = 0


class ApplicationAdmin(DjangoLDPAdmin):
    list_display = ("urlid", "friendly_name", "short_description")
    exclude = ("urlid", "slug", "is_backlink", "allow_create_backlink")
    inlines = [ApplicationComponentInline, FederationInline]
    search_fields = ["urlid", "friendly_name", "short_description"]
    ordering = ["slug"]


admin.site.register(Application, ApplicationAdmin)
admin.site.register(ApplicationTemplate, ApplicationTemplateAdmin)
admin.site.register(TemplateRequiredPackage, EmptyAdmin)
admin.site.register(TemplateRequiredComponent, EmptyAdmin)
admin.site.register(Federation, EmptyAdmin)
admin.site.register(ApplicationComponent, EmptyAdmin)
