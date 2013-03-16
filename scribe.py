#!/usr/bin/env python
import os
import sys
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


# Add current directory to path so we can import settings.
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import settings


__version__ = '0.1'


class PhotoEventHandler(FileSystemEventHandler):
    """
    Searches for photos in a certain folder structure and triggers processing
    on them.
    """
    def dispatch(self, event):
        print event


if __name__ == '__main__':
    handler = PhotoEventHandler()
    observer = Observer()
    observer.schedule(handler, path=settings.PHOTO_DIRECTORY, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
