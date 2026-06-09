from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from backend.ingestor import DocumentIngester
from backend.vault import VectorVault
import time
import json
import asyncio
import os


class watcher(PatternMatchingEventHandler):

    def __init__(self) -> None:
        
        super().__init__(patterns=["*.pdf"], ignore_directories=True)
        self.ingestor = DocumentIngester()
        self.vault = VectorVault()
        self.connection_list = connection_list

    def on_created(self, event):
        file_path = event.src_path
        print(f"New file detected, waiting for copy to finish: {file_path}")
        time.sleep(3)

        chunks = self.ingestor.Reader(file_path)
        self.vault.add_documents(chunks)
        
        print(f"Successfully processed {file_path}")

        just_filename = os.path.basename(file_path)
        payload = {
            "type": "new_file",
            "name": just_filename
        }

        json_message = json.dumps(payload)

        for ws in self.connections_list:
            try:
                # Fetch the active FastAPI event loop
                loop = asyncio.get_event_loop()
                # Safely deliver the package from this standard thread to the async loop
                asyncio.run_coroutine_threadsafe(ws.send_text(json_message), loop)
            except Exception as e:
                print(f"Failed to alert a browser tab: {e}")


def start_watcher(path_to_watch="./documents/", connection_list= None):
    if connection_list is None:
        connection_list = []

    event_handler=watcher(connection_list)

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
        print("\nStopping watcher...")
    finally:
        # This ALWAYS runs, preventing ghost background threads
        engine.stop()
        engine.join()
        print("Watcher stopped cleanly.")