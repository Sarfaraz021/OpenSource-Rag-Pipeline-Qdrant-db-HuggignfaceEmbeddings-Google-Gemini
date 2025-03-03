# RAG Application

A question-answering RAG (Retrieval-Augmented Generation) system built with Langchain, Qdrant and Gemini. 

## Prerequisites

- Python 3.11.5 or later
- Docker Desktop
- Install GCP https://cloud.google.com/sdk/docs/install
- SetUp Local development Environment: https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment
- Get Google API Key: https://ai.google.dev/gemini-api/docs/api-key

## Installation

1. Navigate to 'code' directory
```bash
cd RAG-App
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. Install dependencies
```bash
pip install langchain-community
pip install langchain
pip install python-dotenv
pip install langchain-huggingface
pip install unstructured
pip install "unstructured[docx]" "unstructured[pdf]" docx2txt
pip install -qU langchain-qdrant
pip install pypdf
pip install -qU langchain-google-genai
%pip install -qU langchain-openai
```

## Setting up Qdrant

1. Pull the Qdrant Docker image:
```bash
docker pull qdrant/qdrant
```

2. Run the Qdrant container:
```bash
docker run -p 6333:6333 -v "E:\RAG App\Indexed Data:/qdrant/storage" qdrant/qdrant
```
Note: Replace `E:\RAG App` with your actual project path if different.

3. Verify the installation by accessing:
```bash
curl http://localhost:6333
```

## Usage

1. To Index and Load your data 
```bash
  navigate to index_data.py Specify the path to your data files it supports pdfs, txt, word doc/docx for now.
  run 
  python index_data.py
```
2. Start the application:
```bash
python main.py
```

## Support

If you need assistance, feel free to schedule a Zoom meeting for detailed guidance.

