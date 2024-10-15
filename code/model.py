
def model():

    import os
    from dotenv import load_dotenv
    from langchain.chat_models import ChatOpenAI

    load_dotenv(".env")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4o-mini")
    return model, OPENAI_API_KEY, PINECONE_API_KEY