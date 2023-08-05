import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from djangoldp.models import Model
from rest_framework.exceptions import ValidationError


class Application(Model):
    friendly_name = models.CharField(max_length=255, blank=True, null=True)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    creator = models.ForeignKey(
        get_user_model(),
        related_name="applications",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        try:
            return "{} ({})".format(self.friendly_name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        anonymous_perms = ["view"]
        authenticated_perms = ["inherit", "add"]
        auto_author = "creator"
        container_path = "/applications/"
        depth = 1  # Do not serialize user
        lookup_field = "slug"
        # nested_fields = []
        ordering = ["slug"]
        owner_field = "creator"
        owner_perms = ["inherit", "change", "delete"]
        rdf_context = {
            "friendly_name": "sib:friendlyName",
            "short_description": "sib:shortDescription",
            "creator": "foaf:user",
        }
        rdf_type = "sib:application"
        serializer_fields = [
            "@id",
            "friendly_name",
            "short_description",
            "creator",
        ]
        superuser_perms = ["view"]
        verbose_name = _("application")
        verbose_name_plural = _("applications")


@receiver(pre_save, sender=Application)
def pre_application_save(sender, instance, **kwargs):
    if not instance.urlid or instance.urlid.startswith(settings.SITE_URL):
        if getattr(instance, Model.slug_field(instance)) != slugify(
            instance.friendly_name
        ):
            if (
                Application.objects.local()
                .filter(slug=slugify(instance.friendly_name))
                .count()
                > 0
            ):
                raise ValidationError(_("Application name must be unique"))
            setattr(
                instance, Model.slug_field(instance), slugify(instance.friendly_name)
            )
            setattr(instance, "urlid", "")
    else:
        # Is a distant object, generate a random slug
        setattr(instance, Model.slug_field(instance), uuid.uuid4().hex.upper()[0:8])
