- 👋 Hi, I’m @sjawads
- 👀 I’m interested in web designing
- 🌱 I’m currently learning javascript
- 💞️ I’m looking to collaborate on ...
- 📫 How to reach me jawadmlis2110@gmail.com

## Barchelan accounting starter (Django)

This repository now includes a Django starter project and data model for a
multi-user accounting system tailored to Barchelan workflows.

### Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python barchelan/manage.py makemigrations accounting
python barchelan/manage.py migrate
python barchelan/manage.py createsuperuser
python barchelan/manage.py runserver
```

Then visit `http://127.0.0.1:8000/admin/` to manage contracts, invoices, and
ledger entries.

### Windows quick start

```powershell
py -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python barchelan/manage.py makemigrations accounting
python barchelan/manage.py migrate
python barchelan/manage.py createsuperuser
python barchelan/manage.py runserver
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

<!---
sjawads/sjawads is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->
