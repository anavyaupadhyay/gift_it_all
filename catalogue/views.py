# django imports
from django.urls import reverse
from django.views.generic import (
    ListView,
    TemplateView,
    FormView,
    RedirectView,
)

from oscar.apps.catalogue.views import (
    CatalogueView,
    ProductCategoryView,
    ProductDetailView,
)

from django.http import HttpResponseRedirect

class ProductListView(RedirectView):
    pattern_name="website:product_list"

class CustomProductDetailView(ProductDetailView):
    """
    A view for display all the product in a website
    """
    # template_name = 'catalogue/detail.html'
    template_name = 'website/product_detail.html'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'

    def dispatch(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('website:product_list'))    
       

         