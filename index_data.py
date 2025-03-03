import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader, Docx2txtLoader, UnstructuredWordDocumentLoader, PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import Qdrant

def main():
    # Configuration (modify these variables as needed)
    DATA_PATH = r'E:\RAG App\code\data'  # Path to your data directory
    COLLECTION_NAME = 'my_documents'  # Name of Qdrant collection
    CHUNK_SIZE = 500  # Document chunk size
    CHUNK_OVERLAP = 50  # Overlap between chunks
    QDRANT_URL = 'http://localhost:6333'  # Qdrant server URL
    
    print(f"Loading documents from: {DATA_PATH}")
    
    # Load documents
    documents = load_documents(DATA_PATH)
    print(f"Loaded {len(documents)} documents")
    
    # Split documents
    docs = split_documents(documents, CHUNK_SIZE, CHUNK_OVERLAP)
    print(f"Split into {len(docs)} chunks")
    
    # Initialize embeddings
    embeddings = initialize_embeddings()
    print("Initialized embeddings model")
    
    # Index to Qdrant
    vectorstore = index_to_qdrant(docs, embeddings, QDRANT_URL, COLLECTION_NAME)
    print(f"Indexed documents to Qdrant collection: {COLLECTION_NAME}")

def load_documents(data_path):
    """Load documents from a file or directory."""
    if os.path.isfile(data_path):
        # Handle single file based on extension
        extension = os.path.splitext(data_path)[1].lower()
        if extension == '.pdf':
            loader = PyPDFLoader(data_path)
        elif extension == '.docx':
            loader = Docx2txtLoader(data_path)
        elif extension == '.doc':
            loader = UnstructuredWordDocumentLoader(data_path)
        else:  # Default to text loader for .txt and other files
            loader = TextLoader(data_path)
        return loader.load()
    
    elif os.path.isdir(data_path):
        # Load multiple file types from directory
        loaders = []
        
        # Text files
        txt_loader = DirectoryLoader(
            data_path,
            glob="**/*.txt",
            loader_cls=TextLoader
        )
        loaders.append(txt_loader)
        
        # PDF files
        pdf_loader = DirectoryLoader(
            data_path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
        loaders.append(pdf_loader)
        
        # DOCX files
        docx_loader = DirectoryLoader(
            data_path,
            glob="**/*.docx",
            loader_cls=Docx2txtLoader
        )
        loaders.append(docx_loader)
        
        # DOC files
        doc_loader = DirectoryLoader(
            data_path,
            glob="**/*.doc",
            loader_cls=UnstructuredWordDocumentLoader
        )
        loaders.append(doc_loader)
        
        # Load and combine all documents
        all_documents = []
        for loader in loaders:
            try:
                docs = loader.load()
                print(f"Loaded {len(docs)} documents with {loader.__class__.__name__}")
                all_documents.extend(docs)
            except Exception as e:
                print(f"Error loading with {loader.__class__.__name__}: {str(e)}")
        
        return all_documents
    
    else:
        raise ValueError(f"Path {data_path} is not a valid file or directory")

def split_documents(documents, chunk_size, chunk_overlap):
    """Split documents into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(documents)

def initialize_embeddings():
    """Initialize the HuggingFace embeddings model."""
    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

def index_to_qdrant(docs, embeddings, qdrant_url, collection_name):
    """Index documents to Qdrant."""
    qdrant = Qdrant.from_documents(
        docs,
        embeddings,
        url=qdrant_url,
        prefer_grpc=False,
        collection_name=collection_name,
    )
    return qdrant

if __name__ == "__main__":
    main()