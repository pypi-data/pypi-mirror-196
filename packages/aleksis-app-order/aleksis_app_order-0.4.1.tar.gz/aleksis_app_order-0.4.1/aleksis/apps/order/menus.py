from django.utils.translation import ugettext_lazy as _

MENUS = {
    "NAV_MENU_CORE": [
        {
            "name": _("Orders"),
            "url": "#",
            "svg_icon": "mdi:cart-outline",
            "vuetify_icon": "mdi-cart-outline",
            "root": True,
            "validators": [
                (
                    "aleksis.core.util.predicates.permission_validator",
                    "order.show_menu",
                ),
            ],
            "submenu": [
                {
                    "name": _("My digital products"),
                    "url": "digital_products",
                    "svg_icon": "mdi:download",
                    "vuetify_icon": "mdi-download",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "order.view_my_digital_products",
                        ),
                    ],
                },
                {
                    "name": _("List"),
                    "url": "list_orders",
                    "svg_icon": "mdi:receipt-outline",
                    "vuetify_icon": "mdi-receipt-outline",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "order.view_orders",
                        ),
                    ],
                },
                {
                    "name": _("Pick up"),
                    "url": "pick_up_order",
                    "svg_icon": "mdi:receipt-outline",
                    "vuetify_icon": "mdi-receipt-outline",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "order.view_orders",
                        ),
                    ],
                },
            ],
        }
    ]
}
