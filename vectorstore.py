def vectorstore(PINECONE_API_KEY, index_name, transcription):
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.document_loaders import TextLoader
    from langchain_openai.embeddings import OpenAIEmbeddings
    from langchain_pinecone import PineconeVectorStore
    from pinecone.grpc import PineconeGRPC as Pinecone
    from pinecone import ServerlessSpec
    from langchain_community.vectorstores import DocArrayInMemorySearch
    from langchain_core.runnables import RunnableParallel, RunnablePassthrough

    loader= TextLoader("transcription.txt")
    text_documents = loader.load()
    text_splitter= RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    documents = text_splitter.split_documents(text_documents)
    embeddings = OpenAIEmbeddings()
    
    # loading the transcription into the vector store:
    vectorstore2= DocArrayInMemorySearch.from_documents(documents, embeddings)
    setup2=RunnableParallel(context=vectorstore2.as_retriever(), question=RunnablePassthrough())


    pc = Pinecone(api_key=PINECONE_API_KEY)

    pc.create_index(
    name=index_name,
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
    )

    pinecone= PineconeVectorStore.from_documents(
    documents, embeddings, index_name=index_name)

    return pinecone