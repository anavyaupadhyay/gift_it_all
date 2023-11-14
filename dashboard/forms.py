# oscar imports
from oscar.apps.dashboard.catalogue import forms as base_forms

from django import forms

from catalogue.models import Product

class ProductForm(base_forms.ProductForm):
    """
    Customized Product Form
    """

    class Meta(base_forms.ProductForm.Meta):
        fields = (
            'title',
            'slug',
            'upc',
            'product_title',
            'product_tagline',
            'product_description',
            'additional_information',
            'is_active'
        )

    def clean_slug(self):
        slug = self.cleaned_data.get('slug', None)
        if (slug and self.instance.pk and Product.objects.filter(slug=slug).exclude(id=self.instance.id).exists()) or not self.instance.id and Product.objects.filter(slug=slug).exists():
            raise forms.ValidationError('A Product with this slug is already exists')
        return slug