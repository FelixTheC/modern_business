from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .admin import AssociatedAdmin
from django.utils.translation import ugettext_lazy as _

from .models import Hello, ArticleTitlePlugin, AssociatedItem


class HelloPlugin(CMSPluginBase):
    model = Hello
    name = _("Hello Plugin")
    render_template = "hello_plugin.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super(HelloPlugin, self).render(context, instance, placeholder)
        return context


class AssociatedPlugin(CMSPluginBase):
    model = AssociatedItem
    name = _('Associated Plugin')
    render_template = 'hello_plugin.html'
    cache = False
    
    def render(self, context, instance, placeholder):
        return super(AssociatedPlugin, self).render(context, instance, placeholder)


class ArticleTitlePlugin(CMSPluginBase):
    model = ArticleTitlePlugin
    name = _('Article Title')
    render_template = 'hello_plugin.html'
    cache = False
    inlines = AssociatedAdmin

    def render(self, context, instance, placeholder):
        return super(ArticleTitlePlugin, self).render(context, instance, placeholder)


plugin_pool.register_plugin(HelloPlugin)
plugin_pool.register_plugin(AssociatedPlugin)
plugin_pool.register_plugin(ArticleTitlePlugin)
