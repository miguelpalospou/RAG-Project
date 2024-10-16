import streamlit as st
from code.transcription import transcription
from code.model import model
from code.vectorstore import vectorstore
from code.chains import chains
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env")

# Title of the app
st.title("🤖 YoutuberGPT")

# Input API Keys
st.subheader("API Keys")
OPENAI_API_KEY = st.text_input("Enter your OpenAI API Key:", type="password", value=os.getenv("OPENAI_API_KEY"))
PINECONE_API_KEY = st.text_input("Enter your Pinecone API Key:", type="password", value=os.getenv("PINECONE_API_KEY"))

# Step 1: Input YouTube Link
youtube_link = st.text_input("Enter YouTube Video Link with quotes:")

# Step 2: Choose a name for the transcription file
transcription_name = st.text_input("Enter a name for the transcription file:")

# Step 3: Input the Pinecone Index Name
index_name = st.text_input("Enter a name for the Pinecone Index:")

# Ensure all necessary inputs are provided
if youtube_link and transcription_name and index_name and OPENAI_API_KEY and PINECONE_API_KEY:
    if st.button("Transcribe and Process Video"):
        st.write("Transcribing video... Please wait.")
        
        # Step 4: Transcribe the video
        transcription_text = transcription(youtube_link, transcription_name)
        st.write("Transcription complete!")

        # Step 5: Set up the vector store
        st.write("Setting up the vector store...")
        try:
            # Call the model function and store the LLM model in session state
            llm_model, _, _ = model(OPENAI_API_KEY, PINECONE_API_KEY)
            st.session_state.llm_model = llm_model
            
            # Call the vectorstore function
            st.session_state.pinecone_vectorstore = vectorstore(OPENAI_API_KEY, PINECONE_API_KEY, index_name, transcription_text)
            st.write("Vector store setup complete.")
        except Exception as e:
            st.error(f"Error setting up vector store: {e}")
else:
    st.warning("Please fill in all fields before proceeding.")

# Step 6: Ask Questions
question = st.text_input("Ask a question about the video:")

if question:
    if st.button("Get Answer"):
        # Step 7: Retrieve the answer using the question
        if 'pinecone_vectorstore' in st.session_state:
            answer = chains(st.session_state.pinecone_vectorstore, question, st.session_state.llm_model)
            st.write("Answer:")
            st.write(answer)
        else:
            st.write("Vector store not initialized. Please transcribe the video first.")



