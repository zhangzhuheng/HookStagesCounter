from queue import Queue
from threading import Thread
from keyboard import on_press_key
from PySimpleGUI import Window, Button, WIN_CLOSED

from text_window import TextWindow


def cb(e):
    match e.name:
        case '1':
            TextWindow.counter_a = TextWindow.counter_a + 1 if TextWindow.counter_a <= 1 else TextWindow.counter_a
        case '!':
            TextWindow.counter_a = TextWindow.counter_a - 1 if TextWindow.counter_a >= 1 else TextWindow.counter_a
        case '2':
            TextWindow.counter_b = TextWindow.counter_b + 1 if TextWindow.counter_b <= 1 else TextWindow.counter_b
        case '@':
            TextWindow.counter_b = TextWindow.counter_b - 1 if TextWindow.counter_b >= 1 else TextWindow.counter_b
        case '3':
            TextWindow.counter_c = TextWindow.counter_c + 1 if TextWindow.counter_c <= 1 else TextWindow.counter_c
        case '#':
            TextWindow.counter_c = TextWindow.counter_c - 1 if TextWindow.counter_c >= 1 else TextWindow.counter_c
        case '4':
            TextWindow.counter_d = TextWindow.counter_d + 1 if TextWindow.counter_d <= 1 else TextWindow.counter_d
        case '$':
            TextWindow.counter_d = TextWindow.counter_d - 1 if TextWindow.counter_d >= 1 else TextWindow.counter_d
    messages.put('InvalidateRect')


if __name__ == '__main__':

    messages = Queue()
    tw = TextWindow(messages)

    layout = [[Button('On', size=(10, 2), button_color='white on green', key='-B-')]]

    window = Window('Realtime Shell Command Output', layout, size=(300, 100), element_justification='center')

    while True:  # Event Loop
        event, values = window.read()
        print(event, values)
        if event == '-B-':  # if the normal button that changes color and text

            Thread(target=tw.run).start()

            on_press_key('1', cb)
            on_press_key('2', cb)
            on_press_key('3', cb)
            on_press_key('4', cb)

            window['-B-'].update(text='Running', disabled=True, button_color='white on red')
        elif event == WIN_CLOSED:
            messages.put('DestroyWindow')
            break
    window.close()
