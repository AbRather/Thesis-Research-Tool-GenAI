# My GenAI Project
# Thesis Research Tool 📈

Hi there! This is a simple Python application that lets you "chat" with research pages.

Have you ever opened 10 different tabs trying to research a topic, only to get overwhelmed by the reading? This tool solves that. You just paste the URLs of the articles you want to read, and the AI reads them for you. Then, you can ask questions like "What is the summary?" or "What are the key dates?" and get answers based only on those specific research topic.

How it Works (Simply Put)

Reading: The tool visits the websites you provide and scrapes the text (like a robot reader).

Memory: It breaks that text into small chunks and saves them in a special searchable database on your computer (FAISS).

Answering: When you ask a question, it finds the most relevant chunks of text and sends them to OpenAI (ChatGPT) to generate a precise answer for you.

How to Run It on Your Computer

1. Get the Code

Clone this repository to your local machine:

git clone <your-repo-url>


2. Install the "Ingredients"

You need a few Python libraries to make this work. Open your terminal in the project folder and run:

pip install -r requirements.txt


(Note: If you are on a Mac, you might also need to run brew install libmagic for the URL loader to work).

3. Launch the App

Run this command to start the website locally:

streamlit run main.py


How to Use It

API Key: On the left sidebar, paste your OpenAI API Key. (The app uses this to talk to the AI brain).

Add Links: Paste up to 3 URLs of news articles you want to analyze.

Process: Click the "Process URLs" button. You'll see the status update as it works.

Ask: Once it says "Processing Complete," go to the main chat box and ask your question!

The Tech Stack

Streamlit: For the web interface.

LangChain: For handling the logic.

OpenAI: For the intelligence.

FAISS: For the vector memory.

Project Structure

main.py: The main application script.

requirements.txt: A list of python packages needed to run the app.

faiss_store_openai.pkl: (Generated locally) The file where the AI stores the article memory.
