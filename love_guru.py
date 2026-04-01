from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_community.embeddings import HuggingFaceEmbeddings
from prompt_templates import main_rag_template, situationship_template, categorize_template
from extraction_pipeline import extract_relationship_advice
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()


class LoveDocIngester:
    EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

    def __init__(self, persist_directory: str = "./chroma_db", data_dir: str = "./data"):
        self.persist_directory = persist_directory
        self.data_dir = data_dir

        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.EMBEDDING_MODEL,
            model_kwargs={'device': 'cuda'},
            encode_kwargs={'normalize_embeddings': True}
        )

        self.vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings,
            collection_name="love_docs"
        )

        self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=300,
            chunk_overlap=50
        )

    def ingest_doc(self, documents: list):
        self.documents = documents
        splits = self.text_splitter.split_documents(self.documents)

        self.vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name="love_docs"
        )

        self.vectorstore.persist()

        self.retriever = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 10, "lambda_mult": 0.5}
        )

        return self.retriever


class QueryPipeline:
    EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    RELATIONSHIP_PROMPT = PromptTemplate.from_template(main_rag_template())
    SITUATIONSHIP_PROMPT = PromptTemplate.from_template(situationship_template())
    CATEGORIZE_TEMPLATE = PromptTemplate.from_template(categorize_template())
    LLM_MODEL = "gemini-3-flash-preview"

    def __init__(self):
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=self.LLM_MODEL,
                temperature=0.7
            )
        except Exception as e:
            print(f"Warning: Could not initialize LLM: {e}")
            raise RuntimeError("LLM initialization failed")

        vectorstore = Chroma(
            persist_directory="./chroma_db",
            embedding_function=HuggingFaceEmbeddings(
                model_name=self.EMBEDDING_MODEL,
                model_kwargs={'device': 'cuda'},
                encode_kwargs={'normalize_embeddings': True}
            ),
            collection_name="love_docs"
        )

        if vectorstore._collection.count() == 0:
            documents = extract_relationship_advice()
            self.retriever = LoveDocIngester().ingest_doc(documents)
        else:
            self.retriever = vectorstore.as_retriever()

        self.situationship_chain = (
                self.SITUATIONSHIP_PROMPT
                | self.llm
                | StrOutputParser()
        )

        self.relationship_chain = (
                self.RELATIONSHIP_PROMPT
                | self.llm
                | StrOutputParser()
        )

    def categorize(self, user_query: str):
        generate_category = (
                self.CATEGORIZE_TEMPLATE
                | self.llm
                | JsonOutputParser()
        )

        return generate_category.invoke({"user_input": user_query})

    def format_docs(self, docs):
        return "\n\n".join([
            f"[Source {i + 1}] ({doc.metadata.get('source', 'unknown')})\n{doc.page_content}"
            for i, doc in enumerate(docs)
        ])

    def retrieval_chain(self, user_query: str):
        docs = self.retriever.invoke(user_query)
        context = self.format_docs(docs)

        json_output = self.categorize(user_query)
        category = json_output.get("category", "RELATIONSHIP_ADVICE")
        if category == "SITUATIONSHIP_ADVICE":
            return self.situationship_chain.invoke({"question": user_query, "context": context})

        else:
            return self.relationship_chain.invoke({"question": user_query, "context": context})

