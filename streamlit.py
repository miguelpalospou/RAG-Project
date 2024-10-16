import streamlit as st
from code.transcription import transcription
from code.model import model
from code.vectorstore import vectorstore
from code.chains import chains

# Title of the app
st.title("🤖YoutuberGPT")

# Input API Keys
st.subheader("API Keys")
OPENAI_API_KEY = st.text_input("Enter your OpenAI API Key:", type="password")
PINECONE_API_KEY = st.text_input("Enter your Pinecone API Key:", type="password")

# Step 1: Input YouTube Link
youtube_link = st.text_input("Enter YouTube Video Link with quotes:")

# Step 2: Choose a name for the transcription file
transcription_name = st.text_input("Enter a name for the transcription file:")

# Step 3: Input the Pinecone Index Name
index_name = st.text_input("Enter a name for the Pinecone Index:")

# Check if all necessary inputs are provided
if youtube_link and transcription_name and index_name and OPENAI_API_KEY and PINECONE_API_KEY:
    if st.button("Transcribe and Process Video"):
        st.write("Transcribing video... Please wait.")
        
        # Perform transcription
        transcription_text = transcription(youtube_link, transcription_name)
        st.write("Transcription complete!")

        # Step 6: Set up the vector store
        st.write("Setting up the vector store...")

        # Call the model function
        try:
            llm_model, _, _ = model(OPENAI_API_KEY, PINECONE_API_KEY)
            st.session_state.llm_model = llm_model
        except Exception as e:
            st.error(f"Error initializing model: {e}")
            st.stop()  # Stop further execution

        # Call vectorstore function
        try:
            st.session_state.pinecone_vectorstore = vectorstore(OPENAI_API_KEY, PINECONE_API_KEY, index_name, transcription_text)
            st.write("Vector store setup complete.")
        except Exception as e:
            st.error(f"Error setting up vector store: {e}")

# Step 7: Ask Questions
question = st.text_input("Ask a question about the video:")

if question:
    if st.button("Get Answer"):
        # Retrieve the answer using the question
        if 'pinecone_vectorstore' in st.session_state:
            answer = chains(st.session_state.pinecone_vectorstore, question, st.session_state.llm_model)
            st.write("Answer:")
            st.write(answer)
        else:
            st.write("Vector store not initialized. Please transcribe the video first.")



