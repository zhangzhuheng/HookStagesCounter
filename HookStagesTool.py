from queue import Queue
from keyboard import on_press_key

from HookWindow import HookWindow

if __name__ == '__main__':

    messages = Queue()
    hw = HookWindow(messages)
    on_press_key('1', lambda event: messages.put(event))
    on_press_key('2', lambda event: messages.put(event))
    on_press_key('3', lambda event: messages.put(event))
    on_press_key('4', lambda event: messages.put(event))
    hw.run()

