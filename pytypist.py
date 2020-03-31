#!/home/kajman/projects/pytypist/.pytypist/bin/python
from pynput import keyboard
text = "This is some test text"

def on_press(key):
    try:
        #print('alphanumeric key {0} pressed'.format( key.char))
        if key=='a':
            print('Bravo!')
    except AttributeError:
        print('special key {0} pressed'.format( key))

def on_release(key):
    #print('{0} released'.format( key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
while True:
    sleep.time(0.01)
