import chromadb
from ingestor import DocumentIngester
from chromadb.utils import embedding_functions

Worker = DocumentIngester()

class VectorVault:
    def __init__(self) -> None:
        self.DB_path = chromadb.PersistentClient(path="./Database")
        self.brain = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        self.collected_data = self.DB_path.get_or_create_collection(name="embaded_db", embedding_function=self.brain) #type: ignore

    def add_documents(self, chunks: list):
        docs = []
        metas = []
        ids = []

        for index, chunk in enumerate(chunks):
            docs.append(chunk["Content"])
            Mt_data = {
                "file_name":chunk["file_name"],
                "page_number":chunk["page_number"]
            }
            ids.append(f"id_{index}")
            metas.append(Mt_data)

        self.collected_data.upsert(
            documents=docs,
            metadatas=metas, # type: ignore
            ids=ids
        )

    def search(self, question: str, n_result: int=3) -> list:
        Ans = self.collected_data.query(
            query_texts=[question],
            n_results=n_result
            )

        result = Ans["documents"]

        return result[0] if result else []



if __name__ == "__main__":
    folderPath = "./documents/"
    Data = Worker.Reader(folderPath)
    engine = VectorVault()
    result = engine.add_documents(Data)
    test = engine.search("who is the document for?")
    print(f"iteams saved in vault: {engine.collected_data.count()}")
    print(test)
    
