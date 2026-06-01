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
        full_text = "\n".join(context)

        instructions = "You are CogniFlow, a professional PDF analyst. Answer the question using ONLY the context provided. If the answer isn't there, say you don't know. only do a friendly response for 'hi', 'hey', means for greeting messages and focus on document"
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

        # return response.choices[0].message.content

if __name__ == "__main__":
    engine = knowledgeBrain()
    VaultEngine = VectorVault()
    question = "Who is muiz and what his role and what they are presenting?"
    chunks = VaultEngine.search(question)

    result = engine.ask(question, chunks)
    
    for text in result:

        print(text, end="", flush=True)
