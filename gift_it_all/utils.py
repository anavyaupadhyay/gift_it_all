# inner app imports
from basket.models import Basket
# third party imports
from rest_framework.relations import HyperlinkedRelatedField
from rest_framework import exceptions

from django.core.exceptions import ValidationError

def parse_basket_from_hyperlink(DATA, format):  # pylint: disable=redefined-builtin
    "Parse basket from relation hyperlink"
    basket_parser = HyperlinkedRelatedField(
        view_name="catalogue:basket-detail", queryset=Basket.objects, format=format
    )
    try:
        basket_uri = DATA.get("basket")
        data_basket = basket_parser.to_internal_value(basket_uri)
    except ValidationError as e:
        raise exceptions.NotAcceptable(e.messages)
    else:
        return data_basket