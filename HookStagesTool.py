from HookWindow import HookWindow
from keyboard import on_press_key

if __name__ == '__main__':
    hw = HookWindow()
    on_press_key('1', lambda event: hw.show_hook(0) if event.name == '1' else hw.hide_hook(0))
    on_press_key('2', lambda event: hw.show_hook(1) if event.name == '2' else hw.hide_hook(1))
    on_press_key('3', lambda event: hw.show_hook(2) if event.name == '3' else hw.hide_hook(2))
    on_press_key('4', lambda event: hw.show_hook(3) if event.name == '4' else hw.hide_hook(3))
    on_press_key('0', lambda event: hw.reset_hook())
    hw.run()
