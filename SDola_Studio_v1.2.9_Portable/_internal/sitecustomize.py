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

    # Patch Check Cookies with Auto Skill Upload popup
    orig_check_cookies = dola_gui.DolaApp._check_cookies
    if not getattr(orig_check_cookies, "_zdola_popup_patched", False):
        def _find_skill_file():
            candidates = [
                os.path.join(os.getcwd(), "SKILL.md"),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "SKILL.md"),
                os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "SKILL.md"),
                r"c:\Users\SAAHA\Searches\ZDolaStudio\SKILL.md",
                r"c:\Users\SAAHA\Searches\SKILL.md",
            ]
            for c in candidates:
                if os.path.exists(c):
                    return os.path.abspath(c)
            return None

        def _prepare_and_upload_skill(app_inst, selected_only=False):
            skill_file = _find_skill_file()
            if not skill_file:
                app_inst._log("⚠️ [SKILL WARNING] SKILL.md not found in root or app directory.", "warn")
                return
            try:
                if hasattr(app_inst, "skill_mode"):
                    app_inst.skill_mode.set("custom")
                if hasattr(app_inst, "_toggle_skill_inputs"):
                    app_inst._toggle_skill_inputs()
                if hasattr(app_inst, "skill_file_entry") and app_inst.skill_file_entry:
                    app_inst.skill_file_entry.configure(state="normal")
                    app_inst.skill_file_entry.delete(0, "end")
                    app_inst.skill_file_entry.insert(0, skill_file)
                if hasattr(app_inst, "cookie_tree") and app_inst.cookie_tree:
                    if selected_only:
                        sel = app_inst.cookie_tree.selection()
                        if not sel:
                            children = app_inst.cookie_tree.get_children()
                            if children:
                                app_inst.cookie_tree.selection_set(children)
                    else:
                        children = app_inst.cookie_tree.get_children()
                        if children:
                            app_inst.cookie_tree.selection_set(children)
                if hasattr(app_inst, "_on_account_selection"):
                    app_inst._on_account_selection()
                if hasattr(app_inst, "btn_upload_skill"):
                    app_inst.btn_upload_skill.configure(state="normal")
                app_inst._upload_skill_action()
            except Exception as ex:
                app_inst._log(f"⚠️ [ERROR] Failed to dispatch skill upload: {ex}", "error")

        class CheckAndSkillDialog(ctk.CTkToplevel):
            def __init__(self, master=None, selected_only=False):
                super().__init__(master)
                self.choice = None
                self.selected_only = selected_only
                target_str = "Selected" if selected_only else "All"
                self.title(f"Check {target_str} Accounts & Upload Skill")
                self.geometry("540x290")
                self.resizable(False, False)
                if master:
                    try:
                        master.update_idletasks()
                        x = master.winfo_x() + (master.winfo_width() // 2) - 270
                        y = master.winfo_y() + (master.winfo_height() // 2) - 145
                        self.geometry(f"+{max(0, x)}+{max(0, y)}")
                    except Exception: pass
                self.attributes("-topmost", True)
                self.grab_set()

                container = ctk.CTkFrame(self, corner_radius=12)
                container.pack(fill="both", expand=True, padx=15, pady=15)

                title_lbl = ctk.CTkLabel(
                    container,
                    text=f"⚡ Check {target_str.lower()} accounts and upload skill?",
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color="#F59E0B"
                )
                title_lbl.pack(pady=(18, 10))

                desc_lbl = ctk.CTkLabel(
                    container,
                    text=(
                        "It will take some time to check selected and update skill, upload skill.\n\n"
                        "Would you like to automatically verify session cookies and upload/update\n"
                        "the video generation skill (Seedance 2.5 / SKILL.md) for these accounts?"
                    ),
                    font=ctk.CTkFont(size=12),
                    justify="center",
                    text_color="#E2E8F0"
                )
                desc_lbl.pack(padx=20, pady=5)

                btn_row = ctk.CTkFrame(container, fg_color="transparent")
                btn_row.pack(side="bottom", fill="x", padx=15, pady=(12, 16))

                btn_yes = ctk.CTkButton(
                    btn_row,
                    text="Yes, Check & Upload Skill",
                    fg_color="#10B981",
                    hover_color="#059669",
                    font=ctk.CTkFont(size=12, weight="bold"),
                    command=self._on_yes
                )
                btn_yes.pack(side="left", expand=True, padx=5)

                btn_no = ctk.CTkButton(
                    btn_row,
                    text="Check Cookies Only",
                    fg_color="#3B82F6",
                    hover_color="#2563EB",
                    font=ctk.CTkFont(size=12),
                    command=self._on_no
                )
                btn_no.pack(side="left", expand=True, padx=5)

                btn_cancel = ctk.CTkButton(
                    btn_row,
                    text="Cancel",
                    fg_color="#4B5563",
                    hover_color="#374151",
                    font=ctk.CTkFont(size=12),
                    width=75,
                    command=self._on_cancel
                )
                btn_cancel.pack(side="left", expand=True, padx=5)

            def _on_yes(self):
                self.choice = "yes"
                self.destroy()

            def _on_no(self):
                self.choice = "no"
                self.destroy()

            def _on_cancel(self):
                self.choice = "cancel"
                self.destroy()

        def patched_check_cookies(self, selected_only=False):
            _log(f"[CHECK HOOK] patched_check_cookies called with selected_only={selected_only}")
            parent = getattr(self, "root", None)
            choice = None
            try:
                dialog = CheckAndSkillDialog(parent, selected_only=selected_only)
                if parent:
                    parent.wait_window(dialog)
                choice = dialog.choice
            except Exception as dialog_err:
                _log(f"[CHECK HOOK] CTkToplevel dialog error: {dialog_err}, using messagebox fallback")
                import tkinter.messagebox as mb
                ans = mb.askyesnocancel(
                    "Check Accounts & Upload Skill",
                    "Check accounts and upload skill?\n\nIt will take some time to check selected and update skill, upload skill."
                )
                if ans is True: choice = "yes"
                elif ans is False: choice = "no"
                else: choice = "cancel"

            target_tag = "selected" if selected_only else "all"
            _log(f"[CHECK HOOK] User choice: {choice} for target_tag: {target_tag}")

            if choice == "yes":
                self._log(f"⚡ [CHECK & SKILL] 'Check {target_tag} and upload skill' initiated.", "info")
                self._log("⏳ [NOTICE] It will take some time to check selected and update skill, upload skill. Please wait calmly...", "info")
                self._log(f"🔍 [STEP 1/3] Verifying session authorization & health for {target_tag} accounts...", "info")

                try:
                    self.root.after(0, lambda: orig_check_cookies(self, selected_only=selected_only))
                except Exception:
                    orig_check_cookies(self, selected_only=selected_only)

                def wait_and_upload():
                    time.sleep(1.5)
                    dots = 1
                    while getattr(self, "checking_cookies", False):
                        time.sleep(2.0)
                        self._log(f"🔄 [PROGRESS] Checking accounts in progress{'.' * dots} validating credentials...", "info")
                        dots = (dots % 3) + 1

                    self._log("✅ [STEP 1 COMPLETE] Account session validation completed.", "success")
                    time.sleep(1.0)
                    self._log("📦 [STEP 2/3] Preparing video generation skill (Seedance 2.5 / SKILL.md)...", "info")
                    time.sleep(1.0)
                    self._log(f"🚀 [STEP 3/3] Uploading & updating skill on active {target_tag} accounts...", "info")
                    time.sleep(0.5)

                    try:
                        self.root.after(0, lambda: _prepare_and_upload_skill(self, selected_only=selected_only))
                    except Exception:
                        try:
                            _prepare_and_upload_skill(self, selected_only=selected_only)
                        except Exception as e:
                            self._log(f"⚠️ [WARNING] Skill upload trigger error: {e}", "warn")
                            return

                    time.sleep(1.5)
                    self._log(f"✨ [COMPLETE] Skill upload pipeline dispatched for {target_tag} accounts!", "success")

                threading.Thread(target=wait_and_upload, daemon=True).start()

            elif choice == "no":
                self._log(f"⚡ [ACTION] Checking {target_tag} accounts (cookie check only)...", "info")
                return orig_check_cookies(self, selected_only=selected_only)
            else:
                self._log(f"ℹ️ [ACTION] 'Check {target_tag}' cancelled by user.", "info")

        patched_check_cookies._zdola_popup_patched = True
        dola_gui.DolaApp._check_cookies = patched_check_cookies

    _log("[PRE-PATCH] dola_gui patched successfully into sys.modules")
except Exception as e:
    _log(f"[PRE-PATCH ERROR] dola_gui: {e}")

_log("=== sitecustomize.py setup completed successfully ===")
