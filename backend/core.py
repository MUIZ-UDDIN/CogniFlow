from backend.brain import knowledgeBrain
from backend.ingestor import DocumentIngester
from backend.vault import VectorVault
import os

class CogniFlow:
    def __init__(self) -> None:
        self.brain = knowledgeBrain()
        self.ingester = DocumentIngester()
        self.vault = VectorVault()

        check = self.vault.count()
        if check == 0:
            read = self.ingester.Reader("./documents/")
            self.vault.add_documents(read)
            print(f"Added {len(read)} documents to vector store")

        else:
            print("Vector store already has documents")
        
    def ask_question(self, question: str, file_name: str = None):
        chunks = self.vault.search(question, file_name=file_name)

        return self.brain.ask(question, chunks)