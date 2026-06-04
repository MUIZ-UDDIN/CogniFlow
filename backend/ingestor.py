import pymupdf
import os
import logging

class DocumentIngester():

    def Reader(self, target_path: str) -> list:
        all_chunks = []
        files_to_process = []

        # 1. Determine if the path is a folder or a single file
        if os.path.isdir(target_path):
            # It's a folder, get all PDF files inside it
            for file_name in os.listdir(target_path):
                if file_name.endswith(".pdf"):
                    files_to_process.append(os.path.join(target_path, file_name))
        elif os.path.isfile(target_path) and target_path.endswith(".pdf"):
            # It's a single PDF file, add it directly to our processing list
            files_to_process.append(target_path)
        else:
            logging.info(f"Provided path is neither a valid directory nor a PDF file: {target_path}")
            return all_chunks

        # 2. Process the collected files
        for file_path in files_to_process:
            try:
                # Extract just the file name (e.g., "Corrected FIle.pdf") for your metadata dictionary
                just_file_name = os.path.basename(file_path)
                
                file = pymupdf.open(file_path)
                Page_count = len(file)
                
                for pages_num in range(Page_count):
                    page_num = file[pages_num]
                    texts = page_num.get_text()

                    for text in range(0, len(texts), 800):
                        chunk = texts[text: text + 1000]

                        all_chunks.append({
                            "file_name": just_file_name, # Safe file name extraction
                            "page_number": pages_num + 1,
                            "Content": chunk
                        })
                        
            except Exception as e:
                logging.info(f"Error processing file {file_path}: {e}")

        return all_chunks


if __name__ == "__main__":
    folderPath = "D:\\Projects\\CogniFlow\\documents\\"
    engine = DocumentIngester()
    result = engine.Reader(folderPath)
    print(result)