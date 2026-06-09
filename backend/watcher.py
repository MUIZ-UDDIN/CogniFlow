from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from backend.ingestor import DocumentIngester
from backend.vault import VectorVault
import time
import json
import asyncio
import os


class watcher(PatternMatchingEventHandler):

    def __init__(self, connections_list: list, loop) -> None:
        
        super().__init__(patterns=["*.pdf"], ignore_directories=True)
        self.ingestor = DocumentIngester()
        self.vault = VectorVault()
        self.connections_list = connections_list
        self.loop = loop

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
                asyncio.run_coroutine_threadsafe(ws.send_text(json_message), self.loop)
            except Exception as e:
                print(f"Failed to alert a browser tab: {e}")


def start_watcher(path_to_watch="./documents/", connections_list= None, loop= None):
    if connections_list is None:
        connections_list = []

    if loop is None:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

    event_handler=watcher(connections_list, loop)

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