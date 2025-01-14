import pytest

from ..channel.utils import create_channel
from ..product.utils.preparing_product import prepare_product
from ..shipping_zone.utils import (
    create_shipping_method,
    create_shipping_method_channel_listing,
    create_shipping_zone,
)
from ..utils import assign_permissions
from ..warehouse.utils import create_warehouse
from .utils import (
    checkout_create,
    checkout_delivery_method_update,
    raw_checkout_complete,
)


def create_shop_for_orders_without_payments(
    e2e_staff_api_client,
    permission_manage_products,
    permission_manage_channels,
    permission_manage_product_types_and_attributes,
    permission_manage_shipping,
    permission_manage_orders,
    permission_manage_checkouts,
):
    channel_slug = "test-test"
    permissions = [
        permission_manage_products,
        permission_manage_channels,
        permission_manage_shipping,
        permission_manage_product_types_and_attributes,
        permission_manage_orders,
        permission_manage_checkouts,
    ]
    assign_permissions(e2e_staff_api_client, permissions)
    warehouse_data = create_warehouse(e2e_staff_api_client)
    warehouse_id = warehouse_data["id"]

    warehouse_ids = [warehouse_id]
    channel_data = create_channel(
        e2e_staff_api_client,
        slug=channel_slug,
        warehouse_ids=warehouse_ids,
        allow_unpaid_orders=True,
        automatically_confirm_all_new_orders=True,
    )
    channel_id = channel_data["id"]

    channel_ids = [channel_id]
    shipping_zone_data = create_shipping_zone(
        e2e_staff_api_client,
        warehouse_ids=warehouse_ids,
        channel_ids=channel_ids,
    )
    shipping_zone_id = shipping_zone_data["id"]

    shipping_method_data = create_shipping_method(
        e2e_staff_api_client, shipping_zone_id
    )
    shipping_method_id = shipping_method_data["id"]

    create_shipping_method_channel_listing(
        e2e_staff_api_client, shipping_method_id, channel_id
    )
    return channel_slug, warehouse_id, channel_id, shipping_method_id


@pytest.mark.e2e
def test_should_be_able_to_create_order_with_no_payment_CORE_0111(
    e2e_staff_api_client,
    permission_manage_products,
    permission_manage_channels,
    permission_manage_product_types_and_attributes,
    permission_manage_shipping,
    permission_manage_orders,
    permission_manage_checkouts,
):
    # Before
    (
        channel_slug,
        warehouse_id,
        channel_id,
        shipping_method_id,
    ) = create_shop_for_orders_without_payments(
        e2e_staff_api_client,
        permission_manage_products,
        permission_manage_channels,
        permission_manage_product_types_and_attributes,
        permission_manage_shipping,
        permission_manage_orders,
        permission_manage_checkouts,
    )

    product_variant_id = prepare_product(e2e_staff_api_client, warehouse_id, channel_id)

    assert shipping_method_id is not None

    # Step 1 - Create checkout.
    lines = [
        {"variantId": product_variant_id, "quantity": 1},
    ]
    checkout_data = checkout_create(
        e2e_staff_api_client,
        lines,
        channel_slug,
        email="testEmail@example.com",
        set_default_billing_address=True,
        set_default_shipping_address=True,
    )
    checkout_id = checkout_data["id"]

    assert checkout_data["isShippingRequired"] is True
    assert checkout_data["deliveryMethod"] is None
    assert checkout_data["shippingMethod"] is None
    shipping_method_id = checkout_data["shippingMethods"][0]["id"]

    # Step 2 - Set shipping address and DeliveryMethod for checkout
    checkout_data = checkout_delivery_method_update(
        e2e_staff_api_client,
        checkout_id,
        shipping_method_id,
    )
    assert checkout_data["deliveryMethod"]["id"] == shipping_method_id

    # Step 3 - Checkout complete results in the order creation
    data = raw_checkout_complete(e2e_staff_api_client, checkout_id)
    order_data = data["order"]
    assert order_data is not None
    assert order_data["id"] is not None
    assert order_data["isShippingRequired"] is True
    assert order_data["paymentStatus"] == "NOT_CHARGED"
    assert order_data["status"] == "UNCONFIRMED"
    assert order_data["isPaid"] is False

    errors = data["errors"]
    assert errors == []
