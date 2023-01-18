from win32api import RGB
from win32ui import GetDeviceCaps
from win32gui import PostQuitMessage, BeginPaint, LOGFONT, CreateFontIndirect, SelectObject, SetTextColor, \
    GetClientRect, DrawText, EndPaint, DefWindowProc, WNDCLASS, GetStockObject, RegisterClass, CreateWindowEx, \
    SetLayeredWindowAttributes, UpdateWindow, SetWindowPos, PumpWaitingMessages, ShowWindow, InvalidateRect, \
    DestroyWindow
from win32con import WM_DESTROY, WM_PAINT, LOGPIXELSX, DT_CENTER, DT_NOCLIP, NONANTIALIASED_QUALITY, WHITE_BRUSH, \
    WS_EX_COMPOSITED, WS_EX_LAYERED, WS_EX_NOACTIVATE, WS_EX_TOPMOST, WS_EX_TRANSPARENT, WS_DISABLED, WS_POPUP, \
    WS_VISIBLE, LWA_COLORKEY, LWA_ALPHA, HWND_TOP, SWP_NOMOVE, SWP_NOSIZE, SWP_SHOWWINDOW, SW_SHOW
from queue import Queue

__all__ = ['TextWindow']


class TextWindow:
    counter_a, counter_b, counter_c, counter_d = 0, 0, 0, 0

    def __init__(self, messages: Queue):
        self._messages = messages

    def run(self):
        """

        [扩展的窗口样式](https://learn.microsoft.com/zh-cn/windows/win32/winmsg/extended-window-styles)
        [窗口样式](https://learn.microsoft.com/zh-cn/windows/win32/winmsg/window-styles)
        [创建窗口](https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-createwindowexa)
        [SetLayeredWindowAttributes 函数](https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-setlayeredwindowattributes)
        # https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-setwindowpos
        # https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-showwindow
        # https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-updatewindow
        """
        dwExStyle = WS_EX_COMPOSITED | WS_EX_LAYERED | WS_EX_NOACTIVATE | WS_EX_TOPMOST | WS_EX_TRANSPARENT
        # The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
        lpClassName = self._register_class()
        lpWindowName = None
        style = WS_DISABLED | WS_POPUP | WS_VISIBLE
        x, y, width, height = 150, 650, 50, 450

        hwnd = CreateWindowEx(dwExStyle, lpClassName, lpWindowName, style, x, y, width, height, None, None, None, None)
        SetLayeredWindowAttributes(hwnd, 0x00ffffff, 255, LWA_COLORKEY | LWA_ALPHA)
        SetWindowPos(hwnd, HWND_TOP, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)
        ShowWindow(hwnd, SW_SHOW)
        UpdateWindow(hwnd)

        while True:
            PumpWaitingMessages()
            msg = self._messages.get()
            if msg:
                print(msg)
            if msg == 'DestroyWindow':
                DestroyWindow(hwnd)
                return
            elif msg == 'InvalidateRect':
                InvalidateRect(hwnd, None, True)
            else:
                raise ValueError('Undefined messages')

    @staticmethod
    def _register_class() -> int:
        """

        [WNDCLASSA 结构](https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/ns-winuser-wndclassa)
        [WNDPROC 回调函数](https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nc-winuser-wndproc)
        [GetStockObject 函数](https://learn.microsoft.com/zh-cn/windows/win32/api/wingdi/nf-wingdi-getstockobject)
        [registerClassA 函数](https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-registerclassa)
        """

        wndClass = WNDCLASS()  # win32gui does not support WNDCLASSEX.
        wndClass.lpfnWndProc = TextWindow.window_proc
        wndClass.hbrBackground = GetStockObject(WHITE_BRUSH)
        wndClass.lpszClassName = 'MyWindowClassName'
        return RegisterClass(wndClass)  # win32gui does not support RegisterClassEx

    @staticmethod
    def window_proc(hwnd, umsg, wparam, lparam):
        """[WNDPROC 回调函数](https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nc-winuser-wndproc)

        :param hwnd:
        :param umsg:
        :param wparam:
        :param lparam:
        :return:
        """
        # print(f'call window_proc({hwnd=}, {umsg=}, {wparam=}, {lparam=})')
        if umsg == WM_DESTROY:
            PostQuitMessage(0)
            return 0

        elif umsg == WM_PAINT:
            return TextWindow.paint_proc(hwnd)
        else:
            return DefWindowProc(hwnd, umsg, wparam, lparam)

    @staticmethod
    def paint_proc(hwnd):
        """

        [LOGFONTA 结构](https://learn.microsoft.com/zh-cn/windows/win32/api/wingdi/ns-wingdi-logfonta)
        [DrawText 函数](https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-drawtext)

        :param hwnd:
        :return:
        """
        hdc, paintStruct = BeginPaint(hwnd)

        dpiScale = GetDeviceCaps(hdc, LOGPIXELSX) / 60.0
        fontSize = 38
        lf = LOGFONT()
        lf.lfHeight = int(round(dpiScale * fontSize))
        lf.lfWeight = 0
        lf.lfQuality = NONANTIALIASED_QUALITY  # Use nonantialiased to remove the white edges around the text.
        hf = CreateFontIndirect(lf)

        SelectObject(hdc, hf)
        SetTextColor(hdc, RGB(200, 200, 200))

        data = f'{TextWindow.counter_a}\n\n{TextWindow.counter_b}\n\n{TextWindow.counter_c}\n\n{TextWindow.counter_d}'
        data = (
                '𝗹' * TextWindow.counter_a
                + '\n\n'
                + '𝗹' * TextWindow.counter_b
                + '\n\n'
                + '𝗹' * TextWindow.counter_c
                + '\n\n'
                + '𝗹' * TextWindow.counter_d
        )
        DrawText(hdc, data, -1, GetClientRect(hwnd), DT_CENTER | DT_NOCLIP)
        EndPaint(hwnd, paintStruct)
        return 0
