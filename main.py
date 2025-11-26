import os
import streamlit as st
import pickle

# 1. Partner Package (Models)
from langchain_openai import OpenAI, OpenAIEmbeddings

# 2. Community Tools (Loaders & Vector Stores)
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.vectorstores import FAISS

# 3. Splitters
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 4. Chains (Using CLASSIC for v1.1 compatibility)
from langchain_classic.chains import RetrievalQAWithSourcesChain

# --- APP CONFIGURATION ---
st.set_page_config(page_title="News Research Tool", page_icon="📈")
st.title("News Research Tool 📈")
st.markdown("Enter news URLs in the sidebar to build a custom knowledge base.")

# --- SIDEBAR: DATA INGESTION ---
st.sidebar.title("1. Configuration")

# Securely ask for API Key (or load from .env if you prefer)
api_key = st.sidebar.text_input("OpenAI API Key", type="password")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

st.sidebar.title("2. Data Sources")
urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    if url:
        urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs")
file_path = "faiss_store_openai.pkl"

# --- MAIN LOGIC: PROCESS DATA (ETL) ---
if process_url_clicked:
    if not api_key:
        st.error("Please enter your OpenAI API Key in the sidebar first!")
    elif not urls:
        st.error("Please enter at least one URL.")
    else:
        # Create a status container
        status_container = st.status("Processing Data...", expanded=True)
        
        try:
            # 1. LOAD
            status_container.write("Scraping URLs")
            loader = UnstructuredURLLoader(urls=urls)
            data = loader.load()
            
            # 2. SPLIT
            status_container.write("Splitting text into chunks")
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            docs = text_splitter.split_documents(data)
            status_container.write(f"Created {len(docs)} document chunks")

            # 3. EMBED & INDEX
            status_container.write("Generating Embeddings & Building Index")
            embeddings = OpenAIEmbeddings()
            vector_index = FAISS.from_documents(docs, embedding=embeddings)
            
            # 4. SAVE (Persistence)
            with open(file_path, "wb") as f:
                pickle.dump(vector_index, f)
            
            status_container.update(label="Processing Complete!", state="complete", expanded=False)
            st.success("Index built and saved successfully! You can now ask questions.")
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

# --- RAG ---
st.divider()
st.header("Ask a Question")
query = st.text_input("What do you want to know about these articles?")

if query:
    if os.path.exists(file_path):
        if not api_key:
             st.error("Please enter your OpenAI API Key to run the query.")
        else:
            with st.spinner("Thinking..."):
                try:
                    # 1. Load the Index
                    with open(file_path, "rb") as f:
                        vector_index = pickle.load(f)
                    
                    # 2. Initialize LLM
                    llm = OpenAI(temperature=0.9, max_tokens=500)
                    
                    # 3. Create Chain
                    chain = RetrievalQAWithSourcesChain.from_chain_type(
                        llm=llm, 
                        chain_type="stuff", 
                        retriever=vector_index.as_retriever()
                    )
                    
                    # 4. Run Chain (Using .invoke)
                    result = chain.invoke({"question": query})
                    
                    # 5. Display Result
                    st.write("### Answer")
                    st.write(result["answer"])
                    
                    # 6. Display Sources
                    sources = result.get("sources", "")
                    if sources:
                        st.write("### Sources")
                        st.write(sources)
                        
                except Exception as e:
                    st.error(f"Error occurred: {e}")
                    st.write("Tip: Try reprocessing the URLs if the index file is corrupted.")
    else:
        st.info("⚠️ No index found. Please process some URLs in the sidebar first.")