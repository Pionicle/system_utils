"""Watch for folder, log new file, show deleted files."""

from watchdog.observers import Observer
from watchdog.events import (
    FileSystemEventHandler,
    FileDeletedEvent,
    DirCreatedEvent,
    FileCreatedEvent,
)
import logging
import sys
import subprocess
from tabulate import tabulate

files = {"created_files": [], "deleted_files": []}


class MyEventHandler(FileSystemEventHandler):
    """Handler for watch new and deleted file events."""

    def __init__(self, logger: logging):
        super().__init__()
        self.logger = logger

    def on_created(self, event: DirCreatedEvent | FileCreatedEvent):
        if not event.is_directory:
            file = event.src_path
            files["created_files"].append(file)
            self.logger.info(f"Created file: {file}")

    def on_deleted(self, event: DirCreatedEvent | FileCreatedEvent):
        if not event.is_directory:
            file = event.src_path
            files["deleted_files"].append(file)
            self.logger.info(f"Deleted file: {file}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    file_handler = logging.FileHandler("logs")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.propagate = False

    path = sys.argv[1] if len(sys.argv) > 1 else "."
    my_handler = MyEventHandler(logger)
    file_observer = Observer()
    file_observer.schedule(
        my_handler,
        path,
        recursive=True,
        event_filter=[FileCreatedEvent, FileDeletedEvent],
    )
    file_observer.start()
    try:
        while file_observer.is_alive():
            file_observer.join(1)
            subprocess.run("clear")
            print(tabulate(files, headers="keys"))
    finally:
        file_observer.stop()
        file_observer.join()
