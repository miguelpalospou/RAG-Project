def model(OPENAI_API_KEY=None, PINECONE_API_KEY=None):
    import os
    from dotenv import load_dotenv
    from langchain_openai import ChatOpenAI

    # Load from .env file if API keys are not provided (for standalone script)
    if OPENAI_API_KEY is None or PINECONE_API_KEY is None:
        load_dotenv(".env")  # Load environment variables from .env file
        OPENAI_API_KEY = OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        PINECONE_API_KEY = PINECONE_API_KEY or os.getenv("PINECONE_API_KEY")

        # Raise an error if API keys are not provided or found
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not provided and not found in .env file")
        if not PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY not provided and not found in .env file")

    # Initialize the OpenAI model with the API key
    model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4o-mini")
    
    return model, OPENAI_API_KEY, PINECONE_API_KEY

