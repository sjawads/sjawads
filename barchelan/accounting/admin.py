from django.contrib import admin

from . import models


@admin.register(models.AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "account_type")
    list_filter = ("account_type",)
    search_fields = ("name",)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(models.License)
class LicenseAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(models.Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("name", "account", "calculation_type", "contract_date", "is_closed")
    list_filter = ("calculation_type", "is_closed")
    search_fields = ("name", "account__name")


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "contract", "invoice_date", "is_complete")
    list_filter = ("is_complete", "invoice_date")
    search_fields = ("invoice_number", "contract__name")


@admin.register(models.InvoiceLine)
class InvoiceLineAdmin(admin.ModelAdmin):
    list_display = ("invoice", "row_number", "line_date", "product_type", "payer_account")
    list_filter = ("line_date", "product_type")
    search_fields = ("invoice__invoice_number", "driver_name", "bill_of_lading_number")


@admin.register(models.LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ("account", "contract", "entry_date", "entry_type", "amount_afn", "amount_usd")
    list_filter = ("entry_type", "entry_date")
    search_fields = ("account__name", "contract__name")
