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

class CustomProductDetailView(RedirectView):
    pattern_name="website:product_detail"  
       

         