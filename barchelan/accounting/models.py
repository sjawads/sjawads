from django.db import models


class AccountType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Account(models.Model):
    name = models.CharField(max_length=150)
    account_type = models.ForeignKey(AccountType, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self) -> str:
        return self.name


class License(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self) -> str:
        return self.name


class Contract(models.Model):
    class CalculationType(models.TextChoices):
        PRICE_PER_TON = "price_per_ton", "فی تن (دلاری)"
        COST_BASED = "cost_based", "به اساس هزینه"
        COST_BASED_USD = "cost_based_usd", "به اساس هزینه تبدیل به دلار"

    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="contracts")
    name = models.CharField(max_length=150)
    product_type = models.ForeignKey(Product, on_delete=models.PROTECT)
    contract_date = models.DateField()
    is_closed = models.BooleanField(default=False)
    calculation_type = models.CharField(max_length=40, choices=CalculationType.choices)
    price_per_ton_usd = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    license_fee_afn = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    misc_fee_afn = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    commission_afn = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    commission_usd = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f"{self.name} - {self.account}"


class Invoice(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.PROTECT, related_name="invoices")
    invoice_number = models.CharField(max_length=50)
    invoice_date = models.DateField()
    description = models.TextField(blank=True)
    is_complete = models.BooleanField(default=False)

    class Meta:
        unique_together = ("contract", "invoice_number")

    def __str__(self) -> str:
        return f"{self.invoice_number}"


class InvoiceLine(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="lines")
    row_number = models.PositiveIntegerField()
    line_date = models.DateField()
    bill_of_lading_number = models.CharField(max_length=80, blank=True)
    driver_name = models.CharField(max_length=120, blank=True)
    transit = models.CharField(max_length=120, blank=True)
    product_type = models.ForeignKey(Product, on_delete=models.PROTECT)
    weight_bol = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    weight_customs = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    liters = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    license = models.ForeignKey(License, on_delete=models.PROTECT, null=True, blank=True)
    payer_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="payer_invoice_lines",
    )
    product_fee_afn = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    public_benefit_afn = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    transport_afn = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    fee_60_afn = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    fee_20_afn = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    norm_afn = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    dozbalagh_afn = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    exchanger_commission_afn = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    escort_afn = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    night_sleep_afn = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    scale_afn = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    misc_afn = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    commission_barchelan_afn = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    norm_usd = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    license_commission_usd = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    freight_usd = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    misc_usd = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    commission_barchelan_usd = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    goods_percentage = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("invoice", "row_number")

    def __str__(self) -> str:
        return f"{self.invoice.invoice_number} - {self.row_number}"


class LedgerEntry(models.Model):
    class EntryType(models.TextChoices):
        DEBIT = "debit", "Debit"
        CREDIT = "credit", "Credit"

    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="ledger_entries")
    contract = models.ForeignKey(
        Contract,
        on_delete=models.PROTECT,
        related_name="ledger_entries",
        null=True,
        blank=True,
    )
    entry_date = models.DateField()
    entry_type = models.CharField(max_length=10, choices=EntryType.choices)
    description = models.TextField(blank=True)
    amount_afn = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    amount_usd = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f"{self.account} - {self.entry_date}"
