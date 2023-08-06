import time
import ctypes
import random
import win32con
import win32gui
import win32api

class SupyCool:
    class cursor:
        @staticmethod
        def DrawIcon(icon_ids=[]):
            user32 = ctypes.windll.user32
            gdi32 = ctypes.windll.gdi32
            hwnd = win32gui.GetDesktopWindow()
            hdc = user32.GetDC(hwnd)
            icon_size = win32api.GetSystemMetrics(win32con.SM_CXICON)

            # Save the original cursor.
            original_cursor = user32.CopyIcon(user32.GetCursor())

            while True: # Funny fucking=）
                point = win32gui.GetCursorPos()

                # Draw original icons.
                user32.DrawIcon(hdc, point[0], point[1], original_cursor)

                for i, icon_id in enumerate(icon_ids):
                    hicon = user32.LoadImageW(None, icon_id, win32con.IMAGE_ICON, icon_size, icon_size, win32con.LR_DEFAULTCOLOR | win32con.LR_SHARED)
                    user32.DrawIcon(hdc, point[0] + (i + 1) * icon_size, point[1] + (i + 1) * icon_size, hicon)

                # flush
                user32.UpdateWindow(hwnd)

                time.sleep(0.001)
        @staticmethod
        def Jitter(sway=2):
            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32
            class POINT(ctypes.Structure):
                 _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
            x, y, a = 0, 0, 0
            p = POINT()
            while True: # Funny fucking=)
                user32.GetCursorPos(ctypes.byref(p))
                x = random.randint(0, sway)
                y = random.randint(0, sway)
                a = random.randint(0, 1)

                if a == 1:
                    user32.SetCursorPos(p.x + x, p.y + y)
                elif a == 0:
                    user32.SetCursorPos(p.x - x, p.y - y)

                kernel32.Sleep(15)
    class screen:
        @staticmethod
        def InvertColor(sleep_time=1):
            class RECT(ctypes.Structure):
                _fields_ = [("left", ctypes.c_long),
                            ("top", ctypes.c_long),
                            ("right", ctypes.c_long),
                            ("bottom", ctypes.c_long)]
            user32 = ctypes.WinDLL("user32.dll")
            gdi32 = ctypes.WinDLL("gdi32.dll")
            desktop = user32.GetDesktopWindow()
            hdc = user32.GetWindowDC(desktop)
            rect = RECT()
            user32.GetWindowRect(desktop, ctypes.byref(rect))
            while True: # Funny fucking=)
                gdi32.BitBlt(hdc, 0, 0, rect.right - rect.left, rect.bottom - rect.top, hdc, 0, 0, 3342344)
                time.sleep(sleep_time)
            user32.ReleaseDC(desktop, hdc)
        @staticmethod
        def ChaosBlock(sleep_time=0.1):
            SRCCOPY = 0x00CC0020
            CAPTUREBLT = 0x40000000
            bitblt = ctypes.windll.gdi32.BitBlt
            user32 = ctypes.windll.user32
            screen_width = user32.GetSystemMetrics(0)
            screen_height = user32.GetSystemMetrics(1)
            hdc_src = user32.GetDC(0)
            try:
                while True: # Funny fucking=)
                    x_src = random.randint(0, screen_width)
                    y_src = random.randint(0, screen_height)
                    width = random.randint(100, screen_width)
                    height = random.randint(100, screen_height)
                    x_dst = random.randint(0, screen_width)
                    y_dst = random.randint(0, screen_height)
                    bitblt(hdc_src, x_dst, y_dst, width, height, hdc_src, x_src, y_src, SRCCOPY | CAPTUREBLT)
                    time.sleep(sleep_time)
            finally:
                user32.ReleaseDC(0, hdc_src)
        @staticmethod
        def Tunnel(sleep_time=1):
            user32 = ctypes.windll.user32
            gdi32 = ctypes.windll.gdi32
            desktop = user32.GetDesktopWindow()
            hdc = user32.GetWindowDC(desktop)
            class POINT(ctypes.Structure):
                _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
            while True: # Funny fucking=)
                width = user32.GetSystemMetrics(1)
                height = user32.GetSystemMetrics(0)
                point = POINT()
                user32.GetCursorPos(ctypes.byref(point))
                user32.DrawIcon(hdc, point.x - 5, point.y - 5, user32.LoadIconW(None, 32513))
                randx = random.randint(0, width)
                randy = random.randint(0, height)
                desktop_dc = user32.GetDC(None)
                gdi32.BitBlt(desktop_dc, random.randint(0, width), random.randint(0, height), randx + 200, randy + 200, desktop_dc, randx, randy, 0x00CC0020)
                user32.ReleaseDC(None, desktop_dc)
                a = user32.GetSystemMetrics(1)
                b = user32.GetSystemMetrics(0)
                gdi32.StretchBlt(user32.GetDC(None), 50, 50, a - 100, b - 100, user32.GetDC(None), 0, 0, a, b, 0x00CC0020)
                time.sleep(sleep_time)
        @staticmethod
        def GrayMirror():
            user32 = ctypes.windll.user32
            gdi32 = ctypes.windll.gdi32
            screen_width = user32.GetSystemMetrics(0)
            screen_height = user32.GetSystemMetrics(1)
            desktop_dc = user32.GetDC(0)
            mem_dc = gdi32.CreateCompatibleDC(desktop_dc)
            bitmap = gdi32.CreateCompatibleBitmap(desktop_dc, screen_width, screen_height)
            gdi32.SelectObject(mem_dc, bitmap)
            gdi32.BitBlt(mem_dc, 0, 0, screen_width, screen_height, desktop_dc, 0, 0, 0x00CC0020)
            buffer_size = screen_width * screen_height * 4
            buffer = ctypes.create_string_buffer(buffer_size)
            gdi32.GetBitmapBits(bitmap, buffer_size, buffer)
            for i in range(screen_width * screen_height):
                b, g, r, _ = buffer[i * 4:i * 4 + 4]
                gray = int(0.3 * r + 0.59 * g + 0.11 * b)
                buffer[i * 4:i * 4 + 3] = bytes((gray, gray, gray))
            gdi32.SetBitmapBits(bitmap, buffer_size, buffer)
            gdi32.BitBlt(desktop_dc, 0, 0, screen_width, screen_height, mem_dc, 0, 0, 0x00CC0020) # Funny fucking=)
            gdi32.DeleteObject(bitmap)
            gdi32.DeleteDC(mem_dc)
            user32.ReleaseDC(0, desktop_dc)
    class window:
        @staticmethod
        def ShakeFirst():
            user32 = ctypes.windll.user32
            user32.GetWindowRect.restype = ctypes.c_bool
            user32.MoveWindow.restype = ctypes.c_bool
            hwnd = user32.GetForegroundWindow()
            class RECT(ctypes.Structure):
                _fields_ = [("left", ctypes.c_long),
                            ("top", ctypes.c_long),
                            ("right", ctypes.c_long),
                            ("bottom", ctypes.c_long)]
            while True: # Funny fucking=)
                current_hwnd = user32.GetForegroundWindow()
                if current_hwnd != hwnd: # If first window isn't original window.
                    hwnd = current_hwnd
                rect = RECT()
                user32.GetWindowRect(hwnd, ctypes.byref(rect))
                shake_amount = random.randint(10, 50)
                user32.MoveWindow(hwnd, rect.left, rect.top + shake_amount, rect.right - rect.left, rect.bottom - rect.top, True)
                time.sleep(0.1)
                user32.MoveWindow(hwnd, rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top, True)
                time.sleep(0.1)
        @staticmethod
        def MinimizeAll():
            keybd_event = ctypes.windll.user32.keybd_event
            VK_LWIN = 0x5B
            VK_M = 0x4D
            KEYEVENTF_KEYUP = 0x2
            keybd_event(VK_LWIN, 0, 0, 0)
            keybd_event(VK_M, 0, 0, 0)
            keybd_event(VK_M, 0, KEYEVENTF_KEYUP, 0)
            keybd_event(VK_LWIN, 0, KEYEVENTF_KEYUP, 0) # Funny fucking=)
if __name__ == "__main__":
    # 自定义图标列表
    my_icon_ids = [
        win32con.IDI_ERROR,  # 错误图标
        win32con.IDI_QUESTION,  # 问题图标
        win32con.IDI_INFORMATION,  # 信息图标
        win32con.IDI_WARNING
    ]

# SupyCool.cursor.DrawIcon(my_icon_ids)
# SupyCool.cursor.Jitter(2)
# SupyCool.screen.InvertColor(1)
# SupyCool.screen.ChaosBlock()
# SupyCool.screen.Tunnel()
# SupyCool.screen.GrayMirror()
# SupyCool.window.ShakeFirst()
# SupyCool.window.MinimizeAll()
