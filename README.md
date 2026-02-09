# Bar Chalan Online Accounting System

این ریپازیتوری شامل اسکلت اولیه‌ی یک سیستم حسابداری آنلاین برای بارچالانی است. پیاده‌سازی با Django انجام شده و مدل‌های اصلی مطابق نیازهای مطرح‌شده ساخته شده‌اند.

## امکانات کلیدی (نسخه اولیه)
- مدیریت کاربران (از طریق Django Admin)
- حساب‌ها و نوع حساب‌ها
- قراردادها با سه روش محاسبه
- فاکتور و جزئیات تانکرها
- داد و گرفت‌ها (Ledger)
- پشتیبانی از ارز AFN و USD

## راه‌اندازی
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python bar_chalan_accounting/manage.py migrate
python bar_chalan_accounting/manage.py createsuperuser
python bar_chalan_accounting/manage.py runserver
```

## ساختار پروژه
- `bar_chalan_accounting/` پروژه Django
- `bar_chalan_accounting/accounting/` اپلیکیشن اصلی حسابداری

## قدم‌های بعدی پیشنهادی
- افزودن API با Django REST Framework
- پیاده‌سازی گزارش‌های سود و زیان و مانده حساب
- اضافه کردن نمایش تاریخ شمسی در UI
- طراحی فرانت‌اند حرفه‌ای
