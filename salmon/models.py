from django.db import models
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType


class SubscriptionManager(models.Manager):

    def subscribe(self, obj, endpoint):
        content_type = ContentType.objects.get_for_model(obj)
        return Subscription.objects.create(
            content_type=content_type,
            object_id=obj.id,
            salmon_endpoint=endpoint)

    def unsubscribe(self, obj):
        subscription = self.get_for_object(obj)
        if subscription:
            subscription.delete()

    def get_for_object(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        print content_type
        print obj.id
        try:
            sub = Subscription.objects.get(
                content_type=content_type, object_id=obj.id)
            return sub
        except Subscription.DoesNotExist:
            return None


class Subscription(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    salmon_endpoint = models.URLField()

    objects = SubscriptionManager()

    def __unicode__(self):
        obj = self.content_type.get_object_for_this_type(id=self.object_id)
        return u":".join((
            obj.__class__.__name__,
            unicode(obj), self.salmon_endpoint))

    def get_object(self):
        cls = self.content_type.model_class()
        return cls.objects.get(id=self.object_id)
admin.site.register(Subscription)
