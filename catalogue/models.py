from django.urls import reverse
# django imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# oscar import
from oscar.apps.catalogue.abstract_models import AbstractProduct

class Product(AbstractProduct):
    """
    extended product model
    """ 

    product_tagline = models.CharField(
        _('Product Tagline'),
        max_length=100,
        null=True,
        blank=True,
    )

    product_description = models.TextField(
        _('Product Description'),
        null=True,
        blank=True,
    )
    additional_information = models.TextField(
        _('Additional Information'),
        blank=True,
    )

    is_active = models.BooleanField(
        _('Active'),
        default=True,
    )

    product_title = models.CharField(
        _('Product Title'),
        max_length=100,
        null=True,
        blank=True,
    )
      
    

    @property
    def variants_list(self):
        product_list = []
        if self.is_parent:
            for prod in self.children.public().order_by('subscription_ordering'):
                stockrecord = prod.stockrecords.first()
                if hasattr(prod, 'stockrecords') and stockrecord and stockrecord.num_in_stock > 0:
                    product_list.append(prod)
        return product_list

    @property
    def percent_discount(self):
        discount = 0
        if hasattr(self, 'stockrecords') and self.stockrecords.first():
            stockrecord = self.stockrecords.first()
            price_retail = stockrecord.price_retail
            discount = ((price_retail - stockrecord.price_excl_tax)*100)/price_retail
            discount = round(discount)
        return discount    

    @property
    def get_complete_title(self):
        if self.structure == "child":
            name = f"{self.parent.title} {self.title}"
        else:
            name = self.title
        return name      

    @property
    def get_tag_line(self):
        if self.structure == "child":
            name = self.parent.tagline
        else:
            name = self.tagline
        return name



    def get_absolute_url(self):
        """
        Return a product's absolute URL
        """
        if self.structure == "child":
            return reverse('website:product_detail',
                       kwargs={'slug': self.parent.slug}) 
        return reverse('website:product_detail',
                       kwargs={'slug': self.slug}) 

      
    def clean_text_with_single_space(self,original_text):
        words = original_text.split()
        cleaned_text = " ".join(words)
        return cleaned_text
    
    @property
    def get_next_line_text(self):
        print(self.title)
        return self.clean_text_with_single_space(self.title)
    
from oscar.apps.catalogue.models import *  # noqa isort:skip
