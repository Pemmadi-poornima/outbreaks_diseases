"""
Start the server with: python run.py
Works reliably on Windows (avoids Python 3.10 dev-server bug).
"""
import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'outbreak_django.settings')

try:
    from waitress import serve
    from outbreak_django.wsgi import application
    print("=" * 55)
    print("  Outbreak AI  |  http://127.0.0.1:8000")
    print("  Admin Panel  |  http://127.0.0.1:8000/admin/")
    print("  Press CTRL+C to stop")
    print("=" * 55)
    serve(application, host='127.0.0.1', port=8000, threads=4)
except ImportError:
    print("[ERROR] Run:  pip install waitress")
    sys.exit(1)
