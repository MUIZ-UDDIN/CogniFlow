import pymupdf
import os
import logging

class DocumentIngester():

    def Reader(self, folder: str) -> list:
        all_chunks = []

        for files in os.listdir(folder):
            try:
                if files.endswith(".pdf"):
                    file_path = os.path.join(folder, files)
                    file = pymupdf.open(file_path)
                    Page_count = len(file)
                    for pages_num in range(Page_count):
                        page_num = file[pages_num]
                        texts = page_num.get_text()

                        for text in range(0, len(texts), 800):

                            chunk = texts[text: text + 1000]

                            all_chunks.append(
                                {"file_name":files,
                                "page_number": pages_num+1,
                                "Content": chunk}
                            )
            except Exception as e:

                logging.info(f"Required files are not found: {e}")

        return all_chunks


if __name__ == "__main__":
    folderPath = "D:\\Projects\\CogniFlow\\documents\\"
    engine = DocumentIngester()
    result = engine.Reader(folderPath)
    print(result)
