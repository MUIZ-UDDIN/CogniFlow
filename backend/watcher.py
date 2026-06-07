from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from backend.ingestor import DocumentIngester
from backend.vault import VectorVault
import time


class watcher(PatternMatchingEventHandler):

    def __init__(self) -> None:
        
        super().__init__(patterns=["*.pdf"], ignore_directories=True)
        self.ingestor = DocumentIngester()
        self.vault = VectorVault()

    def on_created(self, event):
        file_path = event.src_path
        print(f"New file detected, waiting for copy to finish: {file_path}")
        time.sleep(3)

        chunks = self.ingestor.Reader(file_path)
        self.vault.add_documents(chunks)
        
        print(f"Successfully processed {file_path}")

    def start_watcher(path_to_watch="./documents/"):
        event_handler=watcher()

        obs = Observer()
        obs.schedule(event_handler=event_handler, path=path_to_watch, recursive=True)
        obs.start()

        print(f"Watcher started on path: {path_to_watch}")  
        return obs

if __name__ == "__main__":

    engine = start_watcher()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        Obs.stop()
    Obs.join()