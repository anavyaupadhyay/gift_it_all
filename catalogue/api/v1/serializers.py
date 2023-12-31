# third-party imports
from rest_framework import serializers,exceptions

# inter-app imports
from catalogue.models import (
    Product,
    Category,
    Option
)
from basket.models import Basket
# oscar imports
from oscarapi.serializers import basket as corebasket
from oscarapi.serializers import checkout as corecheckout
from oscarapi.serializers.fields import (
    DrillDownHyperlinkedIdentityField,
    DrillDownHyperlinkedRelatedField,
)
from oscar.core.loading import get_class, get_model

# django imports
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()
Order = get_model("order", "Order")
OrderLine = get_model("order", "Line")
Voucher = get_model("voucher", "Voucher")
ShippingAddress = get_model("order", "ShippingAddress")
BillingAddress = get_model("order", "BillingAddress")
StockRecord = get_model("partner", "StockRecord")

class ChildProductSerializer(serializers.ModelSerializer):
    """
    serializer for child product
    """
    selling_price = serializers.SerializerMethodField()
    retail_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'structure',
            'selling_price',
            'retail_price',
            'description',
        )

    def get_selling_price(self, obj):
        if obj.has_stockrecords:
            selling_price = obj.stockrecords.first().price_excl_tax
            return selling_price
        return None

    def get_retail_price(self, obj):
        if obj.has_stockrecords:
            retail_price = obj.stockrecords.first().price_retail
            return retail_price
        return None    


class ProductListSerializer(serializers.ModelSerializer):
    """
    serializer for blog list
    """

    image = serializers.SerializerMethodField()
    selling_price = serializers.SerializerMethodField()
    retail_price = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()
    image_list = serializers.SerializerMethodField()
    # categories = CategorySerializer(many=True, read_only=True)
    stock_record = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name='catalogue:product_detail',
    )

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'structure',
            'image',
            'categories',
            'selling_price',
            'retail_price',
            'description',
            'product_rating',
            'product_rating_count',
            'detail_url',
            'attribute_summary',
            'image_list',
            'additional_information',
            'ingredients',
            'benefits',
            'stock_record',
            'url',
            'children',
        )

        read_only_fields = (
            'id',
            'image',
            'structure',
            'selling_price',
            'retail_price',
            'detail_url',
            'attribute_summary',
            'image_list',
            'stock_record',
            'children',
        )

    def get_image(self, obj):
        image = obj.primary_image()
        if hasattr(image, 'original'):
            return image.original.url
        return None

    def get_image_list(self, obj):
        image_list = obj.get_all_images()
        images_list = []
        for obj in image_list:
            image_dict = {
                'image': obj.original.url,
                'caption': obj.caption,
                'display_order': obj.display_order,
            }
            images_list.append(image_dict)
        return images_list

    def get_stock_record(self, obj):
        stock_record_list = []
        stock_list = obj.stockrecords.all()
        for obj in stock_list:
            stock_dict = {
                'partner_sku': obj.partner_sku,
                'num_in_stock': obj.num_in_stock,
                'num_allocated': obj.num_allocated,
                'low_stock_threshold': obj.low_stock_threshold,
            }
            stock_record_list.append(stock_dict)
        return stock_record_list

    def get_selling_price(self, obj):
        if obj.has_stockrecords:
            selling_price = obj.stockrecords.first().price_excl_tax
            return selling_price
        return None

    def get_retail_price(self, obj):
        if obj.has_stockrecords:
            retail_price = obj.stockrecords.first().price_retail
            return retail_price
        return None

    def get_detail_url(self, obj):
        if obj.has_stockrecords:
            detail_url = obj.get_absolute_url()
            return detail_url
        return None

    def to_representation(self, instance):
        self.fields['children'] = ChildProductSerializer(many=True)
        return super(ProductListSerializer, self).to_representation(instance)    


class CategorySerializer(serializers.ModelSerializer):
    """
    category serializer
    """
    product_set = ProductListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'description',
            'image',
            'icon',
            'product_set',
        )

        read_only_fields = (
            'id',
        )


class BasketSerializer(corebasket.BasketSerializer):
    """
    customised basket serializer
    """
    owner = serializers.HyperlinkedRelatedField(
        view_name="customer:custom_user-detail",
        required=False,
        allow_null=True,
        queryset=User.objects.all(),
    )

    lines = serializers.HyperlinkedIdentityField(view_name="catalogue:basket-lines-list")

    url = serializers.HyperlinkedIdentityField(
        view_name='catalogue:basket-detail',
    )

    class Meta(corebasket.BasketSerializer.Meta):
        fields = (
            "id",
            "owner",
            "status",
            "lines",
            "url",
            "total_excl_tax",
            "total_excl_tax_excl_discounts",
            "total_incl_tax",
            "total_incl_tax_excl_discounts",
            "total_tax",
            "currency",
            "voucher_discounts",
            "offer_discounts",
            "is_tax_known",
        )


class BasketLineSerializer(corebasket.BasketLineSerializer):
    """
    Customised basket line serializer
    """

    url = DrillDownHyperlinkedIdentityField(
        view_name="catalogue:basket-line-detail", extra_url_kwargs={"basket_pk": "basket.id"}
    )

    product = serializers.HyperlinkedRelatedField(
        view_name="catalogue:product_detail",
        required=False,
        allow_null=True,
        queryset=Product.objects.all(),
    )

    basket = serializers.HyperlinkedIdentityField(
        view_name='catalogue:basket-detail',
    )

    product_detail = serializers.SerializerMethodField(read_only=True)

    class Meta(corebasket.BasketLineSerializer.Meta):
        fields = (
            "url",
            "product",
            "quantity",
            "attributes",
            "price_currency",
            "price_excl_tax",
            "price_incl_tax",
            "price_incl_tax_excl_discounts",
            "price_excl_tax_excl_discounts",
            "is_tax_known",
            "warning",
            "basket",
            # "stockrecord",
            "date_created",
            "date_updated",
            "product_detail",
        )

    def get_product_detail(self, obj):
        if obj.product:
            product_image = obj.product.primary_image()
            if hasattr(product_image, 'original'):
                image = product_image.original.url
            else:
                image = None
            data = {
                'title': obj.product.title,
                'description': obj.product.description,
                'image': image,
            }
            
            if obj.product.has_stockrecords:
                selling_price = obj.product.stockrecords.first().price_excl_tax
                retail_price = obj.product.stockrecords.first().price_retail
                data['selling_price'] = selling_price
                data['retail_price'] = retail_price
            image_list = obj.product.get_all_images()
            images_list = []
            for obj in image_list:
                image_dict = {
                    'image': obj.original.url,
                    'caption': obj.caption,
                    'display_order': obj.display_order,
                }
                images_list.append(image_dict)
            if len(images_list) > 0:
                data['images_list'] = images_list
            return data
        return None


class OptionValueSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    option = serializers.HyperlinkedRelatedField(
        view_name="option-detail", queryset=Option.objects
    )
    value = serializers.CharField()


class CustomAddProductSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Serializes and validates an add to basket request.
    """

    quantity = serializers.IntegerField(required=True)
    # url = serializers.HyperlinkedRelatedField(
    #     view_name="catalogue:product_detail", queryset=Product.objects, required=True
    # )
    # options = OptionValueSerializer(many=True, required=False)
    quantity = serializers.IntegerField(required=True)
    url = serializers.HyperlinkedRelatedField(
        view_name="product-detail", queryset=Product.objects, required=True
    )
    options = OptionValueSerializer(many=True, required=False) 


class OrderSerializer(corecheckout.OrderSerializer):
    """
    The order serializer tries to have the same kind of structure as the
    basket. That way the same kind of logic can be used to display the order
    as the basket in the checkout process.
    """
    owner = serializers.HyperlinkedRelatedField(
        view_name="customer:custom_user-detail", read_only=True, source="user"
    )
    lines = serializers.HyperlinkedIdentityField(view_name="catalogue:order_lines_list_api")
    url = serializers.HyperlinkedIdentityField(
        view_name='catalogue:order_detail_api',
    )
    basket = serializers.HyperlinkedRelatedField(
        view_name='catalogue:basket-detail', read_only=True,
    )

    class Meta(corecheckout.OrderSerializer.Meta):
        fields = (
            "id",
            "number",
            "basket",
            "url",
            "lines",
            "owner",
            "billing_address",
            "currency",
            "total_incl_tax",
            "total_excl_tax",
            "shipping_incl_tax",
            "shipping_excl_tax",
            "shipping_address",
            "shipping_method",
            "shipping_code",
            "status",
            "email",
            "date_placed",
            # "payment_url",
            "offer_discounts",
            "voucher_discounts",
            "surcharges",
            "payment_done",
            "transaction_number",
            "payment_mode",
            "is_shiprocket_order_processed"
        )
        read_only_fields = (
            'id',
        )



OrderTotalCalculator = get_class("checkout.calculators", "OrderTotalCalculator")
from oscar.core import prices
from oscarapi.basket.operations import assign_basket_strategy
from django.conf import settings
from catalogue.mixin import CustomOrderPlacementMixin
from decimal import Decimal as D
class CheckoutSerializer(CustomOrderPlacementMixin, corecheckout.CheckoutSerializer):
    """
    Custom checkout serializer
    """
    basket = serializers.HyperlinkedRelatedField(
        view_name="catalogue:basket-detail", queryset=Basket.objects
    )
    def validate(self, attrs):
        request = self.request

        if request.user.is_anonymous:
            if not settings.OSCAR_ALLOW_ANON_CHECKOUT:
                message = _("Anonymous checkout forbidden")
                raise serializers.ValidationError(message)

            if not attrs.get("guest_email"):
                # Always require the guest email field if the user is anonymous
                message = _("Guest email is required for anonymous checkouts")
                raise serializers.ValidationError(message)
        else:
            if "guest_email" in attrs:
                # Don't store guest_email field if the user is authenticated
                del attrs["guest_email"]

        basket = attrs.get("basket")
        basket = assign_basket_strategy(basket, request)
        if basket.num_items <= 0:
            message = _("Cannot checkout with empty basket")
            raise serializers.ValidationError(message)
   
        shipping_method = self._shipping_method(
            request,
            basket,
            attrs.get("shipping_method_code"),
            attrs.get("shipping_address"),
        )
        shipping_charge = shipping_method.calculate(basket)
        posted_shipping_charge = attrs.get("shipping_charge")

        # if posted_shipping_charge is not None:
        #     posted_shipping_charge = prices.Price(**posted_shipping_charge)
        #     # test submitted data.
        #     if not posted_shipping_charge == shipping_charge:
        #         message = _(
        #             "Shipping price incorrect %s != %s"
        #             % (posted_shipping_charge, shipping_charge)
        #         )
        #         raise serializers.ValidationError(message)

        posted_total = attrs.get("total")
        total = OrderTotalCalculator().calculate(basket, shipping_charge)
        # if posted_total is not None:
        #     if posted_total != total.incl_tax:
        #         message = _("Total incorrect %s != %s" % (posted_total, total.incl_tax))
        #         raise serializers.ValidationError(message)

        # update attrs with validated data.
        total_amount=0
        if total.incl_tax<1000 :
            tax_amount = D('100.00')

            # Calculate the updated inclusive tax value
            updated_incl_tax = total.incl_tax + tax_amount

            # Create a new Price object with the updated inclusive tax
            total = prices.Price(
                currency=basket.currency,
                excl_tax=total.excl_tax,
                incl_tax=updated_incl_tax, 
                tax=tax_amount
            )
        attrs["order_total"] = total
        attrs["shipping_method"] = shipping_method
        attrs["shipping_charge"] = shipping_charge  
        attrs["basket"] = basket
        return attrs

    def create(self, validated_data):
        
        try:
            basket = validated_data.get("basket")
            order_number = self.generate_order_number(basket)
            request = self.request
            
            if "shipping_address" in validated_data:
                shipping_address = ShippingAddress(**validated_data["shipping_address"])
            else:
                shipping_address = None

            if "billing_address" in validated_data:
                billing_address = BillingAddress(**validated_data["billing_address"])
            else:
                billing_address = None
            
            return self.place_order(
                order_number=order_number,
                user=request.user,
                basket=basket,
                shipping_address=shipping_address,
                shipping_method=validated_data.get("shipping_method"),
                shipping_charge=validated_data.get("shipping_charge"),
                billing_address=billing_address,
                order_total=validated_data.get("order_total"),
                guest_email=validated_data.get("guest_email") or "",
            )
        except ValueError as e:
            raise exceptions.NotAcceptable(str(e))


class OrderLineSerializer(corecheckout.OrderLineSerializer):
    "This serializer renames some fields so they match up with the basket"

    url = serializers.HyperlinkedIdentityField(view_name="catalogue:order_lines_detail_api")
    order = serializers.HyperlinkedRelatedField(view_name="catalogue:order_detail_api", queryset=Order.objects.all())
    product = serializers.HyperlinkedRelatedField(view_name="catalogue:product_detail", queryset=Product.objects.all())
    attributes = corecheckout.OrderLineAttributeSerializer(
        many=True, fields=("url", "option", "value"), required=False
    )
    price_currency = serializers.CharField(source="order.currency", max_length=12)
    price_excl_tax = serializers.DecimalField(
        decimal_places=2, max_digits=12, source="line_price_excl_tax"
    )
    price_incl_tax = serializers.DecimalField(
        decimal_places=2, max_digits=12, source="line_price_incl_tax"
    )
    price_incl_tax_excl_discounts = serializers.DecimalField(
        decimal_places=2, max_digits=12, source="line_price_before_discounts_incl_tax"
    )
    price_excl_tax_excl_discounts = serializers.DecimalField(
        decimal_places=2, max_digits=12, source="line_price_before_discounts_excl_tax"
    )
    stockrecord = DrillDownHyperlinkedRelatedField(
        view_name="product-stockrecord-detail",
        extra_url_kwargs={"product_pk": "product_id"},
        queryset=StockRecord.objects.all(),
    )
    product_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderLine
        fields = (
            "attributes",
            "url",
            "product",
            "stockrecord",
            "quantity",
            "price_currency",
            "price_excl_tax",
            "price_incl_tax",
            "price_incl_tax_excl_discounts",
            "price_excl_tax_excl_discounts",
            "order",
            "product_detail",
        )

    def get_product_detail(self, obj):
        if obj.product:
            product_image = obj.product.primary_image()
            if hasattr(product_image, 'original'):
                image = product_image.original.url
            else:
                image = None
            data = {
                'title': obj.product.title,
                'description': obj.product.description,
                'image': image,
            }
            if obj.product.has_stockrecords:
                selling_price = obj.product.stockrecords.first().price_excl_tax
                retail_price = obj.product.stockrecords.first().price_retail
                data['selling_price'] = selling_price
                data['retail_price'] = retail_price
            image_list = obj.product.get_all_images()
            images_list = []
            for obj in image_list:
                image_dict = {
                    'image': obj.original.url,
                    'caption': obj.caption,
                    'display_order': obj.display_order,
                }
                images_list.append(image_dict)
            if len(images_list) > 0:
                data['images_list'] = images_list
            return data
        return None


class OrderUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for update order
    """

    url = serializers.HyperlinkedIdentityField(
        view_name='catalogue:order_detail_api',
    )

    class Meta:
        model = Order
        fields = (
            'id',
            'url',
            'status',
            'payment_done',
            'transaction_number',
        )

        read_only_fields = (
            'id',
            'url',
        )

    def validate_status(self, status):
        order = self.instance
        new_status = status
        if not new_status:
            raise serializers.ValidationError('The new status {} is not valid'.format(new_status))
        elif new_status not in order.available_statuses():
            raise serializers.ValidationError('The new status {} is not valid for'.format(new_status))
        else:
            return status


class VoucherRemoveSerializer(serializers.Serializer):
    """
    Serializer for remove voucher from cart
    """
    vouchercode = serializers.CharField(max_length=128, required=True)

    def validate(self, attrs):
        # oscar expects this always to be uppercase.
        attrs["vouchercode"] = attrs["vouchercode"].upper()
        request = self.context.get("request")
        try:
            voucher = request.basket.vouchers.get(code=attrs.get("vouchercode"))
        except Voucher.DoesNotExist:
            raise serializers.ValidationError(_("No voucher found with this code in a basket"))
        self.instance = voucher
        return attrs

