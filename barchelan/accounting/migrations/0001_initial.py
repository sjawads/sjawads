from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AccountType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Account",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                (
                    "account_type",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="accounting.accounttype"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="License",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Contract",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                ("contract_date", models.DateField()),
                ("is_closed", models.BooleanField(default=False)),
                (
                    "calculation_type",
                    models.CharField(
                        choices=[
                            ("price_per_ton", "فی تن (دلاری)"),
                            ("cost_based", "به اساس هزینه"),
                            ("cost_based_usd", "به اساس هزینه تبدیل به دلار"),
                        ],
                        max_length=40,
                    ),
                ),
                ("price_per_ton_usd", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("license_fee_afn", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("misc_fee_afn", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("commission_afn", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("commission_usd", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                (
                    "account",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="contracts", to="accounting.account"),
                ),
                (
                    "product_type",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="accounting.product"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Invoice",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("invoice_number", models.CharField(max_length=50)),
                ("invoice_date", models.DateField()),
                ("description", models.TextField(blank=True)),
                ("is_complete", models.BooleanField(default=False)),
                (
                    "contract",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="invoices", to="accounting.contract"),
                ),
            ],
            options={"unique_together": {("contract", "invoice_number")}},
        ),
        migrations.CreateModel(
            name="InvoiceLine",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("row_number", models.PositiveIntegerField()),
                ("line_date", models.DateField()),
                ("bill_of_lading_number", models.CharField(blank=True, max_length=80)),
                ("driver_name", models.CharField(blank=True, max_length=120)),
                ("transit", models.CharField(blank=True, max_length=120)),
                ("weight_bol", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("weight_customs", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("liters", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("product_fee_afn", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("public_benefit_afn", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("transport_afn", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("fee_60_afn", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("fee_20_afn", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("norm_afn", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("dozbalagh_afn", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("exchanger_commission_afn", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("escort_afn", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("night_sleep_afn", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("scale_afn", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("misc_afn", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("commission_barchelan_afn", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("norm_usd", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("license_commission_usd", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("freight_usd", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("misc_usd", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("commission_barchelan_usd", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("goods_percentage", models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ("notes", models.TextField(blank=True)),
                (
                    "invoice",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="lines", to="accounting.invoice"),
                ),
                (
                    "license",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to="accounting.license"),
                ),
                (
                    "payer_account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="payer_invoice_lines",
                        to="accounting.account",
                    ),
                ),
                (
                    "product_type",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="accounting.product"),
                ),
            ],
            options={"unique_together": {("invoice", "row_number")}},
        ),
        migrations.CreateModel(
            name="LedgerEntry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("entry_date", models.DateField()),
                (
                    "entry_type",
                    models.CharField(choices=[("debit", "Debit"), ("credit", "Credit")], max_length=10),
                ),
                ("description", models.TextField(blank=True)),
                ("amount_afn", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("amount_usd", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="ledger_entries",
                        to="accounting.account",
                    ),
                ),
                (
                    "contract",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="ledger_entries",
                        to="accounting.contract",
                    ),
                ),
            ],
        ),
    ]
