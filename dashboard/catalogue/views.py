from dashboard.forms import ProductForm
from oscar.apps.dashboard.catalogue.views import ProductCreateUpdateView

class ProductCreateOrUpdateView(ProductCreateUpdateView):
    """
    View for create or update product
    """

    form_class = ProductForm