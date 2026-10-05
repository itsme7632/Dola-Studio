"""
Sitecustomize for SDola Studio:
1. Environment & Tcl/Tk setup
2. Full offline license spoof
3. Custom branding (SDola Studio, Created by Sajid AI) & Social buttons customization
4. Yellow Gradient / Radiant Gold Accent Theme via CustomTkinter Constructor Hooks
5. Window Title & Icon Hooks
6. Safe Single-Instance Mutex bypass
"""
import sys, types, hashlib, platform, json, base64, importlib, os, webbrowser
from pathlib import Path

# Configure Tcl/Tk library paths if present in _internal
try:
    _this_dir = os.path.dirname(os.path.abspath(__file__))
    _root_dir = os.path.dirname(_this_dir)
    if os.path.exists(os.path.join(_this_dir, "_tcl_data")):
        os.environ["TCL_LIBRARY"] = os.path.join(_this_dir, "_tcl_data")
        os.environ["TK_LIBRARY"] = os.path.join(_this_dir, "_tk_data")
    elif os.path.exists(os.path.join(_root_dir, "_internal", "_tcl_data")):
        os.environ["TCL_LIBRARY"] = os.path.join(_root_dir, "_internal", "_tcl_data")
        os.environ["TK_LIBRARY"] = os.path.join(_root_dir, "_internal", "_tk_data")
except Exception:
    pass

def _log(msg):
    try:
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        os.makedirs(log_dir, exist_ok=True)
        with open(os.path.join(log_dir, "site_log.txt"), "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except Exception:
        pass

_log(f"=== sitecustomize.py LOADED ===\npython={sys.version}")

# =====================================================
# PART 1: INJECT FAKE LICENSE MODULES
# =====================================================

def _make(name):
    m = types.ModuleType(name)
    sys.modules[name] = m
    return m

def _device_id():
    try:
        import winreg
        k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography",
                           0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        guid, _ = winreg.QueryValueEx(k, "MachineGuid")
        winreg.CloseKey(k)
        return hashlib.sha256(guid.encode()).hexdigest()
    except Exception:
        return hashlib.sha256(platform.node().encode()).hexdigest()

_DID = _device_id()
_S = {
    "licensed": True, "plan": "pro", "active": True,
    "claims": {"plan": "pro", "licensed": True},
    "expires_at": 9999999999, "issued_at": 0,
    "token": "ONYX-BYPASS", "product": "DOLA-STUDIO",
    "device": _DID, "subscription": {"plan": "pro", "active": True, "status": "active"},
    "features": {"all": True, "pro": True, "unlimited": True},
    "is_online": True, "online": True,
}

class _LS:
    def __init__(self, *a, **kw): self._d = _DID
    def status(self, *a, **kw): return dict(_S)
    def activate(self, *a, **kw): return dict(_S)
    def refresh(self, *a, **kw): return dict(_S)
    def verify(self, *a, **kw): return True
    def _save(self, *a, **kw): pass
    @property
    def is_online(self): return True
    def __getattr__(self, n):
        if n == 'is_online': return True
        return lambda *a,**k: dict(_S)

class LicenseError(Exception):
    pass

lc = _make("license_client")
lc.LicenseStore = _LS
lc.LicenseError = LicenseError
lc.device_id = lambda: _DID
lc.normalize_device = lambda d: d.strip().lower()
lc.verify_license = lambda *a,**k: True

class _WS:
    def __init__(self, *a, **kw): pass
    def status(self, *a, **kw): return dict(_S)
    def refresh(self, *a, **kw): return dict(_S)
    def verify(self, *a, **kw): return True
    @property
    def is_online(self): return True
    def __getattr__(self, n):
        if n == 'is_online': return True
        return lambda *a,**k: dict(_S)

wl = _make("worker_license")
wl.WorkerLicenseStore = _WS
wl.verify_token = lambda *a,**k: True

class _FS:
    def __init__(self, *a, **kw): pass
    def status(self, *a, **kw): return dict(_S)
    def activate(self, *a, **kw): return dict(_S)
    def refresh(self, *a, **kw): return dict(_S)
    @property
    def is_online(self): return True
    def __getattr__(self, n):
        if n == 'is_online': return True
        return lambda *a,**k: dict(_S)

fl = _make("firebase_license")
fl.FirebaseLicenseStore = _FS
fl.verify_firebase_license = lambda *a,**k: True

class _OL:
    def __init__(self, *a, **kw): pass
    def status(self, *a, **kw): return dict(_S)
    def activate(self, *a, **kw): return dict(_S)
    def refresh(self, *a, **kw): return dict(_S)
    @property
    def is_online(self): return True
    def __getattr__(self, n):
        if n == 'is_online': return True
        return lambda *a,**k: dict(_S)

ol = _make("online_license")
ol.OnlineLicenseStore = _OL
ol.check_online_license = lambda *a,**k: dict(_S)
ol.refresh_online_license = lambda *a,**k: dict(_S)

ic = _make("integrity_check")
ic.verify_installation = lambda *a,**k: True
ic.verify_payload = lambda *a,**k: True
ic.check_files = lambda *a,**k: True

def _verify_payload(payload=None, *a, **k):
    return payload if payload else {}
def _sign_payload(p, *a, **k):
    return {"payload": base64.urlsafe_b64encode(
        json.dumps(p, sort_keys=True).encode()).decode().rstrip("="),
        "signature": "ONYXBYPASS",
        "purpose": p.get("purpose","license") if isinstance(p,dict) else "license"}

sp = _make("signed_payload")
sp.verify_payload = _verify_payload
sp.sign_payload = _sign_payload

class _LR:
    def __init__(self, *a, **kw): pass
    def status(self, *a, **kw): return dict(_S)
    def check(self, *a, **kw): return True
    def verify(self, *a, **kw): return True
    @property
    def is_online(self): return True
    def __getattr__(self, n):
        if n == 'is_online': return True
        return lambda *a,**k: dict(_S)

lr = _make("license_router")
lr.LicenseRouter = _LR
lr.RoutedLicenseStore = _LR
lr.get_license_status = lambda *a,**k: dict(_S)
lr.check_license = lambda *a,**k: True

# Update client/helper fakes
uh = _make("update_helper")
uh.apply = lambda *a, **kw: False
uh.main = lambda *a, **kw: False

uc = _make("update_client")
uc.check_for_updates = lambda: None
uc.download_update = lambda *a, **kw: False
uc.fetch_manifest = lambda *a, **kw: {}
uc.verify_manifest = lambda *a, **kw: True
uc.start_installer = lambda *a, **kw: False
uc.check_file = lambda *a, **kw: True
uc.version_tuple = lambda *a, **kw: (1, 2, 9)
uc.raw = b""
uc.stream = None
uc.tsf = None
uc.xy1 = None

# =====================================================
# PART 2: MUTEX & PATHS CUSTOMIZATION
# =====================================================

try:
    import desktop_instance
    desktop_instance.MUTEX_NAME = f"Local\\SDolaStudio-{os.getpid()}"
    desktop_instance.SHOW_EVENT_NAME = f"Local\\SDolaStudio-show-{os.getpid()}"
    orig_acquire = desktop_instance.WindowsBackend.acquire_mutex
    def _safe_acquire(self):
        h, _ = orig_acquire(self)
        return (h, False)
    desktop_instance.WindowsBackend.acquire_mutex = _safe_acquire
    _log("[PRE-PATCH] desktop_instance patched with unique mutex")
except Exception as e:
    _log(f"[PRE-PATCH ERROR] desktop_instance: {e}")

try:
    import app_paths
    app_paths.USER_VIDEOS = Path.home() / "Videos" / "SDola Studio"
    app_paths.USER_VIDEOS.mkdir(parents=True, exist_ok=True)
    app_paths.VIDEO_DIR = app_paths.USER_VIDEOS
    _log("[PRE-PATCH] app_paths updated to SDola Studio")
except Exception:
    pass

# =====================================================
# PART 3: CUSTOM BRANDING, SOCIAL LINKS & YELLOW THEME
# =====================================================

NEW_APP_NAME = "SDola Studio"
NEW_CREATOR = "Created by Sajid AI"
NEW_WHATSAPP_URL = "https://whatsapp.com/channel/0029Vb96GhE47Xe6BotLE21r"

YELLOW_ACCENT = ("#D97706", "#F5C518")      # Deep Warm Gold (Light) / Glowing Yellow Gold (Dark)
YELLOW_HOVER = ("#B45309", "#FFDC60")       # Rich Amber (Light) / Bright Radiant Gold (Dark)
YELLOW_TEXT = ("#FFFFFF", "#181500")        # White (Light) / Deep Dark Charcoal (Dark)
YELLOW_SOFT = ("#FEF3C7", "#382D08")        # Soft Gold Pill / Badge
OLD_ACCENTS = (("#B9573D", "#D58A6C"), "#B9573D", "#D58A6C")

ac = _make("app_config")
ac.APP_NAME = NEW_APP_NAME
ac.APP_VERSION = "1.2.6"
ac.CREATOR = NEW_CREATOR
ac.PRODUCT = "sdola-studio"
ac.WHATSAPP_CHANNEL = NEW_WHATSAPP_URL
ac.FACEBOOK_URL = ""
ac.SUPPORT_WHATSAPP = ""
ac.WORKER_API_URL = "https://zbotsocial-license.mrbahaudden.workers.dev"
ac.ONLINE_API_URL = "https://zdola-studio-licenses.blissboles331680649.chatgpt.site"
ac.PORTAL_URL = "https://zakariyastudio.com/portal"
ac.WEB_APP_URL = "https://zdola-studio.web.app"
ac.FIREBASE_API_KEY = "AIzaSyDn0_sBXSSfuVzCvBqmaroAc4RfaZ5r7yE"
ac.FIREBASE_PROJECT_ID = "zdola-studio"
ac.LICENSE_PUBLIC_KEY = "MCowBQYDK2VwAyEAuu7EufYV4nz6DEeLIaATCYBLW6pHB8uWHXkTQHanAwo="
ac.WORKER_PUBLIC_KEY = "XCjvJJnN_O7J8zxt3qA8nLwjqGoBu0ZGENuCh-mO3t8"
ac.UPDATE_PUBLIC_KEY = "fTSGlCM80Zp9fZJhptdEgarExgq2cC0DdU1xS7zgZC8hGSu_TocrxO4dt9asAZ_pRj3h8qZtsBwXcOLqtyOviE"
ac.UPDATE_REPOSITORY = "zakariya713/dola-studio-updates"
ac.UPDATE_FEED = "https://github.com/zakariya713/dola-studio-updates/releases/latest/download/update.json"
ac.LICENSE_PANEL_URL = "https://zakariyastudio.com/portal"
ac.ONLINE_PUBLIC_KEY = ac.LICENSE_PUBLIC_KEY

# DIRECT PRE-PATCHING OF STUDIO_UI:
try:
    import studio_ui
    studio_ui.APP_NAME = NEW_APP_NAME
    studio_ui.CREATOR = NEW_CREATOR
    studio_ui.WHATSAPP_CHANNEL = NEW_WHATSAPP_URL
    studio_ui.FACEBOOK_URL = ""
    studio_ui.SUPPORT_WHATSAPP = ""
    studio_ui.COLORS["accent"] = YELLOW_ACCENT
    studio_ui.COLORS["accent_hover"] = YELLOW_HOVER
    studio_ui.COLORS["accent_text"] = YELLOW_TEXT
    studio_ui.COLORS["soft"] = YELLOW_SOFT
    _log("[PRE-PATCH] studio_ui patched with SDola branding and yellow colors")
except Exception as e:
    _log(f"[PRE-PATCH ERROR] studio_ui: {e}")

# =====================================================
# PART 4: HOOK CUSTOMTKINTER CONSTRUCTORS DIRECTLY
# =====================================================
try:
    import customtkinter as ctk
    import tkinter as _tk

    # 1. Force window title to SDola Studio everywhere
    def _hook_title(cls):
        orig_t = cls.title
        def _set_title(self, string=None):
            if string is not None:
                string = NEW_APP_NAME
            return orig_t(self, string)
        cls.title = _set_title

    _hook_title(ctk.CTk)
    _hook_title(ctk.CTkToplevel)
    _hook_title(_tk.Tk)
    _hook_title(_tk.Toplevel)

    # 2. Force window icon to new sdola.ico
    def _hook_icon(cls):
        orig_i = getattr(cls, "iconbitmap", None)
        if orig_i:
            def _set_icon(self, bitmap=None, default=None):
                this_folder = os.path.dirname(os.path.abspath(__file__))
                for candidate in [
                    os.path.join(this_folder, "assets", "sdola.ico"),
                    os.path.join(this_folder, "assets", "zdola.ico"),
                    os.path.join(this_folder, "sdola.ico"),
                    os.path.join(os.path.dirname(this_folder), "sdola.ico"),
                ]:
                    if os.path.exists(candidate):
                        bitmap = candidate
                        break
                return orig_i(self, bitmap=bitmap, default=default)
            cls.iconbitmap = _set_icon

    _hook_icon(ctk.CTk)
    _hook_icon(_tk.Tk)

    # 3. Intercept CTkButton constructor
    orig_btn = ctk.CTkButton.__init__
    def patched_btn(self, *a, **kw):
        fg = kw.get("fg_color")
        if fg in OLD_ACCENTS or (isinstance(fg, tuple) and any(c in str(fg) for c in ("#D58A6C", "#B9573D"))):
            kw["fg_color"] = YELLOW_ACCENT
            kw["hover_color"] = YELLOW_HOVER
            kw["text_color"] = YELLOW_TEXT
        orig_btn(self, *a, **kw)
    ctk.CTkButton.__init__ = patched_btn

    # 4. Intercept CTkCheckBox constructor
    orig_cb = ctk.CTkCheckBox.__init__
    def patched_cb(self, *a, **kw):
        fg = kw.get("fg_color")
        if fg in OLD_ACCENTS or fg is None or (isinstance(fg, tuple) and any(c in str(fg) for c in ("#D58A6C", "#B9573D"))):
            kw["fg_color"] = YELLOW_ACCENT
            kw["hover_color"] = YELLOW_HOVER
        orig_cb(self, *a, **kw)
    ctk.CTkCheckBox.__init__ = patched_cb

    # 5. Intercept CTkSwitch constructor
    orig_sw = ctk.CTkSwitch.__init__
    def patched_sw(self, *a, **kw):
        kw["progress_color"] = YELLOW_ACCENT
        orig_sw(self, *a, **kw)
    ctk.CTkSwitch.__init__ = patched_sw

    # 6. Intercept CTkProgressBar constructor
    orig_pb = ctk.CTkProgressBar.__init__
    def patched_pb(self, *a, **kw):
        kw["progress_color"] = YELLOW_ACCENT
        orig_pb(self, *a, **kw)
    ctk.CTkProgressBar.__init__ = patched_pb

    # 7. Intercept CTkRadioButton constructor
    orig_rb = ctk.CTkRadioButton.__init__
    def patched_rb(self, *a, **kw):
        kw["fg_color"] = YELLOW_ACCENT
        kw["hover_color"] = YELLOW_HOVER
        orig_rb(self, *a, **kw)
    ctk.CTkRadioButton.__init__ = patched_rb

    _log("[PRE-PATCH] CustomTkinter constructors hooked successfully for Yellow Theme")
except Exception as e:
    _log(f"[PRE-PATCH ERROR] CustomTkinter hooks: {e}")

# =====================================================
# PART 5: DOLA_GUI DOLAAPP INIT HOOK
# =====================================================
try:
    import dola_gui
    dola_gui.COLORS.update(studio_ui.COLORS)
    orig_dola_init = dola_gui.DolaApp.__init__
    
    def patched_dola_init(self, *a, **kw):
        orig_dola_init(self, *a, **kw)
        
        def _apply_sdola_ui_polish():
            try:
                self.root.title(NEW_APP_NAME)
                
                # Single WhatsApp Channel button: Destroy Facebook and Support buttons permanently!
                if hasattr(self, "social_buttons") and len(self.social_buttons) >= 3:
                    self.social_buttons[0].configure(
                        command=lambda: webbrowser.open_new_tab(NEW_WHATSAPP_URL)
                    )
                    try:
                        self.social_buttons[1].destroy()
                    except Exception:
                        self.social_buttons[1].grid_forget()
                    try:
                        self.social_buttons[2].destroy()
                    except Exception:
                        self.social_buttons[2].grid_forget()
                
                # Ensure primary buttons are vibrant yellow with dark text
                if hasattr(self, "btn_run"):
                    self.btn_run.configure(fg_color=YELLOW_ACCENT, hover_color=YELLOW_HOVER, text_color=YELLOW_TEXT)
                if hasattr(self, "btn_add_cookies"):
                    self.btn_add_cookies.configure(fg_color=YELLOW_ACCENT, hover_color=YELLOW_HOVER, text_color=YELLOW_TEXT)
                if hasattr(self, "state_badge"):
                    self.state_badge.configure(fg_color=YELLOW_SOFT)
                if hasattr(self, "progress"):
                    self.progress.configure(progress_color=YELLOW_ACCENT)
                
                # Scan any child labels or buttons that might still have old accent
                def walk_polish(w):
                    for c in w.winfo_children():
                        try:
                            if c.cget("fg_color") in OLD_ACCENTS or "#D58A6C" in str(c.cget("fg_color")):
                                c.configure(fg_color=YELLOW_ACCENT)
                        except Exception: pass
                        try:
                            txt = c.cget("text")
                            if "Dola Studio" in txt or txt == NEW_APP_NAME:
                                c.configure(text=NEW_APP_NAME, text_color=YELLOW_ACCENT)
                            elif "Sajid AI" in txt or txt == NEW_CREATOR or "Zakariya" in txt:
                                c.configure(text=NEW_CREATOR, text_color=("#D97706", "#FBBF24"))
                        except Exception: pass
                        walk_polish(c)
                walk_polish(self.root)
            except Exception as err:
                _log(f"[UI POLISH ERROR] {err}")

        _apply_sdola_ui_polish()
        try:
            self.root.after(100, _apply_sdola_ui_polish)
            self.root.after(300, _apply_sdola_ui_polish)
            self.root.after(800, _apply_sdola_ui_polish)
        except Exception:
            pass

    dola_gui.DolaApp.__init__ = patched_dola_init
    _log("[PRE-PATCH] dola_gui patched successfully into sys.modules")
except Exception as e:
    _log(f"[PRE-PATCH ERROR] dola_gui: {e}")

_log("=== sitecustomize.py setup completed successfully ===")
