import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class GitHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            os.system('git add .')
            os.system('git commit -m "Auto update"')
            os.system('git push origin main')

path = '.'
event_handler = GitHandler()
observer = Observer()
observer.schedule(event_handler, path, recursive=True)
observer.start()

try:
    while True:
        time.sleep(2)
except KeyboardInterrupt:
    observer.stop()
observer.join()