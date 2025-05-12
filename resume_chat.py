import os
from dotenv import load_dotenv
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("API_GROQ")
from langchain_groq import ChatGroq
import requests
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA


class resume_chatbot():
    def __init__(self):
        
        self.model = ChatGroq(model = "gemma2-9b-it")
        os.environ["OPENAI_API_KEY" ] = os.getenv("OPENAI_API_KEY")
        self.prompt = ChatPromptTemplate.from_template(
     """
                You are Ann Maria Chirackal George, a highly skilled data scientist. Respond to questions as if you are Ann, based on the provided resume context.

            Instructions:
            1. Use a confident, first-person tone.
            2. Provide direct, context-rich responses without filler phrases like "Based on the information provided."
            3. If the context lacks a clear answer, respond with:
            "I don’t have an answer for this right now. You can reach me at annchirackal@gmail.com for further discussion."

            4. Avoid repeating the prompt in your answers. Just respond naturally, like a conversation.
            5. Hanle small talk questions without context

            Examples:
            Q: What is your proficiency in data science?
            A: I have extensive experience in data science, including model development, data engineering, and applied machine learning, with a strong focus on business impact.

            Q: What tools are you proficient in?
            A: I am skilled in Python, SQL, TensorFlow, R, SAS, and Jupyter Notebooks, allowing me to solve complex data challenges efficiently.

            Q: How many years of experience do you have in tech roles?
            A: I have over 4 years in data science roles and 8+ years in broader tech roles, including data analysis and engineering.

            Q: What is your background in business optimization?
            A: My background in supply chain analytics and business optimization enables me to turn data insights into real-world impact.

            Context:
            {context} + for generic questions use your world knowlegee to answer

            Question: {question} 
            Answer:"""
)
        doc_url = "https://docs.google.com/document/d/13uZQ4x8bHmjcUkpEA-r1BEm_k4YaxQJH/export?format=docx"
        
        docs = self._load_resume_from_google_doc(doc_url)
        splitted_docs = self._split_as_chunks(docs)
        self.vector_store=self._embed_and_vector_store(splitted_docs)
        self.qa_chain = RetrievalQA.from_chain_type(
                                                    llm=self.model,
                                                    retriever=self.vector_store.as_retriever(),
                                                    return_source_documents=False
                                                    )

    def _load_resume_from_google_doc(self,doc_url):
        response = requests.get(doc_url)
        with open("temp.docx", "wb") as f:
                f.write(response.content)
        loader = UnstructuredWordDocumentLoader("temp.docx")
        docs = loader.load()

        return docs
    
    def _split_as_chunks(self,docs):
        text_spiltter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 100 )
        splitted_docs = text_spiltter.split_documents(docs)
        return splitted_docs
    
    def _embed_and_vector_store(self,text_document):
        embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
        embeddings= OpenAIEmbeddings()
        vector_store =FAISS.from_documents(text_document,embeddings)
        return vector_store
    def get_answer(self,question):
        result = self.qa_chain.invoke(question)

        return result['result']

    


# if __name__ == "__main__":
    
#     resume_chatbot=resume_chatbot()
#     while True:
#         user_input = input("👤 You: ")
#         if user_input.lower() in ["exit", "quit"]:
#             print("👋 Goodbye!")
#             break
#         result = resume_chatbot.get_answer(user_input)
        
#         print(f"🤖 Bot: {result}\n")




