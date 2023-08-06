"""
    This module is largely inspired by django-rest-framework settings.
    This module provides the `settings` object, that is used to access
    app settings, checking for user settings first, then falling
    back to the defaults.
"""
from typing import Any, Dict

from django.conf import settings
from django.test.signals import setting_changed
from django.utils.module_loading import import_string

SETTINGS_DOC = "https://gitlab.com/simpel-projects/simpel-sales/"

SIMPEL_SALES_DEFAULTS: Dict[str, Any] = {
    "CUSTOMER_MODEL": "django.contrib.auth.models.User",
    "CUSTOMER_ADDRESS_MODEL": None,
    # ORDER
    "ORDER_EXPIRATION_LIMIT": 1,
    "ORDER_RESOURCE": "simpel_sales.resources.SalesOrderResource",
    "ORDER_FORM": "simpel_sales.forms.SalesOrderForm",
    "ORDER_ADMIN": "simpel_sales.admin.SalesOrderAdmin",
    "ORDER_HANDLER": "simpel_sales.handlers.SalesOrderHandler",
    "ORDER_ABSOLUTE_URL_NAME": "dashboard_simpel_sales_salesorder_inspect",
    # QUOTATION
    "QUOTATION_EXPIRATION_LIMIT": 7,
    "QUOTATION_RESOURCE": "simpel_sales.resources.SalesQuotationResource",
    "QUOTATION_HANDLER": "simpel_sales.handlers.SalesQuotationHandler",
    "QUOTATION_FORM": "simpel_sales.forms.SalesQuotationForm",
    "QUOTATION_ADMIN": "simpel_sales.admin.SalesQuotationAdmin",
    "QUOTATION_ABSOLUTE_URL_NAME": "dashboard_simpel_sales_salesquotation_inspect",
    # INVOICE
    "PROFORMA_ADMIN": "simpel_sales.admin.ProformaAdmin",
    "INVOICE_EXPIRATION_LIMIT": 7,
    "INVOICE_RESOURCE": "simpel_sales.resources.InvoiceResource",
    "INVOICE_HANDLER": "simpel_sales.handlers.InvoiceHandler",
    "INVOICE_ADMIN": "simpel_sales.admin.InvoiceAdmin",
    "INVOICE_ABSOLUTE_URL_NAME": "dashboard_simpel_sales_invoice_inspect",
}

# List of settings that may be in string import notation.
IMPORT_STRINGS = [
    "CUSTOMER_MODEL",
    "ORDER_RESOURCE",
    "CUSTOMER_ADDRESS_MODEL",
    "ORDER_FORM",
    "ORDER_HANDLER",
    "ORDER_ADMIN",
    "QUOTATION_FORM",
    "QUOTATION_HANDLER",
    "QUOTATION_ADMIN",
    "QUOTATION_RESOURCE",
    "PROFORMA_ADMIN",
    "INVOICE_HANDLER",
    "INVOICE_ADMIN",
    "INVOICE_RESOURCE",
]

# List of settings that have been removed
REMOVED_SETTINGS = []


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, str):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    elif isinstance(val, dict):
        return {key: import_from_string(item, setting_name) for key, item in val.items()}
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        return import_string(val)
    except ImportError as e:
        msg = "Could not import '%s' for SIMPEL_SALES setting '%s'. %s: %s." % (
            val,
            setting_name,
            e.__class__.__name__,
            e,
        )
        raise ImportError(msg)


class AppSettings:
    """
    This module is largely inspired by django-rest-framework settings.
    This module provides the `sales_settings` object, that is used to access
    app settings, checking for user settings first, then falling
    back to the defaults.
    """

    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)
        self.defaults = defaults or SIMPEL_SALES_DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, "SIMPEL_SALES", {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid SIMPEL_SALES settings: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def __check_user_settings(self, user_settings):
        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                raise RuntimeError(
                    "The '%s' setting has been removed. Please refer to '%s' for available settings."
                    % (setting, SETTINGS_DOC)
                )
        return user_settings

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, "_user_settings"):
            delattr(self, "_user_settings")


sales_settings = AppSettings(None, SIMPEL_SALES_DEFAULTS, IMPORT_STRINGS)


def reload_sales_settings(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == "SIMPEL_SALES":
        sales_settings.reload()


setting_changed.connect(reload_sales_settings)
