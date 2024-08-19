from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_community import embeddings



from langchain_text_splitters import RecursiveCharacterTextSplitter
import pandas as pd
from dotenv import load_dotenv

class FAQs:
    def __init__(self):
        load_dotenv(".env")


        # model
        MODEL = "llama3.1"
        model = Ollama(model=MODEL , base_url='http://ollama:11434')

        # Load data
        loader = DirectoryLoader('./docs/', glob="**/*.md" , loader_cls=TextLoader)
        data1 = loader.load()


        # text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=5000,
            chunk_overlap=200,
            # separators=[
            #     "###",
            #     "##",
            #     "#",
            # ]
            )
        splits = text_splitter.split_documents(data1)
        data = splits
        
        
        #Prompt Engineer
        template = """
        You are a chat bot assistance to answer people question about internet connection.
        Answer questions based on the context.
        If you can't answer the question, reply "I don't know".


        Context: {context}

        Question: {question}
        """
        prompt = PromptTemplate.from_template(template)

        # Convert documents to Embeddings and store them
        vectorstore = Chroma.from_documents(
            documents=data,
            collection_name="rag-chroma",
            embedding=embeddings.ollama.OllamaEmbeddings(model='nomic-embed-text' , base_url='http://ollama:11434'),
        )
        retriever = vectorstore.as_retriever()
        
        rag_chain = (
            {"context": lambda x: retriever, "question": RunnablePassthrough()} | prompt | model
        )

        rag_chain_with_source = RunnableParallel(
            {"context": retriever, "question": RunnablePassthrough()}
        ).assign(answer=rag_chain)
        
        self.rag_chain = rag_chain_with_source

    def request(self, message):
        try:
            res = self.rag_chain.invoke(message)
        except Exception as e:
            return "I don't know the answer to that question"
            
        return res['answer'] 


        
    @staticmethod
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    
    