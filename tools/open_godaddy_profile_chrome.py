"""Open GoDaddy DNS in the existing Pink Primary Chrome. Do not kill Chrome. Do not touch Xero."""
from __future__ import annotations

import sys
import time
import win32api
import win32con
import win32gui

sys.path.insert(
    0,
    r"C:\Users\HuongBui\OneDrive - Pink Accounting & Tax Solutions Pty Ltd\_PinkOps\Workspaces\serviceprofit-channels-20260911",
)
import chrome_drive as cd  # type: ignore

URL = "https://dcc.godaddy.com/control/dnsmanagement?domainName=pinktax.com.au"
EV = cd.EV


def send_hotkey(*vks: int) -> None:
    for vk in vks:
        win32api.keybd_event(vk, 0, 0, 0)
        time.sleep(0.03)
    for vk in reversed(vks):
        win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.03)


def pick_hwnd() -> int:
    # Prefer the live Pink workspace window. Never the MCP "Pages" Chrome.
    h = cd.find_chrome("Facebook")
    if h:
        return h
    hits = []

    def vis(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return
        if win32gui.GetClassName(hwnd) != "Chrome_WidgetWin_1":
            return
        t = win32gui.GetWindowText(hwnd)
        if not t or t == "PreWarm Empty Addin":
            return
        if "Pages - Google Chrome" in t:
            return
        r = win32gui.GetWindowRect(hwnd)
        hits.append((hwnd, t, r))

    win32gui.EnumWindows(vis, None)
    if not hits:
        raise SystemExit("NO_PINK_CHROME")
    hits.sort(key=lambda x: (x[2][2] - x[2][0]) * (x[2][3] - x[2][1]), reverse=True)
    return hits[0][0]


def main() -> None:
    hwnd = pick_hwnd()
    title = win32gui.GetWindowText(hwnd)
    rect = win32gui.GetWindowRect(hwnd)
    print("PICK", hwnd, title, rect)
    # Same window can hold Xero. Never Ctrl+L while Xero is the current tab.
    # Ctrl+T opens a new blank tab in this profile, then we address that tab.
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 40, 40, 1400, 900, 0)
    time.sleep(0.4)
    cd.activate(hwnd)
    time.sleep(0.3)
    send_hotkey(win32con.VK_CONTROL, ord("T"))
    time.sleep(0.8)
    title2 = win32gui.GetWindowText(hwnd)
    print("AFTER_NEWTAB", title2)
    if "Xero" in title2:
        raise SystemExit("STILL_ON_XERO_AFTER_CTRL_T")
    import win32clipboard

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, URL)
    win32clipboard.CloseClipboard()
    send_hotkey(win32con.VK_CONTROL, ord("L"))
    time.sleep(0.2)
    send_hotkey(win32con.VK_CONTROL, ord("V"))
    time.sleep(0.2)
    send_hotkey(win32con.VK_RETURN)
    time.sleep(4.5)
    cd.shot(hwnd, "godaddy_open.png")
    print("OPENED", URL, "TITLE", win32gui.GetWindowText(hwnd))


if __name__ == "__main__":
    main()
