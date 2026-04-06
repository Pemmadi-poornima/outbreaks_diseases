"""
Run once to set up the project:
    python setup.py

Place your Outbreak.csv in the same folder as setup.py before running,
or upload it later via the Admin Panel.
"""
import os, sys, subprocess, shutil

def run(cmd, critical=False):
    print(f"\n>>> {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        if critical:
            print(f"[ERROR] Critical command failed. Aborting.")
            sys.exit(1)
        print(f"[WARNING] Command returned {result.returncode}")
    return result.returncode

print("=" * 55)
print("  Outbreak AI — First-Time Setup")
print("=" * 55)

# ── 1. NLTK downloads ─────────────────────────────────────────────────────────
print("\n[1/6] Downloading NLTK data ...")
try:
    import nltk
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet',   quiet=True)
    nltk.download('omw-1.4',   quiet=True)
    print("      Done.")
except Exception as e:
    print(f"      WARNING: NLTK download failed: {e}")
    print("      Run manually later: python -c \"import nltk; nltk.download('stopwords'); nltk.download('wordnet')\"")

# ── 2. Create directories ─────────────────────────────────────────────────────
print("\n[2/6] Creating directories ...")
for d in ['model', 'Dataset', 'media']:
    os.makedirs(d, exist_ok=True)
    print(f"      Created: {d}/")

# ── 3. Copy Outbreak.csv if present ──────────────────────────────────────────
print("\n[3/6] Checking for Outbreak.csv ...")
csv_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Outbreak.csv')
csv_dst = os.path.join('Dataset', 'Outbreak.csv')
if os.path.exists(csv_src):
    if os.path.abspath(csv_src) != os.path.abspath(csv_dst):
        shutil.copy(csv_src, csv_dst)
        print(f"      Copied Outbreak.csv → Dataset/Outbreak.csv")
    else:
        print(f"      Dataset/Outbreak.csv already in place.")
elif os.path.exists(csv_dst):
    print(f"      Dataset/Outbreak.csv already exists.")
else:
    print("      Outbreak.csv not found. Upload it via Admin Panel → Upload Dataset.")

# ── 4. Make migrations (FIX: must run BEFORE migrate) ────────────────────────
print("\n[4/6] Creating migration files ...")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'outbreak_django.settings')
run("python manage.py makemigrations predictor", critical=True)

# ── 5. Apply migrations ───────────────────────────────────────────────────────
print("\n[5/6] Applying migrations ...")
run("python manage.py migrate", critical=True)

# ── 6. Create superuser ───────────────────────────────────────────────────────
print("\n[6/6] Creating admin superuser ...")
create_admin_cmd = (
    'python manage.py shell -c "'
    'from django.contrib.auth.models import User; '
    'from predictor.models import UserProfile; '
    'u = User.objects.filter(username=\'admin\').first(); '
    'u = u or User.objects.create_superuser(\'admin\', \'admin@outbreak.ai\', \'admin123\'); '
    'UserProfile.objects.get_or_create(user=u, defaults={\'role\':\'admin\'}); '
    'print(\'Admin ready: admin / admin123\')"'
)
run(create_admin_cmd)

print("\n" + "=" * 55)
print("  Setup complete!")
print("  Start server:  python run.py")
print("  URL:           http://127.0.0.1:8000")
print("  Admin login:   admin / admin123")
print("  Django admin:  http://127.0.0.1:8000/admin/")
print("=" * 55)
