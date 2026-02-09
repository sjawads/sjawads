from django.contrib import admin

from . import models


@admin.register(models.AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "account_type", "currency", "is_active")
    list_filter = ("currency", "is_active", "account_type")
    search_fields = ("name",)


@admin.register(models.Goods)
class GoodsAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(models.Permit)
class PermitAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(models.Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("contract_name", "account", "calc_method", "contract_date", "close_contract")
    list_filter = ("calc_method", "close_contract")
    search_fields = ("contract_name",)


class InvoiceLineInline(admin.TabularInline):
    model = models.InvoiceLine
    extra = 0


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "customer_account", "contract", "invoice_date", "is_finalized")
    list_filter = ("is_finalized", "invoice_date")
    search_fields = ("invoice_number",)
    inlines = [InvoiceLineInline]


@admin.register(models.LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ("entry_date", "account", "contract", "invoice", "debit_afn", "credit_afn", "debit_usd", "credit_usd")
    list_filter = ("entry_date", "account")
    search_fields = ("description",)
