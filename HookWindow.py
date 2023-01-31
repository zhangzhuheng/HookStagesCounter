from base64 import b64decode
from ctypes import windll
from io import BytesIO
from tkinter import Tk, Frame, Label, constants
from PIL import ImageTk, Image
from win32con import WS_EX_TOOLWINDOW, WS_EX_APPWINDOW, GWL_EXSTYLE
from queue import Queue, Empty


class HookWindow:
    def __init__(self, messages: Queue):
        self._messages = messages

        self._root = Tk()
        self._root.title('HookWindow')
        self._root.overrideredirect(True)  # 设置隐藏窗口标题栏和任务栏图标
        self._root.attributes('-topmost', True)
        self._root.attributes('-transparentcolor', 'black')

        self._root_x = int(self._root.winfo_screenwidth() * 0.01)
        self._root_y = int(self._root.winfo_screenheight() * 0.4)
        self._root_width = int(self._root.winfo_screenwidth() * 0.02)
        self._root_height = int(self._root_width * 10)
        # print(f'{self._root_x=}, {self._root_y=}, {self._root_width=}, {self._root_height=}')
        self._root.geometry(f'{self._root_width}x{self._root_height}+{self._root_x}+{self._root_y}')

        frame = Frame(self._root, bg='black')
        frame.pack(side=constants.TOP, fill=constants.BOTH, expand=1)

        hook_img_base64 = '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'
        hook_img_width = self._root_width // 2
        hook_img_height = hook_img_width * 4 // 3
        self.hook_img = ImageTk.PhotoImage(
            Image.open(BytesIO(b64decode(hook_img_base64))).resize((hook_img_width, hook_img_height)))

        self.hooks = [[Label(frame, background='black') for _ in range(2)] for _ in range(4)]
        self.counter = [0, 0, 0, 0]
        self.layout_hook()

    def layout_hook(self):
        for i in range(len(self.hooks)):
            self.hooks[i][0].place(anchor=constants.W, relx=0, rely=(0.1 + 0.25 * i))
            self.hooks[i][1].place(anchor=constants.W, relx=0.5, rely=(0.1 + 0.25 * i))

    def reset_hook(self):
        for l1, l2 in self.hooks:
            l1.config(image=''), l2.config(image='')

    def show_hook(self, n: int):
        if self.counter[n] < 2:
            # print(f"show player_{n} hook {self.counter[n]} to {self.counter[n] + 1}")
            self.hooks[n][self.counter[n]].config(image=self.hook_img)
            self.counter[n] += 1

    def hide_hook(self, n: int):
        if self.counter[n] > 0:
            # print(f"hide player_{n} hook {self.counter[n]} to {self.counter[n] - 1}")
            self.counter[n] -= 1
            self.hooks[n][self.counter[n]].config(image='')

    def _set_window(self):
        """
        在任务栏上显示
        """
        hwnd = windll.user32.GetParent(self._root.winfo_id())
        style = windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
        style &= ~WS_EX_TOOLWINDOW
        style |= WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, style)
        # re-assert the new window style
        self._root.withdraw()
        self._root.after(10, self._root.deiconify)

    def _messages_cb(self):
        try:
            event = self._messages.get_nowait()
            match event.name:
                case '1':
                    self.show_hook(0)
                case '!':
                    self.hide_hook(0)
                case '2':
                    self.show_hook(1)
                case '@':
                    self.hide_hook(1)
                case '3':
                    self.show_hook(2)
                case '#':
                    self.hide_hook(2)
                case '4':
                    self.show_hook(3)
                case '$':
                    self.hide_hook(3)
        except Empty:
            pass
        finally:
            self._root.after(10, self._messages_cb)

    def run(self):
        self._root.after(10, self._set_window)
        self._root.after(10, self._messages_cb)
        self._root.mainloop()


if __name__ == "__main__":
    window = HookWindow(Queue())
    window.show_hook(0)
    window.show_hook(0)
    window.show_hook(1)
    window.show_hook(1)
    window.show_hook(2)
    window.show_hook(2)
    window.show_hook(3)
    window.show_hook(3)
    window.run()

#
# import tkinter as tk
# import tkinter.font as tkFont
#
# class App:
#     def __init__(self, root):
#         #setting title
#         root.title("undefined")
#         #setting window size
#         width=120
#         height=533
#         screenwidth = root.winfo_screenwidth()
#         screenheight = root.winfo_screenheight()
#         alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
#         root.geometry(alignstr)
#         root.resizable(width=False, height=False)
#
#         GLabel_885=tk.Label(root)
#         ft = tkFont.Font(family='Times',size=10)
#         GLabel_885["font"] = ft
#         GLabel_885["fg"] = "#333333"
#         GLabel_885["justify"] = "center"
#         GLabel_885["text"] = ""
#         GLabel_885.place(x=0,y=0,width=120,height=60)
#
#         GLabel_241=tk.Label(root)
#         ft = tkFont.Font(family='Times',size=10)
#         GLabel_241["font"] = ft
#         GLabel_241["fg"] = "#333333"
#         GLabel_241["justify"] = "center"
#         GLabel_241["text"] = ""
#         GLabel_241.place(x=0,y=100,width=120,height=60)
#
#         GLabel_576=tk.Label(root)
#         ft = tkFont.Font(family='Times',size=10)
#         GLabel_576["font"] = ft
#         GLabel_576["fg"] = "#333333"
#         GLabel_576["justify"] = "center"
#         GLabel_576["text"] = ""
#         GLabel_576.place(x=0,y=200,width=120,height=60)
#
#         GLabel_826=tk.Label(root)
#         ft = tkFont.Font(family='Times',size=10)
#         GLabel_826["font"] = ft
#         GLabel_826["fg"] = "#333333"
#         GLabel_826["justify"] = "center"
#         GLabel_826["text"] = ""
#         GLabel_826.place(x=0,y=300,width=120,height=60)
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = App(root)
#     root.mainloop()
