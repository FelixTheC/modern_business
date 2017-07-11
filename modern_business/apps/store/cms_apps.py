from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class StoreApp(CMSApp):
    name = _('Store-App')
    app_name = 'store'
    _urls = ['modern_business.apps.store.urls', ]

    #def get_urls(self, page=None, language=None, **kwargs):
     #   return ['modern_business.apps.store.urls']


apphook_pool.register(StoreApp)
