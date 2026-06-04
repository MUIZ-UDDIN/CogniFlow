from dotenv import load_dotenv
import os
from backend.vault import VectorVault
from openai import OpenAI

load_dotenv()

class knowledgeBrain():

    def __init__(self) -> None:
        self.apiKey = os.getenv("Api_Key", "")
        self.invoke_url = os.getenv("BaseUrl", "")
        self.client = OpenAI(api_key= self.apiKey, base_url=self.invoke_url)
        
    def ask(self, question:str, context: list):
        formated_chunks = []

        for chunk in context:
            line = f"source: {chunk['file']} (page{chunk['page']}): {chunk['text']}"

            formated_chunks.append(line)

        full_text = "\n\n".join(formated_chunks)

        instructions = (
            "You are CogniFlow, a professional PDF analyst. Answer the question using ONLY the context provided. "
            "If the answer isn't there, say you don't know. Only do a friendly response for 'hi' or 'hey' greeting messages. "
            "CRITICAL RULE: You must always explicitly mention the source filename and page number at the end of your answer as a citation."
        )

        user_message = f"Document Data: {full_text}\n\nUser Question: {question}"

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role":"system", "content":instructions},
                {"role":"user", "content": user_message}
                ],
            temperature=0.1,
            stream=True
            )

        for chunk in response:
            Content = chunk.choices[0].delta.content

            if Content:      
                yield Content

if __name__ == "__main__":
    engine = knowledgeBrain()
    VaultEngine = VectorVault()
    question = "Who is muiz and what his role and what they are presenting?"

    # 🎯 Test your targeted search by passing the exact file name here:
    target_file = "K-NEAREST NEIGHBOR ALGORITHM.pdf" 
    chunks = VaultEngine.search(question, file_name=target_file)

    # Safety Guard: Ensure chunks is handled as a list of strings
    if isinstance(chunks, str):
        chunks = []

    print(f"DEBUG Chunks Passed to AI: {chunks}\n")
    
    result = engine.ask(question, chunks)

    for text in result:

        print(text, end="", flush=True)
