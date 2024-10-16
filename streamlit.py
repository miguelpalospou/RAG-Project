import streamlit as st
from code.transcription import transcription
from code.model import model
from code.vectorstore import vectorstore
from code.chains import chains

# Title of the app
st.title("🤖YoutuberGPT")

# Input API Keys
st.subheader("API Keys")
if "OPENAI_API_KEY" not in st.session_state:
    st.session_state.OPENAI_API_KEY = st.text_input("Enter your OpenAI API Key:", type="password")
else:
    st.session_state.OPENAI_API_KEY = st.text_input("OpenAI API Key", value=st.session_state.OPENAI_API_KEY, type="password")

if "PINECONE_API_KEY" not in st.session_state:
    st.session_state.PINECONE_API_KEY = st.text_input("Enter your Pinecone API Key:", type="password")
else:
    st.session_state.PINECONE_API_KEY = st.text_input("Pinecone API Key", value=st.session_state.PINECONE_API_KEY, type="password")


# Step 1: Input YouTube Link
youtube_link = st.text_input("Enter YouTube Video Link with quotes:")

# Step 2: Choose a name for the transcription file
transcription_name = st.text_input("Enter a name for the transcription file:")

# Step 3: Input the Pinecone Index Name
index_name = st.text_input("Enter a name for the Pinecone Index:")

if youtube_link and transcription_name and index_name and st.session_state.OPENAI_API_KEY and st.session_state.PINECONE_API_KEY:
    if st.button("Transcribe and Process Video"):
        st.write("Transcribing video... Please wait.")
        transcription_text = transcription(youtube_link, transcription_name)
        st.write("Transcription complete!")

        # Step 6: Set up the vector store
        st.write("Setting up the vector store...")
        try:
            llm_model, _, _ = model(st.session_state.OPENAI_API_KEY, st.session_state.PINECONE_API_KEY)
            st.session_state.llm_model = llm_model

            st.session_state.pinecone_vectorstore = vectorstore(st.session_state.OPENAI_API_KEY, st.session_state.PINECONE_API_KEY, index_name, transcription_text)
            st.write("Vector store setup complete.")
        except Exception as e:
            st.error(f"Error setting up vector store: {str(e)}")


# Step 7: Ask Questions
question = st.text_input("Ask a question about the video:")

if question:
    if st.button("Get Answer"):
        if 'pinecone_vectorstore' in st.session_state:
            answer = chains(st.session_state.pinecone_vectorstore, question, st.session_state.llm_model)
            st.write("Answer:")
            st.write(answer)
        else:
            st.write("Vector store not initialized. Please transcribe the video first.")




