from dotenv import load_dotenv
import os
from vault import VectorVault
from openai import OpenAI

load_dotenv()

class knowledgeBrain():

    def __init__(self) -> None:
        self.apiKey = os.getenv("Api_Key", "")
        self.invoke_url = os.getenv("BaseUrl", "")
        self.client = OpenAI(api_key= self.apiKey, base_url=self.invoke_url)
        
    def ask(self, question:str, context: list):
        full_text = "\n".join(context)

        instructions = "You are CogniFlow, a professional PDF analyst. Answer the question using ONLY the context provided. If the answer isn't there, say you don't know."
        user_message = f"Document Data: {full_text}\n\nUser Question: {question}"

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role":"system", "content":instructions},
                {"role":"user", "content": user_message}
                ],
            temperature=0.1
            )

        return response.choices[0].message.content

if __name__ == "__main__":
    engine = knowledgeBrain()
    VaultEngine = VectorVault()
    question = "Who is muiz"
    chunks = VaultEngine.search(question)

    result = engine.ask(question, chunks)
    print(result)
