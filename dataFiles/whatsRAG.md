What is RAG? (Retrieval-Augmented Generation) </br>
If you are wondering how this "News Research Tool" actually works under the hood, you are looking at a technique called RAG.</br>
It sounds complicated, but the concept is actually very simple.</br>
The Problem: The "Closed Book" Exam</br>
Imagine ChatGPT (or any AI model) is a very smart student taking a test. This student has read millions of books, but there is a catch: they stopped reading in 2023.</br>
If you ask them: "Who won the game last night?" or "What is in this specific news article from today?", they will fail. They simply don't have that information in their memory. They might even try to guess (hallucinate) just to sound helpful.</br>
The Solution: The "Open Book" Exam (RAG)</br>
RAG (Retrieval-Augmented Generation) is the equivalent of letting that student take an open-book exam.
Instead of forcing the AI to rely on its memory, we give it a specific "textbook" (in this case, your news articles) and say: "Use this book to answer the question."</br>
How It Works (The Engineering Process)</br>
This application performs RAG in three distinct phases. Here is the translation from "Concept" to "Code":</br>


# *Phase 1: Ingestion & Indexing (The Librarian)* </br>
Before the AI can answer, we need to prepare the data. This involves three critical engineering steps:
</br>

### *Loading Data (Ingestion)*: </br>
Concept: Gathering the raw materials.</br>
Technical Process: We use a Loader (UnstructuredURLLoader). It visits the websites, scrapes the HTML, and extracts just the readable text, ignoring ads and navigation bars.</br>

### *Splitting (Chunking)*:</br>
Concept: Cutting a long book into bite-sized index cards.</br>
Technical Process: LLMs have a limit on how much text they can read at once (context window). We use a Text Splitter (RecursiveCharacterTextSplitter) to break the long articles into smaller "chunks" (e.g., 1000 characters each). We use "overlap" to ensure sentences aren't cut in half awkwardly.</br>

### *Embedding & Storage (Vectorization)*:</br>
Concept: Filing the index cards by meaning, not just alphabetically.</br>
Technical Process: This is the magic. We use an Embedding Model (OpenAIEmbeddings) to convert text chunks into lists of numbers called Vectors. These numbers represent the meaning of the text. We store these in a Vector Database (FAISS) which allows for ultra-fast "Similarity Search."</br>


# *Phase 2: Retrieval (The Setup)* </br>
When you ask a question, the app doesn't send it straight to the AI.</br>
Semantic Search:</br>
The app converts your question into numbers (vectors) too.</br>
It asks FAISS: "Find me the 3 chunks of text that are most mathematically similar to this question."</br>


# *Phase 3: Generation (The Answer)* </br>
Now we have the user's question and the relevant facts found by the search.</br>

Prompt Engineering:</br>
The app constructs a strict instructions prompt for the LLM:System: Answer the question using ONLY the following context.</br>
Context: [Chunk 1] [Chunk 2] [Chunk 3]v
User Question: "What is AFP?"</br>
Inference:</br>
The LLM (OpenAI) reads the context and generates the final answer. It cites the sources because it knows exactly which chunk provided the information.</br>

Why Use RAG?</br>
Accuracy: The AI doesn't guess; it reads from the source.</br>
Up-to-Date: You can feed it news from 5 minutes ago, and it will understand it.</br>
Privacy: You can use RAG on your own private company documents without training the public AI on your secrets.</br>
Source Citing: Because the app knows exactly which paragraphs it retrieved, it can tell you where it found the answer (e.g., "Source: Link 1").</br>
