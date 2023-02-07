from HookStagesWindow import HookStagesWindow
from keyboard import on_press_key

if __name__ == '__main__':
    w = HookStagesWindow()
    on_press_key('1', lambda event: w.show_hook(0) if event.name == '1' else w.hide_hook(0))
    on_press_key('2', lambda event: w.show_hook(1) if event.name == '2' else w.hide_hook(1))
    on_press_key('3', lambda event: w.show_hook(2) if event.name == '3' else w.hide_hook(2))
    on_press_key('4', lambda event: w.show_hook(3) if event.name == '4' else w.hide_hook(3))
    on_press_key('0', lambda event: w.reset_hook())
    w.run()
