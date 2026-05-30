from backend.brain import knowledgeBrain
from backend.ingestor import DocumentIngester
from backend.vault import VectorVault

class CogniFlow:
    def __init__(self) -> None:
        self.brain = knowledgeBrain()
        self.ingester = DocumentIngester()
        self.vault = VectorVault()
        
    def ask_question(self, question: str):
        chunks = self.vault.search(question)

        return self.brain.ask(question, chunks)