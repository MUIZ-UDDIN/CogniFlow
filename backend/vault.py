import chromadb
from backend.ingestor import DocumentIngester
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
            safe_filename = chunk["file_name"].replace(" ","_")
            ids.append(f"{safe_filename}_chunk_{index}")
            metas.append(Mt_data)

        self.collected_data.upsert(
            documents=docs,
            metadatas=metas, # type: ignore
            ids=ids
        )

    def search(self, question: str, file_name: str = None, n_result: int=7) -> list:
        print(f"DEBUG: Searching for file name -> '{file_name}'")
        if file_name:
            Ans = self.collected_data.query(
                query_texts=[question],
                n_results=n_result,
                where={"file_name": file_name}
            )

        else:
            Ans = self.collected_data.query(
                query_texts=[question],
                n_results=n_result,
            )     

        text_list = Ans["documents"][0] if Ans["documents"] else []
        meta_list = Ans["metadatas"][0] if Ans["metadatas"] else []

        result = []

        for index in range(len(text_list)):

            chunk_dic = {
                "text": text_list[index],
                "file": meta_list[index]["file_name"],
                "page": meta_list[index]["page_number"]
            }

            result.append(chunk_dic)
            
        return result

    def count(self) -> int:
        return self.collected_data.count()


if __name__ == "__main__":
    folderPath = "../documents/"
    if os.path.exists(folderPath):
        Data = Worker.Reader(folderPath)
        engine = VectorVault()
        result = engine.add_documents(Data)

        test = engine.search("who is the document for?")
        print(f"iteams saved in vault: {engine.collected_data.count()}")

    else:
        print(f"Test folder path '{folderPath}' not found. Skipping ingest test.")
    
