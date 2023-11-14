# oscar imports
import oscar.apps.dashboard.catalogue.apps as apps
from oscar.core.loading import get_class
from django.conf.urls import url


#local imports

class CatalogueDashboardConfig(apps.CatalogueDashboardConfig):
    name = 'dashboard.catalogue'

    def ready(self):
        
        super(CatalogueDashboardConfig, self).ready()
        from .views import ProductCreateOrUpdateView
        self.product_createupdate_view = ProductCreateOrUpdateView
        

    def get_urls(self):
        urls = super(CatalogueDashboardConfig, self).get_urls()
        urls += []
        return self.post_process_urls(urls)