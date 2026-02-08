from decimal import Decimal

import jdatetime
from django.contrib import admin
from django.db.models import Case, DecimalField, F, Sum, Value, When

from . import models


def format_jalali(value):
    if not value:
        return "-"
    return jdatetime.date.fromgregorian(date=value).strftime("%Y/%m/%d")


@admin.register(models.AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "account_type", "balance_afn", "balance_usd")
    list_filter = ("account_type",)
    search_fields = ("name",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        debit_case = Case(
            When(ledger_entries__entry_type=models.LedgerEntry.EntryType.DEBIT, then=F("ledger_entries__amount_afn")),
            default=Value(0),
            output_field=DecimalField(max_digits=14, decimal_places=2),
        )
        credit_case = Case(
            When(ledger_entries__entry_type=models.LedgerEntry.EntryType.CREDIT, then=F("ledger_entries__amount_afn")),
            default=Value(0),
            output_field=DecimalField(max_digits=14, decimal_places=2),
        )
        debit_usd_case = Case(
            When(ledger_entries__entry_type=models.LedgerEntry.EntryType.DEBIT, then=F("ledger_entries__amount_usd")),
            default=Value(0),
            output_field=DecimalField(max_digits=12, decimal_places=2),
        )
        credit_usd_case = Case(
            When(ledger_entries__entry_type=models.LedgerEntry.EntryType.CREDIT, then=F("ledger_entries__amount_usd")),
            default=Value(0),
            output_field=DecimalField(max_digits=12, decimal_places=2),
        )
        return queryset.annotate(
            debit_afn_total=Sum(debit_case),
            credit_afn_total=Sum(credit_case),
            debit_usd_total=Sum(debit_usd_case),
            credit_usd_total=Sum(credit_usd_case),
        )

    @admin.display(description="مانده افغانی")
    def balance_afn(self, obj):
        debit = obj.debit_afn_total or Decimal("0")
        credit = obj.credit_afn_total or Decimal("0")
        return debit - credit

    @admin.display(description="مانده دلاری")
    def balance_usd(self, obj):
        debit = obj.debit_usd_total or Decimal("0")
        credit = obj.credit_usd_total or Decimal("0")
        return debit - credit


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(models.License)
class LicenseAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(models.Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("name", "account", "calculation_type", "contract_date_jalali", "is_closed")
    list_filter = ("calculation_type", "is_closed")
    search_fields = ("name", "account__name")

    @admin.display(description="تاریخ قرارداد")
    def contract_date_jalali(self, obj):
        return format_jalali(obj.contract_date)


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "contract", "invoice_date_jalali", "is_complete")
    list_filter = ("is_complete", "invoice_date")
    search_fields = ("invoice_number", "contract__name")

    @admin.display(description="تاریخ فاکتور")
    def invoice_date_jalali(self, obj):
        return format_jalali(obj.invoice_date)


@admin.register(models.InvoiceLine)
class InvoiceLineAdmin(admin.ModelAdmin):
    list_display = ("invoice", "row_number", "line_date_jalali", "product_type", "payer_account")
    list_filter = ("line_date", "product_type")
    search_fields = ("invoice__invoice_number", "driver_name", "bill_of_lading_number")

    @admin.display(description="تاریخ ردیف")
    def line_date_jalali(self, obj):
        return format_jalali(obj.line_date)


@admin.register(models.LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ("account", "contract", "entry_date_jalali", "entry_type", "amount_afn", "amount_usd")
    list_filter = ("entry_type", "entry_date")
    search_fields = ("account__name", "contract__name")

    @admin.display(description="تاریخ")
    def entry_date_jalali(self, obj):
        return format_jalali(obj.entry_date)
