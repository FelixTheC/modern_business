from django.db import models
from cms.models.pluginmodel import CMSPlugin


class Hello(CMSPlugin):
    guest_name = models.CharField(max_length=50, default='Guest')


class ArticleTitlePlugin(CMSPlugin):
    title = models.CharField(max_length=200, default='Article')

    def copy_relations(self, old_instance):
        self.associated_item.all().delete()
        for associated_item in old_instance.associated_item.all():
            associated_item.pk = None
            associated_item.plugin = self
            associated_item.save()

    def __str__(self):
        return self.title


class AssociatedItem(CMSPlugin):
    article = models.ForeignKey(ArticleTitlePlugin, related_name='associated_item')
    stock = models.IntegerField()

    def __str__(self):
        return self.article.title
