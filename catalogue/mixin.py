import logging

from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import NoReverseMatch, reverse

from oscar.apps.checkout.signals import post_checkout
from oscar.core.loading import get_class, get_model

BillingAddress = get_model('order', 'BillingAddress')
ShippingAddress = get_model('order', 'ShippingAddress')
OrderPlacementMixin = get_class("checkout.mixins", "OrderPlacementMixin")
UserAddress = get_model('address', 'UserAddress')

class CustomOrderPlacementMixin(OrderPlacementMixin):
    """
    Mixin which provides functionality for placing orders.

    Any view class which needs to place an order should use this mixin.
    """
    # Any payment sources should be added to this list as part of the
    # handle_payment method.  If the order is placed successfully, then
    # they will be persisted. We need to have the order instance before the
    # payment sources can be saved.

    def update_address_book(self, user, addr):
        """
        Update the user's address book based on the new shipping address
        """
        
        try:
            user_addr = user.addresses.get(
                hash=addr.generate_hash())
        except ObjectDoesNotExist:
            # Create a new user address
            user_addr = UserAddress(user=user)
            addr.populate_alternative_model(user_addr) 
        if isinstance(addr, ShippingAddress):
            user_addr.num_orders_as_shipping_address += 1
        if isinstance(addr, BillingAddress):
            user_addr.num_orders_as_billing_address += 1
        user_addr.save()
