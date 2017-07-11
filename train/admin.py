from django.contrib import admin
from .models import ArticleTitlePlugin, AssociatedItem


class AssociatedAdmin(admin.StackedInline):
    model = AssociatedItem


admin.site.register(ArticleTitlePlugin)
admin.site.register(AssociatedItem)
