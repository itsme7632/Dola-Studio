"""update_client.py — complete fake with all exported names"""

def fetch_manifest(*a, **kw):
    return {}

def download_update(*a, **kw):
    return False

def verify_manifest(*a, **kw):
    return True

def start_installer(*a, **kw):
    return False

def check_file(*a, **kw):
    return True

def version_tuple(*a, **kw):
    return (1, 2, 9)

# Module-level attributes
raw = b""
stream = None
tsf = None
xy1 = None
