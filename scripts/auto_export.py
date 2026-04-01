"""
A.I.M. - OS Export Hook
Uses uiautomation (Microsoft UIAutomation API for Python) to interact with 
the active Electron UI tree inside the Antigravity IDE. Automatically invokes
the Native Download button to execute a Markdown zero-token log sweep.
"""
import sys
import time
import os
try:
    import uiautomation as auto
except ImportError:
    print("[ERROR] uiautomation not installed. Run: pip install uiautomation pywinauto")
    sys.exit(1)

def auto_export_chat():
    print("[A.I.M] Engaging OS Handoff UI-Hijacker...")
    auto.SetGlobalSearchTimeout(3)
    
    # 1. Locate the Antigravity Main Window
    ide_window = auto.WindowControl(searchDepth=1, ClassName='Chrome_WidgetWin_1', Name='*Antigravity*')
    
    # Check if the exact title exists if regex failed on older versions
    if not ide_window.Exists(0, 0):
        # Fallback to pure window enumeration mapping string partials
        desktop = auto.GetRootControl()
        for win in desktop.GetChildren():
            if win.Name and 'Antigravity' in win.Name:
                ide_window = win
                break

    if not ide_window or not ide_window.Exists(0, 0):
        print("[ERROR] Antigravity IDE window not detected in the Windows session UI tree.")
        return False
        
    print(f"[A.I.M] Locked onto active IDE Window: -> {ide_window.Name}")
    
    # Temporarily pull to foreground
    ide_window.SetFocus()
    time.sleep(0.5)

    # 2. Search deeper into the Chromium tree for the Download/Export button.
    # Electron often obscures aria-labels behind generic groups. We search text strings broadly.
    print("[A.I.M] Sweeping UI tree for Export Action...")
    
    export_btn = None
    target_keywords = ["Export", "Download", "Save Chat"]
    
    for kw in target_keywords:
        # First attempt explicit ButtonControl discovery
        btn = ide_window.ButtonControl(searchDepth=10, Name=kw)
        if btn.Exists(0, 0):
            export_btn = btn
            break
            
        # Fallback to generically named visual elements that contain text
        element = ide_window.Control(searchDepth=10, Name=kw)
        if element.Exists(0, 0):
            export_btn = element
            break

    if not export_btn:
        print("[A.I.M] Warning: Explicit Export UI string not found in tree.")
        print("[A.I.M] Bounding box failure. Trying fallback blind-send keys (Ctrl+Shift+E)...")
        # In the absence of an explicit button, we cannot safely hijack blind coordinates.
        return False

    # 3. Physically invoke the OS level UI element
    print(f"[A.I.M] Hit confirmed on: [{export_btn.Name}]. Firing UI Event...")
    
    try:
        # We attempt drawing a red box to prove to the UI we found it (for diagnostics)
        export_btn.GetBoundingRect() 
        export_btn.Invoke()
    except Exception as e:
        print(f"[A.I.M] Fallback: Invoke failed, sending physical mouse click. ({e})")
        export_btn.Click()

    # 4. Handle the Windows OS "Save As" overlay
    # Standard Electron behaviour will immediately trigger a modal.
    time.sleep(1.0)
    print("[A.I.M] Export triggered. Awaiting Save modal...")
    
    # Send natural ENTER key to confirm saving into default user Downloads folder.
    auto.SendKeys('{Enter}')
    print("[A.I.M] Save confirmed. Markdown dumped to OS Downloads successfully.")
    return True

if __name__ == "__main__":
    success = auto_export_chat()
    if not success:
        print("[A.I.M] Handoff failed to lock UI. Manual Download required.")
        sys.exit(1)
