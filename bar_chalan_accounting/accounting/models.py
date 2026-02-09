from django.conf import settings
from django.db import models


class AccountType(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self) -> str:
        return self.name


class Account(models.Model):
    class Currency(models.TextChoices):
        AFN = "AFN", "Afghani"
        USD = "USD", "US Dollar"

    name = models.CharField(max_length=160)
    account_type = models.ForeignKey(AccountType, on_delete=models.PROTECT, related_name="accounts")
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.AFN)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class Goods(models.Model):
    name = models.CharField(max_length=160)

    def __str__(self) -> str:
        return self.name


class Permit(models.Model):
    name = models.CharField(max_length=160)

    def __str__(self) -> str:
        return self.name


class Contract(models.Model):
    class CalculationMethod(models.TextChoices):
        FLAT_USD_PER_TON = "FLAT_USD_PER_TON", "Flat USD per ton"
        COST_BASED = "COST_BASED", "Cost based"
        COST_BASED_TO_USD_DAILY = "COST_BASED_TO_USD_DAILY", "Cost based converted to USD daily"

    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="contracts")
    contract_name = models.CharField(max_length=200)
    goods_type = models.ForeignKey(Goods, on_delete=models.PROTECT, related_name="contracts")
    contract_date = models.DateField()
    close_contract = models.BooleanField(default=False)
    calc_method = models.CharField(max_length=32, choices=CalculationMethod.choices)
    usd_per_ton = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    permit_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    misc_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    commission_afn = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    commission_usd = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self) -> str:
        return self.contract_name


class Invoice(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.PROTECT, related_name="invoices")
    invoice_number = models.CharField(max_length=50)
    invoice_date = models.DateField()
    description = models.TextField(blank=True)
    is_finalized = models.BooleanField(default=False)
    customer_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="invoices")

    def __str__(self) -> str:
        return f"{self.invoice_number} - {self.customer_account}"


class InvoiceLine(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="lines")
    row_no = models.PositiveIntegerField()
    line_date = models.DateField()
    waybill_number = models.CharField(max_length=100, blank=True)
    driver_name = models.CharField(max_length=160, blank=True)
    transit = models.CharField(max_length=160, blank=True)
    goods_type = models.ForeignKey(Goods, on_delete=models.PROTECT, related_name="invoice_lines")
    waybill_weight = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    customs_weight = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    liters = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    permit = models.ForeignKey(Permit, on_delete=models.PROTECT, related_name="invoice_lines", null=True, blank=True)
    payer_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="paid_invoice_lines")
    product_price_afn = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    public_benefit = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    transport = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    percent_60 = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    percent_20 = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    norm_afn = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    dozbalaq = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    exchanger_commission = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    escort = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    overnight = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    scale = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    misc_afn = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    commission_afn = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    norm_usd = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    permit_commission = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    freight = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    misc_usd = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    commission_usd = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    percent_in_kind = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["invoice", "row_no"]
        unique_together = ("invoice", "row_no")

    def __str__(self) -> str:
        return f"{self.invoice.invoice_number} - {self.row_no}"


class LedgerEntry(models.Model):
    entry_date = models.DateField()
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="ledger_entries")
    contract = models.ForeignKey(Contract, on_delete=models.PROTECT, related_name="ledger_entries", null=True, blank=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name="ledger_entries", null=True, blank=True)
    description = models.TextField(blank=True)
    debit_afn = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    credit_afn = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    debit_usd = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    credit_usd = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="ledger_entries")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-entry_date", "id"]

    def __str__(self) -> str:
        return f"{self.account} - {self.entry_date}"
