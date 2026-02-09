# Online Accounting System for Bar Chalan (Proposal)

> Language: Persian (Dari)

## هدف پروژه
ساخت یک سیستم حسابداری آنلاین چندکاربره با تاریخ شمسی برای مدیریت قراردادها، فاکتورها، داد و گرفت‌ها (ledger)، و گزارش‌های کامل سود و زیان و مانده حساب مشتریان.

## انتخاب تکنولوژی
- **Backend:** Django + Django REST Framework
- **Database:** PostgreSQL (پیشنهادی برای گزارش‌گیری و تراکنش‌های مالی)
- **Frontend:** React + MUI (یا Django Templates اگر MVP ساده بخواهید)
- **Datetime شمسی:** استفاده از `django-jalali` یا `khayyam/jdatetime` برای نمایش، و ذخیره تاریخ به صورت `DateField` استاندارد همراه با نمایش شمسی.
- **چندکاربره:** Django Auth + Role/Permission

## دامنه‌ها و موجودیت‌ها (مدل داده پیشنهادی)
### کاربران
- User (مدیریت دسترسی‌ها، نقش‌ها، و سطوح دسترسی)

### حساب‌ها و انواع حساب
- **Account**
  - id
  - name
  - account_type (FK)
  - currency (AFN / USD)
  - is_active
- **AccountType**
  - id
  - name

### قراردادها
- **Contract**
  - id
  - account (FK به Account)
  - contract_name
  - goods_type
  - contract_date (Jalali UI / Gregorian storage)
  - close_contract (boolean)
  - calc_method (enum: `FLAT_USD_PER_TON`, `COST_BASED`, `COST_BASED_TO_USD_DAILY`)
  - usd_per_ton
  - permit_cost
  - misc_cost
  - commission_afn
  - commission_usd

### فاکتور و جزئیات فاکتور (تانکرها)
- **Invoice**
  - id
  - contract (FK)
  - invoice_number
  - invoice_date
  - description
  - is_finalized
  - customer_account (FK)
- **InvoiceLine** (جزئیات/تانکر)
  - id
  - invoice (FK)
  - row_no
  - line_date
  - waybill_number
  - driver_name
  - transit
  - goods_type
  - waybill_weight
  - customs_weight
  - liters
  - permit_name (FK به Permit)
  - payer_account (FK به Account)
  - afn_costs (JSON یا فیلدهای جداگانه)
    - product_price_afn
    - public_benefit
    - transport
    - percent_60
    - percent_20
    - norm_afn
    - dozbalaq
    - exchanger_commission
    - escort
    - overnight
    - scale
    - misc_afn
    - commission_afn
  - usd_costs (JSON یا فیلدهای جداگانه)
    - norm_usd
    - permit_commission
    - freight
    - misc_usd
    - commission_usd
  - in_kind_costs
    - percent_in_kind
  - description

### کالا و جواز
- **Goods**
  - id
  - name
- **Permit**
  - id
  - name

### داد و گرفت‌ها (Ledger / Journal)
- **LedgerEntry**
  - id
  - entry_date
  - account (FK)
  - contract (FK)
  - invoice (FK, optional)
  - description
  - debit_afn
  - credit_afn
  - debit_usd
  - credit_usd
  - created_by

## قواعد کسب‌وکار (Business Rules)
- هر فاکتور مربوط به یک مشتری است.
- یک مشتری می‌تواند چندین فاکتور داشته باشد.
- هر فاکتور شامل چندین تانکر (InvoiceLine) است.
- هر تراکنش مربوط به یک حساب است و می‌تواند به یک قرارداد خاص مرتبط شود.
- **حساب‌های پرداخت‌کننده هزینه‌ها**: وقتی هزینه‌ی تانکر پرداخت می‌شود، آن حساب بدهکار و هزینه‌ها بستانکار می‌شوند (Ledger).
- **ارزها**: هزینه‌های AFN و USD جدا ذخیره می‌شوند، اما **بلانس کلی به USD** گزارش می‌شود.
- **روش‌های محاسبه قرارداد**:
  1. **فی‌تن دلاری ثابت**: فقط مبلغ توافقی دلاری برای هر تن.
  2. **بر اساس هزینه**: همه هزینه‌ها + کمسیون.
  3. **بر اساس هزینه تبدیل به دلار روز**: هزینه‌های روزانه به نرخ همان روز تبدیل و در فاکتور دلاری درج می‌شود.

## گزارش‌ها (حداقل‌ها)
- مانده حساب مشتری به تفکیک قرارداد و کلی
- گردش حساب مشتری (Ledger)
- گردش یک قرارداد
- گزارش سود و زیان (Profit & Loss)
- گزارش فاکتورهای مشتری و مجموع بدهی/پرداختی

## پیشنهاد پیاده‌سازی MVP
1. ایجاد مدل‌های اصلی + مهاجرت‌ها
2. ساخت API برای قراردادها، فاکتورها، و Ledger
3. پنل مدیریت و داشبورد اولیه (جستجو، فیلتر، گزارش)
4. گزارش‌های اصلی

## نکات UX/UI
- استفاده از رنگ‌بندی آرام و حرفه‌ای (آبی/خاکستری)
- فرم‌های قدم‌به‌قدم برای ثبت قرارداد و فاکتور
- فیلتر سریع بر اساس مشتری، تاریخ، قرارداد

---

اگر تایید کنید، قدم بعدی ساخت اسکلت پروژه Django و ایجاد مدل‌های دیتابیس خواهد بود.
