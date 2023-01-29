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

        self._root_x = 30
        self._root_y = int(self._root.winfo_screenheight() * 0.4)
        self._root_width = int(self._root.winfo_screenwidth() * 0.04)
        self._root_height = int(self._root_width * 4.5)
        print(f'{self._root_width=}, {self._root_height=}')
        self._root.geometry(f'{self._root_width}x{self._root_height}+{self._root_x}+{self._root_y}')

        frame = Frame(self._root, bg='black')
        frame.pack(side=constants.TOP, fill=constants.BOTH, expand=1)

        hook_img_base64 = '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'
        self.hook_img = ImageTk.PhotoImage(
            Image.open(BytesIO(b64decode(hook_img_base64))).resize((self._root_width // 2, self._root_width // 2)))

        self.hooks = [[Label(frame, background='black') for _ in range(2)] for _ in range(4)]
        self.counter = [0, 0, 0, 0]
        self.layout_hook()

        self._root.after(10, self._set_window)
        self._root.after(100, self._read_queue)

    def _set_window(self):
        """
        在任务栏上显示
        """
        hwnd = windll.user32.GetParent(self._root.winfo_id())
        style = windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW
        style = style | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, style)
        # re-assert the new window style
        self._root.withdraw()
        self._root.after(10, self._root.deiconify)

    def layout_hook(self):
        for i in range(len(self.hooks)):
            self.hooks[i][0].place(anchor=constants.W, relx=0, rely=(0.1 + 0.25 * i))
            self.hooks[i][1].place(anchor=constants.W, relx=0.5, rely=(0.1 + 0.25 * i))

    def reset_hook(self):
        for l1, l2 in self.hooks:
            l1.config(image=''), l2.config(image='')

    def show_hook(self, n: int):
        if self.counter[n] < 2:
            print(f'show player_{n} hook {self.counter[n]} to {self.counter[n] + 1}')
            self.hooks[n][self.counter[n]].config(image=self.hook_img)
            self.counter[n] += 1

    def hide_hook(self, n: int):
        if self.counter[n] > 0:
            print(f'hide player_{n} hook {self.counter[n]} to {self.counter[n] - 1}')
            self.counter[n] -= 1
            self.hooks[n][self.counter[n]].config(image='')

    def _read_queue(self):
        """ Check if there is something in the queue. """
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
            self._root.after(100, self._read_queue)

    def run(self):
        self._root.mainloop()


if __name__ == "__main__":
    window = HookWindow(Queue())
    window.show_hook(0)
    window.show_hook(1)
    window.show_hook(2)
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
