# main.py
import os
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain_qdrant import QdrantVectorStore  
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings

# Load environment variables from the .env file
load_dotenv('var.env')

# Define a class for the chatbot
class Main:
    def __init__(self, collection_name="my_documents", qdrant_url="http://localhost:6333"):
        self.model_name = "sentence-transformers/all-mpnet-base-v2"
        self.model_kwargs = {'device': 'cpu'}
        self.encode_kwargs = {'normalize_embeddings': False}
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs=self.model_kwargs,
            encode_kwargs=self.encode_kwargs
        )
        
        # Connect to existing Qdrant collection
        self.vectbd = self.connect_to_qdrant(qdrant_url, collection_name)
        self.retriever = self.vectbd.as_retriever()
        
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0.7)
            
        # Create prompt template and chain
        self.prompt_template = self.create_prompt_template()
        self.chain = self.create_retrieval_qa_chain()

    def connect_to_qdrant(self, url, collection_name):
        """Connect to an existing Qdrant collection."""
        # Create client first, then use it with QdrantVectorStore
        from qdrant_client import QdrantClient
        client = QdrantClient(url=url)
        
        return QdrantVectorStore(
            client=client,  # Use client instead of client_location
            collection_name=collection_name,
            embedding=self.embeddings,  # Use embedding instead of embeddings
        )

    def create_prompt_template(self):
        """Create a prompt template for the conversation."""
        from prompt import template
        return PromptTemplate(
            input_variables=["history", "context", "question"],
            template=template,
        )

    def create_retrieval_qa_chain(self):
        """Create a RetrievalQA chain with the specified components."""
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type='stuff',
            retriever=self.retriever,
            chain_type_kwargs={
                "verbose": False,
                "prompt": self.prompt_template,
                "memory": ConversationBufferMemory(memory_key="history", input_key="question"),
            }
        )

    def get_response(self, user_input):
        """Get a response from the chatbot based on user input."""
        return self.chain.invoke(user_input)['result']

# Main function to run the chatbot in a loop
def main():
    # You can customize these parameters if needed
    chatbot = Main(
        collection_name="my_documents", 
        qdrant_url="http://localhost:6333"
    )
    
    print("Chatbot initialized. Type 'exit' to quit.")
    
    while True:
        prompt = input("User> ")
        if prompt.lower() == 'exit':
            break
        else:
            response = chatbot.get_response(prompt)
            print(f"AI Assistant: {response}")
            print("*********************************")

if __name__ == "__main__":
    main()