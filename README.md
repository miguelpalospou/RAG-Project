
# Building a RAG application from scratch

The following projects consists on a system that transcripts videos from youtube and enables users to interact with it through questions. It's built using LangChain, GPT4 and a simple RAG (Retrieval-Augmented Generation) application using Pinecone and OpenAI's API. The application will allow you to ask questions about any YouTube video.

![Alt text](./images/RAGGS.png)




## Content

1. main_detailed.ipynb: this is the comprehensive notebook that includes testings, detailed explanations and so on. Designed to walk users through the process.

2. main.ipynb. Main notebook that centralizes all encapsulated functions built within the other .py files: transcription.py, vectorstore.py, model.py and chains.py.

3. Streamlit: Amazing app created by Miguel to make it easier for users to play around with the model.

### Short tutorial on how to run it:


[![Watch the video](./images/test.jpeg)](https://youtube.com/watch?v=Ym1b8ZgOM14&ab_channel=MiguelPalosPou)

https://youtube.com/watch?v=Ym1b8ZgOM14&ab_channel=MiguelPalosPou
## Setup

1. Create a virtual environment and install the required packages:

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

2. Create a free Pinecone account and get your API key from [here](https://www.pinecone.io/).

3. Create a `.env` file with the following variables:

```bash
OPENAI_API_KEY = [ENTER YOUR OPENAI API KEY HERE]
PINECONE_API_KEY = [ENTER YOUR PINECONE API KEY HERE]
PINECONE_API_ENV = [ENTER YOUR PINECONE API ENVIRONMENT HERE]
```

## Theoretical explanation

1. **main_detailed.ipynb**: Creating a RAG with an In-Memory Vector Database. This notebook shows how to build a RAG (Retrieval-Augmented Generation) with a local in-memory vector store. It also demonstrates how to run OpenAI models with LangChain.

   ### Content:
   - Running an LLM
   - Loading PDF Documents
   - Prompt Engineering
   - Creating a Local In-Memory Vector Database
   - Testing End-to-End RAG


---

## Models

### OpenAI:
```python
from langchain_openai.chat_models import ChatOpenAI

MODEL = "gpt-4o-mini"
model = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model=MODEL)
```
## Embeddings
```
from langchain_openai.embeddings import OpenAIEmbeddings

#### Using the default model
embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

#### Specifying a custom embedding model
embeddings = OpenAIEmbeddings(
    api_key=os.getenv("OPENAI_API_KEY"), model="embedding_model"
)
```
## Vector Stores

#### For the following examples, we use a PDF document loader to load a document and split it into pages:
```
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

loader= TextLoader("transcription.txt")
text_documents = loader.load()

text_splitter= RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)

```
## Local In-Memory Vector Store
#### For the following examples, we use a PDF document loader to load a document and split it into pages:
```
from langchain_community.vectorstores import DocArrayInMemorySearch

vectorstore = DocArrayInMemorySearch.from_documents(
    pages,
    embedding=embeddings
)
retriever = vectorstore.as_retriever()
retriever.invoke("Information to retrieve")
```
## Retrievers

#### The VectorStoreRetriever class wraps vector stores to allow easy querying. Some configuration options include:

search_type: Type of search to perform ("similarity" (default), "mmr", or "similarity_score_threshold")
search_kwargs: Additional arguments to pass to the search function
k: Number of documents to return (default is 4)
score_threshold: Minimum relevance threshold (default is 0)
fetch_k: Number of documents to pass to the MMR algorithm (default is 20)
lambda_mult: Diversity of results in MMR (1 for minimum diversity, 0 for maximum diversity)
filter: Filter by document metadata